import socket
import time
import os

#read settings from a yml file
import yaml
settings = {}
with open("settings.yml", 'r') as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 12345

s.bind((host,port))
s.listen(5)

is_editor_open = False
is_playing = False
lives_played = 0

while True:
    c, addr = s.accept()
    print(f"Connection from: {addr}")
    while True:
        data = c.recv(1024)
        if not data:
            break
        ue_status = data.decode()
        print(f"Received data: {ue_status}")
        #if ue_status contains substring 'ready' and the editor is not open, open the editor
        if str(ue_status).find('ready') != -1 and not is_playing:
            is_editor_open = True

            if settings['num_simulations'] != 1:
                time.sleep(2)
                c.send(b'play')

            is_playing = True

            #go to ./airsim-ros and run the run_test_square.sh script
            print("AirSim status: " + str(settings['airsim']))
            if settings['airsim']:
                time.sleep(3)
                os.chdir("./airsim-ros")
                os.system("tmux new-window -t Sim:3 -n AirSim-Master './run_test_square.sh; exec bash';")
                os.chdir("..")
        if is_playing:
            if settings['play_time'] > 0:
                time.sleep(settings['play_time'])
                lives_played += 1
                #close the tmux 'AirSim' window from the 'Sim' session
                if settings['airsim']:
                    os.system("tmux kill-window -t AirSim")
                    os.system("docker stop /airsim-ros")

                c.send(b'stop')
                is_playing = False

                if lives_played >= settings['num_simulations'] and settings['num_simulations'] >= 1:
                    os.system("./kill_all.sh")
            else:
                while True:
                    continue
            
        time.sleep(1)
    c.close()

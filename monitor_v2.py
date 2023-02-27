import socket
import time
import os
import yaml

settings = {}
with open("settings.yml", 'r') as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

is_editor_open = False
is_playing = False
lives_played = 0

def getCurrentTime():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

bag_folder = "./bags/"+getCurrentTime()
os.makedirs(bag_folder)
for i in range(0, settings['num_simulations']):
    os.makedirs(bag_folder+"/"+str(i+1))

while True:
    #check if 'ready.txt' exists in the ./shared folder
    if os.path.exists('./shared/ready.txt'):
        print("[" + getCurrentTime() + "]" + "Unreal Editor is ready")
        if not os.path.exists('./shared/play.txt'):
            print("[" + getCurrentTime() + "]" + "Creating play.txt file to let the editor know to start the game")
            #send a message to the editor to start the game
            time.sleep(1)
            os.system('touch ./shared/play.txt')
            is_editor_open = True
            is_playing = True

            #go to ./airsim-ros and run the run_test_square.sh script
            print("AirSim status: " + str(settings['airsim']))
            if settings['airsim']:
                time.sleep(2)
                print("[" + getCurrentTime() + "]" + " Starting AirSim")
                os.chdir("./airsim-ros")
                os.system("tmux new-window -t Sim:3 -n AirSim-Master './run.sh; exec bash';")
                os.chdir("..")

                os.chdir(bag_folder+"/"+str(lives_played+1))
                print("[" + getCurrentTime() + "]" + " Starting baggin info at " + bag_folder+"/"+str(lives_played+1))
                os.system("tmux new-window -t Sim:4 -n ROS-Bags 'rosbag record -O ros.bag /mindful_image /mindful_depth /mindful_info /mindful_pose; exec bash';")
                print("[" + getCurrentTime() + "]" + " Started baggin info at " + bag_folder+"/"+str(lives_played+1))
                os.chdir("../../..")
                print("Now waiting for the game to start...")
        #check if the "playing.txt" file exists
        elif os.path.exists('./shared/playing.txt'):
            if settings['play_time'] > 0:
                print("[" + getCurrentTime() + "]" + " Playing for " + str(settings['play_time']) + " seconds")
                time.sleep(settings['play_time'])
                lives_played += 1
                #close the tmux 'AirSim' window from the 'Sim' session
                if settings['airsim']:
                    print("[" + getCurrentTime() + "]" + " Closing AirSim window and stopping bagging")

                    #sending Ctrl+C to the ROS-Bags tmux window
                    os.system("tmux send-keys -t ROS-Bags C-c")
                    time.sleep(0.5)

                    #sending Ctrl+C to the Publisher tmux window inside airsim-ros container
                    os.system("docker exec -it airsim-ros tmux send-keys -t Publisher C-c")
                    time.sleep(0.75)
                    #renaming the Publisher window to 'Extractor'
                    os.system("docker exec -it airsim-ros tmux rename-window -t Publisher Extractor")
                    #telling thge Extractor window to run image_extractor.py
                    os.system("docker exec -it airsim-ros tmux send-keys -t Extractor 'python3 /root/shared/src/image_extractor.py; exec bash' ENTER")
                    
                    os.chdir(bag_folder+"/"+str(lives_played))
                    os.system("rosbag play ros.bag")
                    os.chdir("../../..")

                    #copy the contents of the temporary rgb/ folder to the current bag folder
                    os.system("cp -r ./airsim-ros/shared/src/rgb/ " + bag_folder+"/"+str(lives_played))
                    os.system("tmux kill-window -t ROS-Bags")
                    os.system("tmux kill-window -t AirSim")
                    os.system("docker stop /airsim-ros")



                #create the 'stop.txt' file
                print("[" + getCurrentTime() + "]" + " Creating stop.txt file to let the editor know to stop the game")
                os.system('touch ./shared/stop.txt')

                print("[" + getCurrentTime() + "]" + " Lives played in total so far: " + str(lives_played))

                time.sleep(2)
                os.system('rm ./shared/play.txt')

                if lives_played >= settings['num_simulations'] and settings['num_simulations'] >= 1:
                    os.system("./kill_all.sh")
            else:
                while True:
                    continue

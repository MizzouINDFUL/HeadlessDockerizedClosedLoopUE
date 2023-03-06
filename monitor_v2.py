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

#print out the topic names
print("Topics: ", settings['topics'])

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
                #get the array of key names from the topics dictionary
                topic_names = list(settings['topics'].keys())
                #include the names of the topics in the rosbag record command without comas
                topic_names = " ".join(topic_names)
                os.system("tmux new-window -t Sim:4 -n ROS-Bags 'rosbag record -O ros.bag "+topic_names+"; exec bash';")
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
                    print("[" + getCurrentTime() + "]" + " Closing AirSim window and extracting the ROS bag")

                    #sending Ctrl+C to the ROS-Bags tmux window
                    os.system("tmux send-keys -t ROS-Bags C-c")
                    time.sleep(0.5)

                    #sending Ctrl+C to the Publisher tmux window inside airsim-ros container
                    os.system("docker exec -it airsim-ros tmux send-keys -t Publisher C-c")
                    time.sleep(0.5)
                    #renaming the Publisher window to 'Extractor'
                    os.system("docker exec -it airsim-ros tmux rename-window -t Publisher Extractor")
                    #copying the settings.yml file to the airsim-ros container
                    os.system("docker cp ./settings.yml airsim-ros:/root/shared/src/settings.yml")
                    #telling thge Extractor window to run image_extractor.py
                    os.system("docker exec -it airsim-ros tmux send-keys -t Extractor 'python3 /root/shared/src/airsim_extractor.py; exec bash' ENTER")
                    
                    os.chdir(bag_folder+"/"+str(lives_played))
                    os.system("rosbag play ros.bag")
                    os.chdir("../../..")

                    #copy the contents of the temporary rgb/ folder to the current bag folder
                    #traverser through the values of the topics dictionary and copy each folder to the current bag folder
                    for folder in settings['topic-folder'].values():
                        if folder != '.' and folder != '':
                            print("Copying " + folder + " to " + bag_folder+"/"+str(lives_played))
                            print("Number of files in " + folder + ": " + str(len(os.listdir("./airsim-ros/shared/src/"+folder))))
                            os.system("cp -r ./airsim-ros/shared/src/"+folder+"/ " + bag_folder+"/"+str(lives_played))
                    
                    #for each value in the topic-json array, copy the json file to the current bag folder
                    for json in settings['topic-json'].values():
                        asTxt = json.split(".")[0] + ".txt"
                        print("Copying " + asTxt + " to " + bag_folder+"/"+str(lives_played))
                        os.system("cp ./airsim-ros/shared/src/"+asTxt+" " + bag_folder+"/"+str(lives_played))
                        #delete the temporary json file
                        #os.system("rm ./airsim-ros/shared/src/"+asTxt)
                        #os.system("rm ./airsim-ros/shared/src/"+json)

                    #delete the copy of the settings.yml file
                    os.system("docker exec -it airsim-ros rm /root/shared/src/settings.yml")

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



import sys
from shared.helper import *
import time
import os
import yaml

class Orchestrator(UnrealBridge):

    def __init__(self, status_file_path) -> None:

        super().__init__(status_file_path)

        self.lives_played = 0

        self.settings = {}

        #read yaml
        with open("./settings.yml", 'r') as file:
            try:
                self.settings = yaml.load(file, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

        self.bag_folder = "./bags/"+get_current_time()
        os.makedirs(self.bag_folder)
        for i in range(0, self.settings['num_simulations']):
            os.makedirs(self.bag_folder+"/"+str(i+1))

        self.ue_state = {}

        self.reset_ue_tags()

    def init_airsim(self):
        print(get_current_time(True) + " Starting AirSim")
        os.chdir("./airsim-ros")
        os.system("tmux new-window -t Sim:3 -n AirSim-Master './run.sh; exec bash';")
        os.chdir("..")

        os.chdir(self.bag_folder+"/"+str(self.lives_played+1))
        print(get_current_time(True) + 
              " Starting bagging info at " +
                self.bag_folder+"/"+str(self.lives_played+1))
        #get the array of key names from the topics dictionary
        topic_names = list(self.settings['topics'].keys())
        #include the names of the topics in the rosbag record command without comas
        topic_names = " ".join(topic_names)
        os.system("tmux new-window -t Sim:4 -n ROS-Bags 'rosbag record -O ros.bag "+
                  topic_names+
                  "; exec bash';")
        print(get_current_time(True) + " Started baggin info at " +
               self.bag_folder+"/"+str(self.lives_played+1))
        os.chdir("../../..")

    def kill_airsim(self):
        print(get_current_time(True) + " Closing AirSim window and extracting the ROS bag")

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
        
        os.chdir(self.bag_folder+"/"+str(self.lives_played))
        os.system("rosbag play ros.bag")
        os.chdir("../../..")

        #copy the contents of the temporary rgb/ folder to the current bag folder
        #traverser through the values of the topics dictionary and copy each folder to the current bag folder
        for folder in self.settings['topic-folder'].values():
            if folder != '.' and folder != '':
                print("Copying " + folder + " to " + self.bag_folder+"/"+str(self.lives_played))
                print("Number of files in " + folder + ": " + str(len(os.listdir("./airsim-ros/shared/src/"+folder))))
                os.system("cp -r ./airsim-ros/shared/src/"+folder+"/ " + self.bag_folder+"/"+str(self.lives_played))
        
        #for each value in the topic-json array, copy the json file to the current bag folder
        for json in self.settings['topic-json'].values():
            asTxt = json.split(".")[0] + ".txt"
            #check if the text file exists
            if os.path.exists("./airsim-ros/shared/src/"+asTxt):
                print("Copying " + asTxt + " to " + self.bag_folder+"/"+str(self.lives_played))
                os.system("cp ./airsim-ros/shared/src/"+asTxt+" " + self.bag_folder+"/"+str(self.lives_played))
                #renaming bback to the original json file name
                os.system("mv " + self.bag_folder+"/"+str(self.lives_played)+"/"+asTxt + " " + self.bag_folder+"/"+str(self.lives_played)+"/"+json)
            elif os.path.exists("./airsim-ros/shared/src/"+json):
                #move the json file to the current bag folder
                print("Copying " + json + " to " + self.bag_folder+"/"+str(self.lives_played))
                os.system("cp ./airsim-ros/shared/src/"+json+" " + self.bag_folder+"/"+str(self.lives_played))
        
        #copy decl.json to the current bag folder
        if os.path.exists("./airsim-ros/shared/src/decl.json"):
            print("Copying decl.json to " + self.bag_folder+"/"+str(self.lives_played))
            os.system("cp ./airsim-ros/shared/src/decl.json " + self.bag_folder+"/"+str(self.lives_played))

        #copy the log file to the current bag folder
        os.system("cp ./airsim-ros/shared/src/log_publisher.txt " + self.bag_folder+"/"+str(self.lives_played))
        os.system("cp ./airsim-ros/shared/src/log_extractor.txt " + self.bag_folder+"/"+str(self.lives_played))

        #delete the copy of the settings.yml file
        os.system("docker exec -it airsim-ros rm /root/shared/src/settings.yml")

        os.system("tmux kill-window -t ROS-Bags")
        os.system("tmux kill-window -t AirSim")
        os.system("docker stop /airsim-ros")

    def request_PIE_session(self):
        print(get_current_time(True) + 
                    "Letting the editor know to start the game")

        #send a message to the editor to start the game
        time.sleep(1)

        #NOTE: need to set this back to 0 once the play in editor session starts
        self.set_ue_condition_tag("play", 1) 

        #go to ./airsim-ros and run the run_test_square.sh script
        print(get_current_time(True) + 
                "AirSim status: " + str(self.settings['airsim']))
        
        if self.settings['airsim']:
                time.sleep(2)
                self.init_airsim()
                print("Now waiting for the game to start...")
    
    def stop_PIE_session(self):
        print(get_current_time(True) + "Telling the editor to stop the game")
        self.set_ue_condition_tag("stop", 1)

        print(get_current_time(True) + " Lives played in total so far: " + str(self.lives_played))

        time.sleep(2)
        self.set_ue_condition_tag("play", 0)

    def on_engine_ready(self):
        print(get_current_time(True) + 
                    "Unreal Editor is ready")
            
        if not self.is_requesting_play():
            time.sleep(3)
            self.request_PIE_session()
        
        elif self.is_engine_playing():
            if self.settings['play_time'] > 0:

                print(get_current_time(True) + " Playing for "
                       + str(self.settings['play_time']) +
                         " seconds")
                
                time.sleep(self.settings['play_time'])
                
                self.lives_played += 1

                if self.settings["airsim"]:
                    self.kill_airsim()
                    time.sleep(2)

                self.stop_PIE_session()
            else:
                '''
                    setting the play time to zero and less will
                    indicate that the user wants to handle the closing of life manually/externally
                '''
                while True:
                    continue

    def iterate(self):
        self.update_ue_state()

        if self.is_in_end_play():
            self.set_ue_condition_tag("end_play", 0)
            # self.kill_airsim()
            if self.lives_played >= self.settings['num_simulations'] and self.settings['num_simulations'] >= 1:
                os.system("./kill_all.sh")
        elif self.is_in_begin_play():
            print(get_current_time(True) + " Begin Play was trigerred")

        if self.is_engine_ready():
            self.on_engine_ready()

if __name__ == "__main__":
    orchestrator = Orchestrator(status_file_path="./shared/unreal.json",)

    while True:
        orchestrator.iterate()


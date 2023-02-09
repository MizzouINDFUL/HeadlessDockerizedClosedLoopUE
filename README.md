# HeadlessDockerizedClosedLoopUE

Prerquisites: 

 

    I was testing this out on a Ubuntu 20.04 machine 

    Docker - https://docs.docker.com/engine/install/ubuntu/ 

    Your Unreal project must have AirSim plugin in it 

    As of right now, we need the Unreal projects to be stored in the ~Documents/Unreal Projects directory. The name of the folder that contains the project must have the title of the that same project. For example, if your .uproject file is called Blocks.uproject, full path should be /home/username/Documents/Unreal Projects/Blocks/Blocks 

    You must provide the python script that will take the role of the controller during the simulation. The repo comes with a sample script called waypoint_lawnmower.py in the airsim-ros/shared/src/ directory. Your custom script should be located in the same directory 
     

 

Building containers: 

    Open username.txt and paste your github username 

    Open password.txt and paste your github token (NOT password). Make sure the github account you're using has access to Epic's official Unreal Engine repo 

    Open terminal and navigate to the Unreal Container project folder 

    Run ./build.sh* 
    *In case you get a "Docker permission denied" error: 

    https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue 

    Note that you may need to restart your machine for it to fix the problem 

 

Running the simulation: 

  run ./start.sh from repo's root directory. Provide to arguments:  

  Project name and the name of the python script that will be the "Controller" in your simulation.  

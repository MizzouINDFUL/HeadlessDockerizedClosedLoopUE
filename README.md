# Headless Dockerized Closed Loop UE
This will run your Unreal project with AirSim plugin in it multiple times, bag the ROS topics, and then store all that data for each simulation

### Prerequisites
+ **Ubuntu 20.04** seemed to be the most stable for this project so far
+ **[Docker](https://docs.docker.com/engine/install/ubuntu/)** 
+ **[Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)**
+ A machine that is capable of running Unreal Engine and has all the drivers installed for it

### Your Unreal Engine project must
+ have AirSim plugin installed
+ be a c++ project

## Building
1. Enter you GitHub username in username.txt. Be sure that your account has access to Unreal Engine's repo
2. Enter yout GitHub token. To get your token, go to Settings->Developer settings->Personal access tokens->Tokens(classic)
3. Run ./build.sh

### Known issues when building
Sometimes you may get a "Docker permission denied" error. A fix to that is described [here](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue). Note that you might have to restart your machine to apply the fix.

## Running
1. Provide the path to your project in *project_path* in settings.yml file
2. You may want to tweak any other parameters. For example if you just want to run Unreal externally from your machine, you may set *use_ue_docker* to false and provide path to your engine folder in *custom_ue_path*
3. Run ./start.sh

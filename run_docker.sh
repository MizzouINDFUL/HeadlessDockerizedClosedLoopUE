docker stop unreal; docker rm unreal
docker run --gpus all -ti -d -v /python:/python -v /shared:/shared  -v /home/$USER/Documents/Unreal\ Projects/$1/:/project/ --net=host --pid=host -u=ue4  --name unreal ghcr.io/epicgames/unreal-engine:dev-4.27.0 /bin/bash
docker start unreal
docker exec -w /python/ unreal python3 add_unreal_ed.py $1
docker exec -w /python/ unreal python3 create_code_dirs.py $1
docker exec -w /python/ unreal python3 fix_api_name.py $1
docker exec unreal /home/ue4/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono /home/ue4/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/project/$1.uproject -TargetType=Editor -Progress
docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor /project/$1.uproject -ExecutePythonScript="start_controller.py" -game -windowed -RenderOffscreen

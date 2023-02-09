SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo $SCRIPTPATH

PROJECTUPPER=${1^^}
PROJECTAPI="${PROJECTUPPER}_API"

docker run --gpus all -ti -d -v $SCRIPTPATH/python/:/python -v $SCRIPTPATH/shared:/shared  -v /home/$USER/Documents/Unreal\ Projects/$1/:/project/ --net=host --pid=host -u=ue4  --name unreal ghcr.io/epicgames/unreal-engine:dev-4.27 /bin/bash
docker start unreal

docker exec -w /python/ unreal cp -u 'MindfulLib.h' "/project/Source/$1/Public"
docker exec -w /python/ unreal cp -u 'MindfulLib.cpp' "/project/Source/$1/Private"
docker exec -w /python/ unreal cp -u 'settings.json' "/home/ue4/Documents/AirSim"
docker exec -w /python/ unreal cp -u 'settings.json' "/root/Documents/AirSim"
cp $SCRIPTPATH/dev/monitor.py $SCRIPTPATH/python/
docker exec -w /python/ unreal cp -u 'monitor.py' "/home/ue4/UnrealEngine/Engine/Binaries/Linux/"
docker exec -w /project/Source/$1/Public/ unreal cat "MindfulLib.h"
docker exec -w /project/Source/$1/Public/ unreal sed -i "s/PROJECT_API/$PROJECTAPI/" "MindfulLib.h"
docker exec -w /project/Source/$1/Public/ unreal cat "MindfulLib.h"
docker exec -w /project/ unreal mkdir -p "/project/Content/Python"
#docker exec -w /python/ unreal cp -u 'init_unreal.py' "/project/Content/Python"

docker exec unreal /home/ue4/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono /home/ue4/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/project/$1.uproject -TargetType=Editor -Progress
docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$1.uproject -game -RenderOffscreen

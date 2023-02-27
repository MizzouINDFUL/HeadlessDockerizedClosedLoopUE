PROJECTPATH=$1
DIR=${PROJECTPATH%/*}
PROJECTNAME=$(basename "$1" .uproject)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECTUPPER=${PROJECTNAME^^}
PROJECTAPI="${PROJECTUPPER}_API"

docker run --gpus all -ti -d -v $SCRIPTPATH/python/:/python -v $SCRIPTPATH/shared:/shared  -v "$DIR":/project/ --net=host --pid=host -u=ue4 --name unreal ghcr.io/epicgames/unreal-engine:dev-4.27 /bin/bash
docker start unreal

if [ $2 == true ]; then
	docker exec -w /python/ unreal cp -u 'MindfulLib.h' "/project/Source/$PROJECTNAME/Public"
	docker exec -w /python/ unreal cp -u 'MindfulLib.cpp' "/project/Source/$PROJECTNAME/Private"
	docker exec -w /project/Source/$PROJECTNAME/Public/ unreal sed -i "s/PROJECT_API/$PROJECTAPI/" "MindfulLib.h"
fi

docker exec -w /python/ unreal cp -u 'settings.json' "/home/ue4/Documents/AirSim"
docker exec -w /python/ unreal cp -u 'settings.json' "/root/Documents/AirSim"
cp $SCRIPTPATH/dev/monitor.py $SCRIPTPATH/python/
docker exec -w /python/ unreal cp -u 'monitor.py' "/home/ue4/UnrealEngine/Engine/Binaries/Linux/"

if [ $3 == true ]; then
	docker exec -w /project/ unreal mkdir -p "/project/Content/Python"
	docker exec -w /python/ unreal cp -u 'init_unreal.py' "/project/Content/Python"
fi

docker exec unreal /home/ue4/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono /home/ue4/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/project/$PROJECTNAME.uproject -TargetType=Editor -Progress
if [ $4 == 1 ]; then
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -game -RenderOffscreen
else
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -RenderOffscreen
fi

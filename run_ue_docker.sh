PROJECTPATH=$1
DIR=${PROJECTPATH%/*}
PROJECTNAME=$(basename "$1" .uproject)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECTUPPER=${PROJECTNAME^^}
PROJECTAPI="${PROJECTUPPER}_API"
MODIFIERSCRIPT=$5
#get the name of the modifier script
MODIFIERSCRIPTNAME=$(basename "$5")

docker run --gpus all -ti -d -v $SCRIPTPATH/python/:/python -v $SCRIPTPATH/shared:/shared  -v "$DIR":/project/ --net=host --pid=host -u=ue4 --name unreal ghcr.io/epicgames/unreal-engine:dev-4.27 /bin/bash
docker start unreal

if [ $2 == true ]; then

	#if /project/Plugins/MindfulPlugin exists, delete it
	if [ -d "$DIR/Plugins/MindfulPlugin" ]; then
		echo "Deleting old MindfulPlugin..."
		rm -rf $DIR/Plugins/MindfulPlugin
	fi

	docker exec -w /python/ unreal cp -r -u 'MindfulPlugin' "/project/Plugins"
fi

docker exec -w /python/ unreal cp -u 'settings.json' "/home/ue4/Documents/AirSim"

echo "Compiling project..."

docker exec unreal /home/ue4/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono /home/ue4/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/project/$PROJECTNAME.uproject -TargetType=Editor -Progress
if [ $4 == 1 ]; then
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -game -RenderOffscreen
else
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -RenderOffscreen
fi


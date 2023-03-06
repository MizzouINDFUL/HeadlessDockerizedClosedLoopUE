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

	#if the Source folder inside /project/ doesn't exist, copy it from the template
	if [ ! -d "$DIR/Source" ]; then
		echo "This is a Blueprint-only project. Converting to C++..."

		cp -r $SCRIPTPATH/python/Source $SCRIPTPATH/shared/Source

		docker exec -w /project/ unreal cp -r /shared/Source .

		rm -rf $SCRIPTPATH/shared/Source

		echo "Copied Source folder from template. Renaming files..."

		#rename the Project folder to the project name
		docker exec -w /project/ unreal mv "Source/Project" "Source/$PROJECTNAME"

		#rename PROJECT.Target.cs to the project name
		docker exec -w /project/ unreal mv "Source/Project.Target.cs" "Source/$PROJECTNAME.Target.cs"

		#create a varialbe that has Editor at the end of the project name
		EDITORNAME="$PROJECTNAME""Editor"

		#rename ProjectEditor.Target.cs to the project name
		docker exec -w /project/ unreal mv "Source/ProjectEditor.Target.cs" "Source/$EDITORNAME.Target.cs"

		docker exec -w /project/ unreal mv "Source/$PROJECTNAME/Project.Build.cs" "Source/$PROJECTNAME/$PROJECTNAME.Build.cs"

		docker exec -w /project/ unreal mv "Source/$PROJECTNAME/Project.cpp" "Source/$PROJECTNAME/$PROJECTNAME.cpp"

		docker exec -w /project/ unreal mv "Source/$PROJECTNAME/Project.h" "Source/$PROJECTNAME/$PROJECTNAME.h"

		echo "Renamed files. Renaming variables..."

		#rename every mention of Project inside the files to the project name
		docker exec -w /project/ unreal sed -i "s/Project/$PROJECTNAME/g" "Source/$PROJECTNAME/$PROJECTNAME.Build.cs"
		docker exec -w /project/ unreal sed -i "s/Project/$PROJECTNAME/g" "Source/$PROJECTNAME/$PROJECTNAME.cpp"
		docker exec -w /project/ unreal sed -i "s/Project/$PROJECTNAME/g" "Source/$PROJECTNAME/$PROJECTNAME.h"
		docker exec -w /project/ unreal sed -i "s/Project/$PROJECTNAME/g" "Source/$PROJECTNAME.Target.cs"
		docker exec -w /project/ unreal sed -i "s/Project/$PROJECTNAME/g" "Source/$EDITORNAME.Target.cs"
	fi

	echo "Adding MindfulLib to project..."
	docker exec -w /python/ unreal cp -u 'MindfulLib.h' "/project/Source/$PROJECTNAME/Public"
	docker exec -w /python/ unreal cp -u 'MindfulLib.cpp' "/project/Source/$PROJECTNAME/Private"
	docker exec -w /project/Source/$PROJECTNAME/Public/ unreal sed -i "s/PROJECT_API/$PROJECTAPI/" "MindfulLib.h"
fi

docker exec -w /python/ unreal cp -u 'settings.json' "/home/ue4/Documents/AirSim"

if [ $3 == true ]; then
	echo "Adding Python to project..."
	docker exec -w /project/ unreal mkdir -p "/project/Content/Python"
	docker exec -w /python/ unreal cp -u 'init_unreal.py' "/project/Content/Python"
	#copy the modifier script to the project
	docker exec -w /python/ unreal cp -u $MODIFIERSCRIPTNAME "/project/Content/Python"
	#replace MODIFIERSCRIPTNAME with the name of the modifier script inside init_unreal.py
	docker exec -w /project/Content/Python/ unreal sed -i "s/MODIFIERSCRIPTNAME/$MODIFIERSCRIPTNAME/" "init_unreal.py"
	echo "init_unreal.py was copied to /project/Content/Python"
fi

echo "Compiling project..."

docker exec unreal /home/ue4/UnrealEngine/Engine/Binaries/ThirdParty/Mono/Linux/bin/mono /home/ue4/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Linux -Project=/project/$PROJECTNAME.uproject -TargetType=Editor -Progress
if [ $4 == 1 ]; then
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -game -RenderOffscreen
else
	docker exec -it -w /home/ue4/UnrealEngine/Engine/Binaries/Linux/ unreal ./UE4Editor-Cmd /project/$PROJECTNAME.uproject -RenderOffscreen
fi


// Fill out your copyright notice in the Description page of Project Settings.


#include "MindfulLib.h"

 	
#include "Settings/LevelEditorPlaySettings.h"
#include "Editor/UnrealEdEngine.h"
#include "Editor/EditorEngine.h"
#include "UnrealEdGlobals.h"
#include "Editor/UnrealEd/Public/Editor.h"

//Stop the Unreal Play In Editor session
float UMindfulLib::StopLife(){
    GUnrealEd->RequestEndPlayMap();
    return -1.0;
}

float UMindfulLib::StartLife(){

    FRequestPlaySessionParams sessionParameters;

    GUnrealEd->RequestPlaySession(sessionParameters);

    //Start Unreal Play In Editor session in the current viewport
    //sessionParameters.ViewportType = ELevelViewportType::LVT_Perspective;

    return 1.0;
}





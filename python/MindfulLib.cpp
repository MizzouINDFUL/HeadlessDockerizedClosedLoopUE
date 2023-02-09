// Fill out your copyright notice in the Description page of Project Settings.


#include "MindfulLib.h"

 	
#include "Settings/LevelEditorPlaySettings.h"
#include "Editor/UnrealEdEngine.h"
#include "Editor/EditorEngine.h"
#include "UnrealEdGlobals.h"
#include "Editor/UnrealEd/Public/Editor.h"


float UMindfulLib::StopLife(){

    if(GEditor){
        UWorld* World = GEditor->GetEditorWorldContext().World();
        if(World){
            GEditor->Exec( World, TEXT( "QUIT_EDITOR" ) );
        }
    }

    return -1.0;
}

float UMindfulLib::StartLife(){
    // if(GEditor){
    //     UWorld* World = GEditor->GetEditorWorldContext().World();
    //     if(World){
    //         GEditor->
    //     }
    // }

    //FLevelEditorModule& LevelEditorModule = FModuleManager::Get().GetModuleChecked<FLevelEditorModule>(TEXT("LevelEditor"));



    //ULevelEditorPlaySettings* playSettings =  GetMutableDefault<ULevelEditorPlaySettings>();

    //playSettings->SetPlayNumberOfClients(1);

    //playSettings->SetPlayNetMode(EPlayNetMode::PIE_Standalone);



    FRequestPlaySessionParams sessionParameters;

    //sessionParameters.DestinationSlateViewport = LevelEditorModule.GetFirstActiveViewport();//sets the server viewport in there. Otherwise, a window is created for the server.

    //sessionParameters.EditorPlaySettings = playSettings;	

    GUnrealEd->RequestPlaySession(sessionParameters);
    //UE_LOG(LogTemp, Error, TEXT("%s"), *FString("c++ function"))
    return 1.0;
}





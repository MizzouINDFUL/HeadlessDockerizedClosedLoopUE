// Fill out your copyright notice in the Description page of Project Settings.


#include "MindfulLib.h"
#include "Kismet/GameplayStatics.h"

#include "Settings/LevelEditorPlaySettings.h"
#include "Editor/UnrealEdEngine.h"
#include "Editor/EditorEngine.h"
#include "UnrealEdGlobals.h"
#include "Editor/UnrealEd/Public/Editor.h"

#include "MindfulNotifier.h"


void UMindfulLib::AddNotifier(UObject* WorldContext)
{
    //Check if there is already an instance of the actor
    TArray<AActor*> FoundActors;
    UGameplayStatics::GetAllActorsOfClass(WorldContext, AMindfulNotifier::StaticClass(), FoundActors);
    if (FoundActors.Num() > 0)
    {
        return;
    }

    //Spawn the AMindfulNotifier actor
    UWorld* World = GEngine->GetWorldFromContextObject(WorldContext);
    FActorSpawnParameters SpawnParams;
    World->SpawnActor<AMindfulNotifier>(SpawnParams);
}

//Stop the Unreal Play In Editor session
void UMindfulLib::StopLife(){
    GUnrealEd->RequestEndPlayMap();
}

void UMindfulLib::StartLife(){
    FRequestPlaySessionParams sessionParameters;

    GUnrealEd->RequestPlaySession(sessionParameters);
}


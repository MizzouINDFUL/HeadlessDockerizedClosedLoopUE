// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "MindfulLib.generated.h"

/**
 * 
 */
UCLASS()
class PROJECT_API UMindfulLib : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	
	public:

	UFUNCTION(BlueprintCallable, Category="MINDFUL")
	static float StartLife();

	UFUNCTION(BlueprintCallable, Category="MINDFUL")
	static float StopLife();
	
	
};

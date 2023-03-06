// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Project : ModuleRules
{
    public Project(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        bEnableExceptions = true; // win64
        if (Target.Platform == UnrealTargetPlatform.Linux)
            bEnableExceptions = false;
        PublicDependencyModuleNames.AddRange(new string[] { "UnrealEd", "Core", "CoreUObject", "Engine", "InputCore" });
    }
}

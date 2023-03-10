// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class ProjectEditorTarget : TargetRules
{
	public ProjectEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		ExtraModuleNames.AddRange(new string[] { "Project" });
        DefaultBuildSettings = BuildSettingsVersion.V2;
        //bUseUnityBuild = false;
        //bUsePCHFiles = false;
    }
}

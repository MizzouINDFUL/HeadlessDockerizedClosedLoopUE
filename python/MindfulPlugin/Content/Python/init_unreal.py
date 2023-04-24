import sys
import os

'''
    yes, this is ugly
'''
if os.path.exists("/shared"):
    sys.path.append("/shared")
if os.path.exists("/home/ue4/UnrealEngine/Engine/Binaries/Linux"):
    sys.path.append("/home/ue4/UnrealEngine/Engine/Binaries/Linux")
elif os.path.exists("./shared"):
    sys.path.append("./shared")
if os.path.exists("/usr/lib/python3/dist-packages"):
    sys.path.append("/usr/lib/python3/dist-packages")

import unreal
import helper
from helper import UnrealBridge
import time

class MindfulUE(UnrealBridge):
    def __init__(self, status_file_path="/shared/unreal.json") -> None:
        super().__init__(status_file_path)
        print("MindfulUE initialized")
        unreal.MindfulLib.add_notifier(unreal.EditorLevelLibrary.get_editor_world())
        #this name will adjusted extetnally
        #if it's set to just "modifier script name", we asuume there is no modifier script
        self.mod_script_name = "MODIFIERSCRIPTNAME"
        print("binding tick callback")
        tickHandle = unreal.register_slate_pre_tick_callback(self.testRegistry)
    
    def run_level_modifier(self):
        if self.mod_script_name != "MODIFIER"+"SCRIPTNAME": 
            unreal.SystemLibrary.execute_console_command(None,"py " + self.mod_script_name)

    def tick(self, deltaTime):

        if self.is_in_begin_play():
            self.set_ue_condition_tag("end_play", 0)
        elif self.is_in_end_play():
            self.set_ue_condition_tag("begin_play", 0)

        if not self.is_engine_playing():
            self.set_ue_condition_tag("ready", 1)

            # self.run_level_modifier()
    
        if self.is_requesting_play() and not self.is_engine_playing():
            self.set_ue_condition_tag("playing", 1)

            unreal.log_warning("Starting PIE session...")
            unreal.MindfulLib.start_life()
        if self.is_requesting_stop():
            self.reset_ue_tags()

            unreal.log_warning("Life ended. Stopping PIE session...")
            unreal.MindfulLib.stop_life()

    def testRegistry(self, deltaTime):
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        if asset_registry.is_loading_assets():
            unreal.log_warning("still loading...")
        else:
            self.update_ue_state()
            self.tick(deltaTime)

            

MindfulUE()

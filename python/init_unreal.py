import unreal 
import os
import time

tickhandle = None
 
def testRegistry(deltaTime):
    
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if asset_registry.is_loading_assets():
        unreal.log_warning("still loading...")
    else:
        if os.path.isfile("ready.txt"):
            unreal.log_warning("ready!")
            time.sleep(2)
            unreal.MindfulLib.start_life()
            unreal.log_warning("startingPIE")
            os.remove("ready.txt")
        else:
            return
            #unreal.log_warning(os.getcwd())
        
        if os.path.isfile("stop.txt"):
            unreal.MindfulLib.stop_life()
            unreal.SystemLibrary.execute_console_command(None,"py tweak_param.py")
            os.remove("stop.txt")
 
print("starting unreal python contorller")
tickhandle = unreal.register_slate_pre_tick_callback(testRegistry)

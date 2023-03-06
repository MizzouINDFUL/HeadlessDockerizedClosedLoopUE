import unreal
import os
import socket
import time

is_playing = False
tickhandle = None

def testRegistry(deltaTime):

    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if asset_registry.is_loading_assets():
        unreal.log_warning("still loading...")
    else:

        #send the ready signal if playing.txt does not exist
        if not os.path.exists("/shared/playing.txt"):
            os.system("touch /shared/ready.txt")
            unreal.SystemLibrary.execute_console_command(None,"py MODIFIERSCRIPTNAME")

        if os.path.exists("/shared/play.txt") and not os.path.exists("/shared/playing.txt"):
            # is_playing = True
            #create file to signal that the editor is ready to play
            os.system("touch /shared/playing.txt")

            unreal.log_warning("Starting PIE session...")
            unreal.MindfulLib.start_life()
        if os.path.exists("/shared/stop.txt"):
            # is_playing = False
            #deleting "playing.txt" file to signal that the editor is not playing anymore
            if os.path.exists("/shared/playing.txt"):
                os.remove("/shared/playing.txt")
            if os.path.exists("/shared/stop.txt"):
                os.remove("/shared/stop.txt")
            #if os.path.exists("/shared/play.txt"):
                #os.remove("/shared/play.txt")
            if os.path.exists("/shared/ready.txt"):
                os.remove("/shared/ready.txt")

            unreal.log_warning("Life ended. Stopping PIE session...")
            unreal.MindfulLib.stop_life()

            #executing the python script to modify the parameters
            unreal.SystemLibrary.execute_console_command(None,"py " + modifier_script)
            #unreal.SystemLibrary.execute_console_command(None,"py tweak_param.py")

print("starting unreal python contorller")

tickhandle = unreal.register_slate_pre_tick_callback(testRegistry)


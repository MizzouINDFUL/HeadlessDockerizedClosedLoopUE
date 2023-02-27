import unreal 
import os
import socket
import time

is_playing = False
tickhandle = None

s = socket.socket()
host = '127.0.0.1'
port = 12345

s.connect((host,port))
 
def testRegistry(deltaTime):
    
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if asset_registry.is_loading_assets():
        unreal.log_warning("still loading...")
    else:

        #send the ready signal if playing.txt does not exist
        if not os.path.exists("playing.txt"):
            s.send(b'ready')

        data = s.recv(1024)
        ue_status = data.decode()
        unreal.log_warning(f"Received data: {ue_status}")

        time.sleep(3)
        if ue_status == 'play' and not os.path.exists("playing.txt"):
            # is_playing = True
            #create file to signal that the editor is ready to play
            f = open("playing.txt","w+")
            unreal.MindfulLib.start_life()
        if ue_status == 'stop':
            # is_playing = False
            #deleting "playing.txt" file to signal that the editor is not playing anymore
            os.remove("playing.txt")
            unreal.MindfulLib.stop_life()
            time.sleep(3)
            #unreal.SystemLibrary.execute_console_command(None,"py tweak_param.py")
 
print("starting unreal python contorller")

tickhandle = unreal.register_slate_pre_tick_callback(testRegistry)

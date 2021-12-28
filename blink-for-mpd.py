
import mpd
import os

BLINK = "/usr/local/bin/blink"


# get MPD status
client = mpd.MPDClient()
client.connect(host="localhost", port=6600)
status = client.status()
client.disconnect()




# blink as needed
if status["state"] == "play":
    os.system(f"{BLINK} blue on")
else:
    os.system(f"{BLINK} green on")


    

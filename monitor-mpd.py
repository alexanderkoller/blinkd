
import mpd
import os
import time
import logging
import sys

### Set up logging

LOGFILE_NAME = "/var/log/mpd-blinkd"
os.makedirs(os.path.dirname(LOGFILE_NAME), exist_ok=True)
logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")



BLINK = "/usr/local/bin/blink"
trying_to_reconnect = False

def refresh_status():
    # get MPD status
    status = client.status()
            
    # blink as needed
    new_state = status["state"]
    logging.debug(f"State changed to '{new_state}'")
            
    if new_state == "play":
        os.system(f"{BLINK} blue on")
    else:
        os.system(f"{BLINK} green on")    


logging.info("")        
logging.info(f"Starting mpd-blink ...")
        
while True:
    try:
        # set up connection
        client = mpd.MPDClient()
        client.connect(host="localhost", port=6600)
        
        logging.info(f"Connected to MPD.")

        # On first startup, let's not set the LED; this is the job of the
        # Phoniebox startup script. We only want to refresh the LED if
        # we temporarily lost the connection to MPD (because of a library scan).
        if trying_to_reconnect:
            refresh_status()
            trying_to_reconnect = False

        # respond to state changes in mpd
        while True:
            # wait for state change
            subsystems = client.idle()
            logging.debug(f"Idle returned {subsystems}; status is {client.status()}")
            
            if "player" in subsystems:
                refresh_status()

    except (mpd.base.ConnectionError, ConnectionRefusedError):
        if not trying_to_reconnect:
            os.system(f"{BLINK} green blink")
            logging.info(f"Lost connection to mpd, trying to reconnect ...")
            trying_to_reconnect = True
        
        logging.debug(f"Still trying to reconnect ...")
        time.sleep(0.5)

    except BaseException as err:
        logging.error(f"Unexpected exception ({type(err)}: {err}, terminating.")
        sys.exit(1)



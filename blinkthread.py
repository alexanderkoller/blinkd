import os
import sys
import time
from queue import Queue, Empty
from threading import Thread

import board
import neopixel
import logging

### Set up logging

LOGFILE_NAME = "/var/log/blinkd"
os.makedirs(os.path.dirname(LOGFILE_NAME), exist_ok=True)
logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


pixels = neopixel.NeoPixel(board.D12, 16)

frames_per_second = 16
frame_duration = 1.0/16  # in ms

GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (200,0,0)
OFF = (0,0,0)

programs = {
    "off": [(OFF, sys.maxsize)]
}

color_names = {"green": GREEN, "red": RED, "blue": BLUE}

for color in ["green", "red", "blue"]:
    programs[f"{color} off"] = programs["off"]
    programs[f"{color} on"] = [(color_names[color], sys.maxsize)]
    programs[f"{color} blink"] = [(color_names[color], 8), (OFF, 8)]


on_off_state = {"red": "off"}


class BlinkThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.change_program("green blink")

    def change_program(self, new_program):
        self.program = new_program
        self.step = 0
        self.frame = -1
        self.have_new_program = True

    def run(self):
        while True:
            if self.have_new_program:
                logging.info(f"New program: {self.program}")
                
                instruction_changed = True
                self.have_new_program = False

                parts = self.program.split()
                if len(parts) == 2:
                    color = parts[0]
                    command = parts[1]

                    if command == "on" or command == "off":
                        on_off_state[color] = command

                    elif command == "toggle":
                        old_state = on_off_state.get(color) or "off"
                        new_state = "on" if old_state == "off" else "off"
                        on_off_state[color] = new_state
                        self.program = f"{color} {new_state}"
                        logging.info(f"Rewrote toggle to {self.program}")

                    else:
                        on_off_state[color] = "off"
            else:
                instruction_changed = False

            if not self.program in programs:
                logging.warning(f"Undefined program: {self.program}")
            else:
                current_program = programs[self.program]
                current_instruction = current_program[self.step]

                # step one frame forward
                self.frame += 1
                if self.frame == current_instruction[1]:
                    # step one instruction forward
                    instruction_changed = True
                    self.step += 1
                    if self.step == len(current_program):
                        self.step = 0
                    self.frame = 0

                # if instruction changed, update the LEDs
                if instruction_changed:
                    current_instruction = current_program[self.step]
                    logging.debug(f"New instruction: {current_instruction}")
                    pixels.fill(current_instruction[0])

            time.sleep(frame_duration)


logging.info("")
logging.info("Starting blinkd ...")

            
bt = BlinkThread()
bt.start()

logging.info("Running.")


FIFO = '/run/blinkd'
if os.path.exists(FIFO):
    os.remove(FIFO)
os.mkfifo(FIFO)
os.chmod(FIFO, 0o666)

try:
    while True:
        with open(FIFO) as fifo:
            for line in fifo:
                logging.debug(f"Read: {line}")
                cmd = line.strip() #.split()
                bt.change_program(cmd) #cmd[1], cmd[0])
finally:
    logging.info("Shutdown")





import os
import sys
import time
from queue import Queue, Empty
from threading import Thread

import board
import neopixel

pixels = neopixel.NeoPixel(board.D21, 16)

frames_per_second = 16
frame_duration = 1.0/16  # in ms

GREEN = (0,80,0)
BLUE = (0,0,60)
RED = (200,0,0)
OFF = (0,0,0)

programs = {
    "green blink": [(GREEN, 8), (OFF, 8)],
    "red blink": [(RED, 8), (OFF, 8)],
    "blue blink": [(BLUE, 8), (OFF, 8)],
    "off": [(OFF, sys.maxsize)]
}

programs["green off"] = programs["off"]
programs["blue off"] = programs["off"]
programs["red off"] = programs["off"]

# colors = {
#     "green": GREEN,
#     "blue": BLUE,
#     "red": RED
# }


class BlinkThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        # self.queue = Queue()
        self.change_program("green blink")

    def change_program(self, new_program): #, new_color):
        # self.queue.put(new_program)
        self.program = new_program
        # self.color = colors[new_color]
        self.step = 0
        self.frame = -1
        self.have_new_program = True

    def run(self):
        while True:
            if self.have_new_program:
                instruction_changed = True
                self.have_new_program = False
            else:
                instruction_changed = False

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
                pixels.fill(current_instruction[0])
                # intensity = current_instruction[0]
                # r, g, b = self.color[0]*intensity, self.color[1]*intensity, self.color[2]*intensity
                # pixels.fill((r,g,b))

            time.sleep(frame_duration)


bt = BlinkThread()
bt.start()


FIFO = '/tmp/neoblink'
if os.path.exists(FIFO):
    os.remove(FIFO)
os.mkfifo(FIFO)
os.chmod(FIFO, 0o666)

while True:
    with open(FIFO) as fifo:
        for line in fifo:
            print(line)
            cmd = line.strip() #.split()
            bt.change_program(cmd) #cmd[1], cmd[0])




# red blink
# green on
# green off

import os
import time
from gpiozero import LED

led_dict = {"green": LED(5)}


FIFO = '/tmp/blink'
if os.path.exists(FIFO):
    os.remove(FIFO)
os.mkfifo(FIFO)

while True:
    with open(FIFO) as fifo:
        for line in fifo:
            print(line)
            cmd = line.strip().split()
            led = led_dict[cmd[0]]

            if cmd[1] == "on":
                led.on()
            elif cmd[1] == "off":
                led.off()
            elif cmd[1] == "blink":
                led.blink()


# import platform
# import gpiozero
#
# from time import sleep
# from gpiozero import LED
#
# led = LED(5)
# led.blink()
#
# for i in range(5):
#     print("hello")
#     sleep(1)
#
# led.off()
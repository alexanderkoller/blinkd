import time

import board
import neopixel

pixels = neopixel.NeoPixel(board.D21, 16)

GREEN = (0,40,0)
BLUE = (0,0,60)
BLACK = (0,0,0)

even_pixels = [2*x for x in range(8)]
odd_pixels = [2*x+1 for x in range(8)]

def fill_pixels(pixel_list, color):
    for pixel in pixel_list:
        pixels[pixel] = color

#
# for i in range(10):
#     fill_pixels(even_pixels, GREEN)
#     fill_pixels(odd_pixels, BLACK)
#
#     time.sleep(0.5)
#
#     fill_pixels(odd_pixels, GREEN)
#     fill_pixels(even_pixels, BLACK)
#
#     time.sleep(0.5)



for i in range(10):
    pixels.fill(GREEN)
    time.sleep(0.5)
    pixels.fill(BLACK)
    time.sleep(0.5)

pixels.fill(BLACK)

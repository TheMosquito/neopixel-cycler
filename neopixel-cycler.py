# Set a NeoPixel to a color specified in the environment, and blink it.

import time
import board
import os
import sys

# Set the appropriate neopixel count for your pixel strip
NUM_PIXELS = 1

# Get configuration from the environment, or set a default value if not there
def get_from_env(v, d):
  if v in os.environ and '' != os.environ[v]:
    return os.environ[v]
  else:
    return d
ARCH = get_from_env('ARCH', '')

# Different libraries for Raspberry Pi and NVIDIA Jetson
if ARCH == 'arm64':
  # NVIDIA Jetson device with SPI0 enabled and with the Neopixel control wire
  # attached to Jetson GPIO pin 19 (SPI0 MOSI)
  import busio
  import neopixel_spi as neopixel
  spi = board.SPI()
  PIXEL_ORDER = neopixel.RGB
  pixels = neopixel.NeoPixel_SPI(spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False)
elif ARCH == 'arm':
  # Raspberry Pi with NeoPixel control wire attached to Pi GPIO board.D18
  import neopixel
  RASPBERRY_PI_GPIO = board.D18
  pixels = neopixel.NeoPixel(RASPBERRY_PI_GPIO, NUM_PIXELS)
else:
  print("%s: unsupported architecture: \"%s\"" % (sys.argv[0], ARCH))
  sys.exit(1)

# Returns a color number from a rainbow wheel
def wheel(pos):
  if pos < 0 or pos > 255:
    r = g = b = 0
  elif pos < 85:
    r = int(pos * 3)
    g = int(255 - pos * 3)
    b = 0
  elif pos < 170:
    pos -= 85
    r = int(255 - pos * 3)
    g = 0
    b = int(pos * 3)
  else:
    pos -= 170
    r = 0
    g = int(pos * 3)
    b = int(255 - pos * 3)
  return (r / 8, g / 8, b / 8)

# Loop forever displaying the rotating rainbow, crashing optionally :-)
DO_CRASH = False
while True:
  for k in range(10):
    for j in range(255):
      for i in range(NUM_PIXELS):
        pixel_index = (i * 256 // NUM_PIXELS) + j
        pixels[i] = wheel(pixel_index & 255)
      pixels.show()
      if DO_CRASH:
        time.sleep(0.001)
      else:
        time.sleep(0.01)
  if DO_CRASH:
    # Turn off the pixels, then deliberately crash
    for i in range(NUM_PIXELS):
      pixels[i] = 0
    pixels.show()
    time.sleep(2.0)
    sys.exit(-1)

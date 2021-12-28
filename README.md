# Blink daemon for Raspberry Pi

This is a service for blinking a [Neopixel LED ring](https://www.adafruit.com/product/1586) (or compatible device) with a Raspberry Pi.

## Usage

Once blinkd is running, you can e.g. make the Neopixel ring blink in green with the following command:

```
blink green blink
```

The first argument to `blink` is the color; the second is the mode. Acceptable colors are `green`, `blue`, and `red`; acceptable modes are `on`, `off`, and `blink`. You can add other colors and modes by editing `blinkthread.py`.

You may want to copy `blink` to a convenient location, such as `/usr/local/bin`.

## Usage with MPD

Blinkd can monitor the behavior of [MPD](https://www.musicpd.org/) (or a compatible service, such as [Mopidy](https://mopidy.com/)) and change the LED ring in response to changes in MPD's state.

The script `monitor-mpd.py` will turn the LED ring to solid blue if MPD is playing a track, and solid green otherwise. If the script loses its connection to MPD (e.g. because you have stopped it to rescan the library), the LED ring will blink green until the connection is reestablished.


## System services

The cleanest way to run blinkd is with a system service.

Edit the `WorkingDirectory` and `ExecStart` entries in `etc/blinkd.service` to match the directory to which you have checked out this repository (same for `mpd-blinkd.service`). Then copy the service files from the `etc` directory into `etc/systemd/system` on your system. Finally, enable the services as follows:

```
sudo systemctl daemon-reload
sudo systemctl enable blinkd
sudo systemctl enable mpd-blinkd # if you want it
```

This will start the services every time you boot the Raspberry Pi. Logging information will be written into `/var/log/blinkd` and `/var/log/mpd-blinkd`, respectively.


## Configuration

By default, blinkd assumes that you have connected the DI pin of your LED ring to GPIO 12 on your Raspberry Pi, and that your LED ring contains 16 LEDs. You can change this by editing the line

```
pixels = neopixel.NeoPixel(board.D12, 16)
```

in `blinkthread.py`.

You will also have to supply the LED ring with power (GND and 5V). See the [official documentation](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring) for details. Note that the DI pin of the Neopixel must be connected to GPIO 10, GPIO 12, GPIO 18 or GPIO 21.


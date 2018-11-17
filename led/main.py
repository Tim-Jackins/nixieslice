from neopixel import *
from datetime import datetime
from pytz import timezone
from os import stat
from time import sleep
from yaml import load

# LED strip configuration:
# LED_PIN = 10 # (10 uses SPI /dev/spidev0.0).

LED_COUNT = 60          # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # set to '1' for GPIOs 13, 19, 41, 45 or 53

#configFile = '../web/sample.yml'
configFile = 'sample.yml'
configYaml = open(configFile, "r")
config = load(configYaml)
timeSinceChange = stat(configFile)[9]


def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        sleep(.05)


def formatTime(hour, minute, second):
    fullTime = ''
    fullTime += str(hour) if len(str(hour)) == 2 else '0' + str(hour)
    fullTime += str(minute) if len(str(minute)) == 2 else '0' + str(minute)
    fullTime += str(second) if len(str(second)) == 2 else '0' + str(second)
    return fullTime


def update(config):
    tz = config['TZ'].replace(' ', '_')
    tz_now = datetime.now(timezone(tz))
    dispTime = formatTime(tz_now.hour, tz_now.minute, tz_now.second)
    print('{0}{1}:{2}{3}:{4}{5}'.format(*[i for i in dispTime]))
    for digit in range(6):
        for nixSlice in range(10):
            if str(nixSlice) == dispTime[digit]:
                sliceConfig = config['Lights']['num-{0}'.format(digit)][nixSlice]
                updateSlice(digit, nixSlice, sliceConfig['brightness'], sliceConfig['color'])
            else:
                updateSlice(digit, nixSlice, 255, '#000000')


def rgb(h):
    h = h.strip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))


def updateSlice(digit, nixSlice, brightness, color):
    global strip
    pos = ( digit * 10 ) + nixSlice
    rgbColor = rgb(color)
    strip.setPixelColorRGB(pos, *rgbColor)


if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    update(config)
    strip.show()

    tz = config['TZ'].replace(' ', '_')
    tz_now = datetime.now(timezone(tz))
    pastTime = formatTime(tz_now.hour, tz_now.minute, tz_now.second)

    try:
        while True:
            tz_now = datetime.now(timezone(tz))
            currentTime = formatTime(tz_now.hour, tz_now.minute, tz_now.second)
            if currentTime != pastTime:
                if timeSinceChange != stat(configFile)[9]:
                    print('CHANGE DETECTED')
                    newConfig = open(configFile, "r")
                    config = load(newConfig)
                    timeSinceChange = stat(configFile)[9]
                update(config)
                strip.show()
                pastTime = currentTime
            sleep(.25)
            
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0))
    except Exception as e:
        print('Thing failed')
        print(e)

from gpiozero import LED
from time import *

led = LED(12)

def allumage():
    led.on()
    sleep(0.4)
    print("\nInstallation allumée\n")

def arret():
    led.off()
    print("\nInstallation éteinte\n")

allumage()

while True:
    pass

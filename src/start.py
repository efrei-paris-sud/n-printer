#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from Adafruit_Thermal import *
import RPi.GPIO as GPIO
import subprocess, time, Image, socket


printer      = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

buttonPin1    = 12
ledPin1    = 6
ledPin4    = 26

#initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin4, GPIO.OUT)

GPIO.output(ledPin4, GPIO.LOW)

prevButtonState1 = GPIO.input(buttonPin1)
prevTime        = time.time()

tapEnable1       = False
holdEnable1      = False

tapTime      = 0.1
holdTime     = 2

GPIO.output(ledPin1, GPIO.HIGH)

time.sleep(5)
printer.feed(1)
printer.print("Imprimante desactivee appuyez sur le bouton 3 pour continuer\n")
printer.feed(2)



while(True):

    buttonState1 = GPIO.input(buttonPin1)
    t1 = time.time()


    if buttonState1 != prevButtonState1:
        prevButtonState1 = buttonState1   # Si l'etat a changé, nouveau etat/temps
        prevTime        = t1
    else:                             # si il ne change pas
        if (t1 - prevTime) >= holdTime:  # resté appuyé ?
            if holdEnable1 == True:
                exit(0)
                holdEnable1 = False          
                tapEnable1  = False          
        elif (t1 - prevTime) >= tapTime:
            if buttonState1 == True:
                if tapEnable1 == True:
                    GPIO.output(ledPin1, GPIO.LOW)
                    subprocess.call(["python", "/home/pi/Desktop/src/main.py"])                   
                    tapEnable1  = False        
                    holdEnable1 = False
            else:                        
                tapEnable1  = True     
                holdEnable1 = True
                GPIO.output(ledPin1, GPIO.HIGH)
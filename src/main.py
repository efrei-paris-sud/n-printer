#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *

printer      = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

buttonPin    = 23
tapTime      = 0.1

#initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#10 seconde avant le debut des actions 
time.sleep(10)

prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()


def tap():
  print("vous avez appuyé sur le bouton\n")
  subprocess.call(["python", "twitter.py"])
  print("twitter fini")


while(True):

  # on prend l'etat actuel du bouton
  buttonState = GPIO.input(buttonPin)
  t           = time.time()

  # l'etat a t'il changé ?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # si oui, nouvel etat et temps
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= tapTime: # si on depasse le taptime
      # depassé
      if buttonState == True:       # bouton laché
        tap()                     # on lance l'action
        print("tap")
        buttonState = False



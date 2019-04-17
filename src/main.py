#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *

printer      = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

buttonPin1    = 12
buttonPin4 = 21
buttonPin2    = 20
ledPin1    = 6
ledPin4    = 26
tapTime      = 0.1
holdTime     = 2
n = 0



#initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin1, GPIO.OUT)
GPIO.setup(ledPin4, GPIO.OUT)

#10 seconde avant le debut des actions


#on allume la led 3sec
GPIO.output(ledPin1, GPIO.HIGH)
GPIO.output(ledPin4, GPIO.HIGH)
time.sleep(3)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    printer.print('Imprimante connectee a internet')
    printer.feed(3)
except:
    printer.boldOn()
    printer.println('Connexion a internet echouee')
    printer.boldOff()
    printer.feed(3)
    exit(0)


query = "efrei"



def tap2():

  GPIO.output(ledPin4, GPIO.LOW)
  print("vous avez appuyé sur le bouton\n")
  printer.print("Impression des tweets 2\n " + query + "\n")
  time.sleep(1)
  GPIO.output(ledPin4, GPIO.HIGH)
  printer.feed(3)
  subprocess.call(["python", "twitter.py" , query, ' '])
  GPIO.output(ledPin4, GPIO.LOW)
  time.sleep(5)
  GPIO.output(ledPin4, GPIO.HIGH)
  print("twitter fini")

def tap():
    global n
    global query
    GPIO.output(ledPin1, GPIO.LOW)
    queryTab = ["from:facebook", "from:instagram", "from:twitter"]
    n = n + 1
    n = n % 3
    GPIO.output(ledPin1, GPIO.HIGH)
    print("vous avez appuyé sur le bouton 3\n")
    query=queryTab[n]
    GPIO.output(ledPin1, GPIO.LOW)
    hashtag = ' '
    print(query)
    printer.print("Changement pour les tweets de \n "+ query + "\n")
    printer.feed(3)
    GPIO.output(ledPin1, GPIO.HIGH)


def tap4():
  GPIO.output(ledPin4, GPIO.LOW)
  print("vous avez appuyé sur le bouton 1\n")
  time.sleep(1)
  GPIO.output(ledPin4, GPIO.HIGH)
  printer.printImage(Image.open('weather.jpeg'), True)
  query = 'from:mto_idf'
  hashtag = '#paris'
  subprocess.call(["python", "twitter.py", query, hashtag])
  GPIO.output(ledPin4, GPIO.LOW)
  printer.printImage(Image.open('stocks.jpeg'), True)
  subprocess.call(["python", "twitter.py", "from:boursorama", "#bourse"])
  GPIO.output(ledPin4, GPIO.HIGH)

  
prevButtonState1 = GPIO.input(buttonPin1)
prevButtonState2 = GPIO.input(buttonPin2)
prevButtonState4 = GPIO.input(buttonPin4)
prevTime        = time.time()
tapEnable1       = False
holdEnable2     = False
holdEnable4     = False
tapEnable4       = False
tapEnable2       = False
holdEnable1      = False


dailyFlag    = False
dailyRatp = False

def daily():
  GPIO.output(ledPin1, GPIO.LOW)
  printer.printImage(Image.open('morning.jpeg'), True)
  GPIO.output(ledPin1, GPIO.HIGH)
  subprocess.call(["python", "twitter.py", "from:mto_idf", "#paris"])
  GPIO.output(ledPin1, GPIO.LOW)
  printer.printImage(Image.open('stocks.jpeg'), True)
  subprocess.call(["python", "twitter.py", "from:boursorama", "#bourse"])
  GPIO.output(ledPin1, GPIO.HIGH)
  
def ratp():
  GPIO.output(ledPin1, GPIO.HIGH)
  printer.printImage(Image.open('ratp.jpeg'), True)
  subprocess.call(["python", "twitter.py", "from:Ligne13_RATP", " "])
  GPIO.output(ledPin1, GPIO.LOW)





def hold():
  GPIO.output(ledPin4, GPIO.HIGH)
  GPIO.output(ledPin1, GPIO.LOW)
  printer.printImage(Image.open('goodbye.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin4, GPIO.LOW)

def hold2():
  GPIO.output(ledPin4, GPIO.LOW)
  printer.printImage(Image.open('goodbye.png'), True)
  printer.feed(3)
  GPIO.output(ledPin1, GPIO.HIGH)
  exit(0)

printer.printImage(Image.open('hello.jpeg'), True)
printer.print("1. Afficher meteo et bourse \n  Hold : eteindre \n\n2. Imprimer les tweet \n\n3. Changer le type de tweet\n Hold : desactiver")
printer.feed(6)

while(True):

    buttonState1 = GPIO.input(buttonPin1)
    buttonState2 = GPIO.input(buttonPin2)
    buttonState4 = GPIO.input(buttonPin4)
    t1 = time.time()
    t2 = time.time()
    t4 = time.time()
    
    sancho = printer.hasPaper()
    if int(sancho) != 1:
        GPIO.output(ledPin1, GPIO.LOW)
        time.sleep(1)
        GPIO.output(ledPin1, GPIO.HIGH)
        GPIO.output(ledPin4, GPIO.LOW)
        time.sleep(1)
        GPIO.output(ledPin4, GPIO.HIGH)
        
    
        
    if buttonState1 != prevButtonState1:
        prevButtonState1 = buttonState1   # Si l'etat a changé, nouveau etat/temps
        prevTime        = t1
    else:                             # si il ne change pas
        if (t1 - prevTime) >= holdTime:  # resté appuyé ?
            if holdEnable1 == True:        # le bouton est il appuyé
                hold2()                      # action resté appuyé
                holdEnable1 = False          
                tapEnable1  = False          
        elif (t1 - prevTime) >= tapTime:
            if buttonState1 == True:
                if tapEnable1 == True:       
                    tap()                     
                    tapEnable1  = False        
                    holdEnable1 = False
            else:                        
                tapEnable1  = True     
                holdEnable1 = True
                
    if buttonState4 != prevButtonState4:
        prevButtonState4 = buttonState4   # Si l'etat a changé, nouveau etat/temps
        prevTime        = t4
    else:                             # si il ne change pas
        if (t4 - prevTime) >= holdTime:  # resté appuyé ?
            if holdEnable4 == True:        # le bouton est il appuyé
                hold()                      # action resté appuyé
                holdEnable4 = False          
                tapEnable4  = False          
        elif (t4 - prevTime) >= tapTime:
            if buttonState4 == True:
                if tapEnable4 == True:       
                    tap4()                     
                    tapEnable4  = False        
                    holdEnable4 = False
            else:                        
                tapEnable4  = True     
                holdEnable4 = True

    if buttonState2 != prevButtonState2:
        prevButtonState2 = buttonState2   # Si l'etat a changé, nouveau etat/temps
        prevTime        = t2
    else:                             # si il ne change pas
        if (t2 - prevTime) >= holdTime:  # resté appuyé ?
            if holdEnable2 == True:        # le bouton est il appuyé
                hold()                      # action resté appuyé
                holdEnable2 = False          
                tapEnable2  = False          
        elif (t2 - prevTime) >= tapTime:
            if buttonState2 == True:
                if tapEnable2 == True:       
                    tap2()                     
                    tapEnable2 = False        
                    holdEnable2 = False
            else:                        
                tapEnable2  = True     
                holdEnable2 = True

    l = time.localtime()

    if (l.tm_hour == 8) and (l.tm_min == 00):
        if dailyFlag == False:
            daily()
            dailyFlag = True
    else:
        dailyFlag = False
    
    if ((l.tm_hour == 8) and (l.tm_min == 30)) or ((l.tm_hour == 17) and (l.tm_min == 05)):
        if dailyRatp == False:
            ratp()
            dailyRatp = True
    else:
        dailyRatp = False 

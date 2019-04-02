#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from serial import Serial
import time

class Adafruit_Thermal(Serial):

    resumeTime      =  0.0
    byteTime        =  0.0
    dotPrintTime    =  0.033
    dotFeedTime     =  0.0025
    prevByte        = '\n'
    column          =  0
    maxColumn       = 32
    charHeight      = 24
    lineSpacing     =  8
    barcodeHeight   = 50
    printMode       =  0
    defaultHeatTime = 60

    #initialisation du baudrate
    def __init__(self, *args, **kwargs):
        baudrate = 19200
        if len(args) == 0:
            args = [ "/dev/serial0", baudrate ]
        elif len(args) == 1:
            args = [ args[0], baudrate ]
        else:
            baudrate = args[1]

        self.byteTime = 11.0 / float(baudrate)

        Serial.__init__(self, *args, **kwargs)

        #Attente avant demarrage
        self.timeoutSet(0.5)

        self.wake()
        self.reset()

        # specifications du manuel de l'imprimante
        heatTime = kwargs.get('heattime', self.defaultHeatTime)
        self.writeBytes(
          27,       
          55,       
          20,      
          heatTime, 
          250)      # Heat interval

        printDensity   = 14 # 120%
        printBreakTime =  4

        self.writeBytes(
          18, 
          35, 
          (printBreakTime << 5) | printDensity)

        self.dotPrintTime = 0.03
        self.dotFeedTime  = 0.0021




    # Fonctions d'attente pour eviter les surcharges
    def timeoutSet(self, x):
        self.resumeTime = time.time() + x
        
    def timeoutWait(self):
        while (time.time() - self.resumeTime) < 0: pass


     #temps, vitesse impressions et saut de lignes
    def setTimes(self, p, f):
        self.dotPrintTime = p / 1000000.0
        self.dotFeedTime  = f / 1000000.0


    def writeBytes(self, *args):
        self.timeoutWait()
        self.timeoutSet(len(args) * self.byteTime)
        for arg in args:
            super(Adafruit_Thermal, self).write(chr(arg))


    # ecriture sur le papier
    def write(self, *data):
        for i in range(len(data)):
            c = data[i]
            if c != 0x13:
                self.timeoutWait()
                super(Adafruit_Thermal, self).write(c)
                d = self.byteTime
                if ((c == '\n') or
                    (self.column == self.maxColumn)):
                    if self.prevByte == '\n':
                        d += ((self.charHeight +
                               self.lineSpacing) *
                              self.dotFeedTime)
                    else:
                        # lignze de texte
                        d += ((self.charHeight *
                               self.dotPrintTime) +
                              (self.lineSpacing *
                               self.dotFeedTime))
                        self.column = 0
                        c = '\n'
                else:
                    self.column += 1
                self.timeoutSet(d)
                self.prevByte = c


    def reset(self):
        self.prevByte      = '\n'
        self.column        =  0
        self.maxColumn     = 32
        self.charHeight    = 24
        self.lineSpacing   =  8
        self.barcodeHeight = 50
        self.writeBytes(27, 64)

    #parametre par defaut du texte
    def setDefault(self):
        self.online()
        self.justify('L')
        self.inverseOff()
        self.doubleHeightOff()
        self.setLineHeight(32)
        self.boldOff()
        self.underlineOff()
        self.setBarcodeHeight(50)
        self.setSize('s')


    def test(self):
        self.writeBytes(18, 84)
        self.timeoutSet(
          self.dotPrintTime * 24 * 26 +
          self.dotFeedTime  * (8 * 26 + 32))


    UPC_A   =  0
    UPC_E   =  1
    EAN13   =  2
    EAN8    =  3
    CODE39  =  4
    I25     =  5
    CODEBAR =  6
    CODE93  =  7
    CODE128 =  8
    CODE11  =  9
    MSI     = 10

    def printBarcode(self, text, type):
        self.writeBytes(
          29,  72, 2,    
          29, 119, 3,    
          29, 107, type) 
        self.timeoutWait()
        self.timeoutSet((self.barcodeHeight + 40) * self.dotPrintTime)
        super(Adafruit_Thermal, self).write(text)
        self.prevByte = '\n'
        self.feed(2)

    def setBarcodeHeight(self, val=50):
        if val < 1:
            val = 1
        self.barcodeHeight = val
        self.writeBytes(29, 104, val)


    # === Character commands ===

    INVERSE_MASK       = (1 << 1)
    UPDOWN_MASK        = (1 << 2)
    BOLD_MASK          = (1 << 3)
    DOUBLE_HEIGHT_MASK = (1 << 4)
    DOUBLE_WIDTH_MASK  = (1 << 5)
    STRIKE_MASK        = (1 << 6)

    def setPrintMode(self, mask):
        self.printMode |= mask
        self.writePrintMode()
        if self.printMode & self.DOUBLE_HEIGHT_MASK:
            self.charHeight = 48
        else:
            self.charHeight = 24
        if self.printMode & self.DOUBLE_WIDTH_MASK:
            self.maxColumn  = 16
        else:
            self.maxColumn  = 32

    def unsetPrintMode(self, mask):
        self.printMode &= ~mask
        self.writePrintMode()
        if self.printMode & self.DOUBLE_HEIGHT_MASK:
            self.charHeight = 48
        else:
            self.charHeight = 24
        if self.printMode & self.DOUBLE_WIDTH_MASK:
            self.maxColumn  = 16
        else:
            self.maxColumn  = 32

    def writePrintMode(self):
        self.writeBytes(27, 33, self.printMode)

    def normal(self):
        self.printMode = 0
        self.writePrintMode()

    def inverseOn(self):
        self.setPrintMode(self.INVERSE_MASK)

    def inverseOff(self):
        self.unsetPrintMode(self.INVERSE_MASK)

    def upsideDownOn(self):
        self.setPrintMode(self.UPDOWN_MASK)

    def upsideDownOff(self):
        self.unsetPrintMode(self.UPDOWN_MASK)

    def doubleHeightOn(self):
        self.setPrintMode(self.DOUBLE_HEIGHT_MASK)

    def doubleHeightOff(self):
        self.unsetPrintMode(self.DOUBLE_HEIGHT_MASK)

    def doubleWidthOn(self):
        self.setPrintMode(self.DOUBLE_WIDTH_MASK)

    def doubleWidthOff(self):
        self.unsetPrintMode(self.DOUBLE_WIDTH_MASK)

    def strikeOn(self):
        self.setPrintMode(self.STRIKE_MASK)

    def strikeOff(self):
        self.unsetPrintMode(self.STRIKE_MASK)

    def boldOn(self):
        self.setPrintMode(self.BOLD_MASK)

    def boldOff(self):
        self.unsetPrintMode(self.BOLD_MASK)


    def justify(self, value):
        c = value.upper()
        if   c == 'C':
            pos = 1
        elif c == 'R':
            pos = 2
        else:
            pos = 0
        self.writeBytes(0x1B, 0x61, pos)


    # sauter une ligne
    def feed(self, x=1):
        while x > 0:
            self.write('\n')
            x -= 1


    def flush(self):
        self.writeBytes(12)


    def setSize(self, value):
        c = value.upper()
        if c == 'L':   # Large: double width and height
            size            = 0x11
            self.charHeight = 48
            self.maxColumn  = 16
        elif c == 'M': # Medium: double height
            size            = 0x01
            self.charHeight = 48
            self.maxColumn  = 32
        else:          # Small: standard width and height
            size            = 0x00
            self.charHeight = 24
            self.maxColumn  = 32

        self.writeBytes(29, 33, size, 10)
        prevByte = '\n' # Setting the size adds a linefeed


    # 0 - non souligné
    # 1 - souligné
    # 2 - souligné gras
    def underlineOn(self, weight=1):
        self.writeBytes(27, 45, weight)


    def underlineOff(self):
        self.underlineOn(0)


    def printBitmap(self, w, h, bitmap, LaaT=False):
        rowBytes = (w + 7) / 8 
        if rowBytes >= 48:
            rowBytesClipped = 48
        else:
            rowBytesClipped = rowBytes

        if LaaT: maxChunkHeight = 1
        else:    maxChunkHeight = 255

        i = 0
        for rowStart in range(0, h, maxChunkHeight):
            chunkHeight = h - rowStart
            if chunkHeight > maxChunkHeight:
                chunkHeight = maxChunkHeight

            self.writeBytes(18, 42, chunkHeight, rowBytesClipped)

            for y in range(chunkHeight):
                for x in range(rowBytesClipped):
                    super(Adafruit_Thermal, self).write(
                      chr(bitmap[i]))
                    i += 1
                i += rowBytes - rowBytesClipped
            self.timeoutSet(chunkHeight * self.dotPrintTime)

        self.prevByte = '\n'

    #Impression d'image
    def printImage(self, image, LaaT=False):
        import Image

        if image.mode != '1':
            image = image.convert('1')

        width  = image.size[0]
        height = image.size[1]
        if width > 384:
            width = 384
        rowBytes = (width + 7) / 8
        bitmap   = bytearray(rowBytes * height)
        pixels   = image.load()

        for y in range(height):
            n = y * rowBytes
            x = 0
            for b in range(rowBytes):
                sum = 0
                bit = 128
                while bit > 0:
                    if x >= width: break
                    if pixels[x, y] == 0:
                        sum |= bit
                    x    += 1
                    bit >>= 1
                bitmap[n + b] = sum

        self.printBitmap(width, height, bitmap, LaaT)


    # ne plus imprimer
    def offline(self):
        self.writeBytes(27, 61, 0)


    # imprimer les instructions
    def online(self):
        self.writeBytes(27, 61, 1)


    def sleep(self):
        self.sleepAfter(1)


    def sleepAfter(self, seconds):
        self.writeBytes(27, 56, seconds)


    def wake(self):
        self.timeoutSet(0);
        self.writeBytes(255)
        for i in range(10):
            self.writeBytes(27)
            self.timeoutSet(0.1)



    # CVerifie si il ya du papier
    # retourne true si il y a du papier et false si il n'y en as pas
    def hasPaper(self):
        self.writeBytes(27, 118, 0)
        stat = ord(self.read(1)) & 0b00000100
        return stat == 0


    def setLineHeight(self, val=32):
        if val < 24:
            val = 24
        self.lineSpacing = val - 24

        self.writeBytes(27, 51, val)


    def tab(self):
        self.writeBytes(9)


    def setCharSpacing(self, spacing):
        self.writeBytes(27, 32, 0, 10)


    def print(self, *args, **kwargs):
        for arg in args:
            self.write(str(arg))

    def println(self, *args, **kwargs):
        for arg in args:
            self.write(str(arg))
        self.write('\n')


# -*- coding: utf-8 -*-

# Notes
#   1. You must enable I2C on your Raspberry Pi board (see your particular operating system documentation).
#       On Raspian: Menu...Preferences...Raspberry Pi Configuration...Interfaces...Enable I2C
#   2. If using Python 3, you will need to install python3-smbus:
#       sudo apt-get install python3-smbus

'''
  I2cCharDisplayDemo.ino

  Written by: Gary Muhonen  gary@wht.io

  versions
    1.0.0 - 8/2/2016
      Original release.

  Short Description:

    These files provide software for the Raspberry Pi, using Python2 or Python3.
    The library files provide useful functions to make it easy
    to communicate with OLED and LCD character
    display modules that use the I2C communication protocol. The demo
    program shows the usage of the functions in the library.

    The library will work with **LCD** and **OLED** character displays
    (e.g. 16x2, 20x2, 20x4, etc.). The LCD displays must use the the
    HD44780 controller chip and have a I2C PCA8574 i/o expander chip
    on a backpack board (which gives the display I2C capability).
    OLED display modules must have the US2066 controller chip
    (which has I2C built in).

    See the links below for installation and usage information.

    Project Details:
    * Library installation and usage: http://wht.io/portfolio/i2c-display-library/
    * OLED hardware information for EastRising modules: http://wht.io/portfolio/i2c-oled-backpack-board-eastrising/
    * OLED hardware information for Newhaven modules: http://wht.io/portfolio/i2c-oled-backpack-board-newhaven/
    * LCD hardware information: http://wht.io/portfolio/i2c-lcd-backpack-board/

    Software Github repositories (library and demo programs):
    * Arduino library files:  https://github.com/wht-io/i2c-char-display-arduino.git
    * Particle library files: https://github.com/wht-io/i2c-char-display-particle.git
    * Raspberry Pi library files: https://github.com/wht-io/i2c-char-display-raspberrypi.git


'''

'''
    This demo program is public domain. You may use it for any purpose.
    NO WARRANTY IS IMPLIED.
'''

from I2cCharDisplay import I2cCharDisplay
from time import sleep

if __name__ == "__main__":


    LCDADDRESS =    0x27                    # i2c address for the lcd display
    OLEDADDRESS =   0x3c                    # i2c address for the oled display

    TESTNUM =       2                       # number of times to run each test

    # In this demo program we are testing both a LCD and OLED display.
    # This program will still run correctly even if you only have one of these displays is hooked up.
    # Normally you would only use one of these two next lines of code, if you only have one display.
    lcd = I2cCharDisplay("LCD", LCDADDRESS, 2)    # create an lcd object for a 2 line display
    oled = I2cCharDisplay("OLED", OLEDADDRESS, 2) # create an oled object for a 2 line display

    while 1:                         # keep running this program until ctrl C is pressed

        # change the constant TESTNUM above to control how many times each test is run.

        # test the lcd backlight on/off and the oled brightness commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Backlight On/Off")
        oled.writeString("Set Brightness")
        for i in range(0,TESTNUM):
            sleep(1)
            lcd.backlightOff()
            oled.setBrightness(0)
            sleep(1)
            lcd.backlightOn()
            oled.setBrightness(255)


        # test the clear command
        lcd.clear()
        oled.clear()
        for i in range(0,TESTNUM):
            lcd.writeString("Clear Display")
            oled.writeString("Clear Display")
            sleep(1)
            lcd.clear()
            oled.clear()
            sleep(1)

        # test the cursor home command
        lcd.clear()
        oled.clear()
        lcd.cursorOn()
        oled.cursorOn()
        for i in range(0,TESTNUM):
            lcd.clear()
            oled.clear()
            lcd.writeString("Cursor Home")
            oled.writeString("Cursor Home")
            sleep(1)
            lcd.home()
            oled.home()
            sleep(1)
            lcd.writeString("123456789012345")
            oled.writeString("123456789012345")
            sleep(1)
        lcd.cursorOff()
        oled.cursorOff()

        # test the cursor move command
        lcd.clear()
        oled.clear()
        lcd.cursorOn()
        oled.cursorOn()
        for i in range(0,TESTNUM):
            lcd.clear()
            oled.clear()
            lcd.writeString("Cursor Move")
            oled.writeString("Cursor Move")
            sleep(1)
            lcd.cursorMove(2, 1)
            oled.cursorMove(2, 1)
            lcd.writeString("12345")
            oled.writeString("12345")
            sleep(1)
            lcd.cursorMove(2, 9)
            oled.cursorMove(2, 9)
            sleep(1)
            lcd.writeString("12345")
            oled.writeString("12345")
            sleep(1)
        lcd.cursorOff()
        oled.cursorOff()

        # test the display on/off commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Display On/Off")
        oled.writeString("Display On/Off")
        for i in range(0,TESTNUM):
            lcd.displayOn()
            oled.displayOn()
            sleep(1)
            lcd.displayOff()
            oled.displayOff()
            sleep(1)
        lcd.displayOn()
        oled.displayOn()

        # test the cursor blink on/off commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Cursor Block")
        oled.writeString("Cursor Block")
        lcd.cursorBlinkOn()
        oled.cursorBlinkOn()
        for i in range(0,TESTNUM):
            lcd.cursorMove(2, 7)
            oled.cursorMove(2, 7)
            sleep(1)
            lcd.writeString("12345")
            oled.writeString("12345")
            sleep(1)
            lcd.cursorMove(2, 7)
            oled.cursorMove(2, 7)
            sleep(1)
            lcd.writeString("67890")
            oled.writeString("67890")
            sleep(1)
        lcd.cursorBlinkOff()
        oled.cursorBlinkOff()

        # test the cursor  on/off commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Cursor On/Off")
        oled.writeString("Cursor On/Off")
        lcd.cursorMove(2, 7)
        oled.cursorMove(2, 7)
        for i in range(0,TESTNUM):
            lcd.cursorOn()
            oled.cursorOn()
            sleep(1)
            lcd.cursorOff()
            oled.cursorOff()
            sleep(1)

        # test the display shift left and right commands (cursor shifts too)
        lcd.clear()
        oled.clear()
        lcd.writeString("Disp Shift R/L")
        oled.writeString("Disp Shift R/L")
        sleep(2)
        lcd.cursorOn()
        oled.cursorOn()
        for i in range(0,TESTNUM):
            lcd.displayShiftLeft()
            oled.displayShiftLeft()
            sleep(1)
            lcd.displayShiftLeft()
            oled.displayShiftLeft()
            sleep(1)
            lcd.displayShiftLeft()
            oled.displayShiftLeft()
            sleep(1)
            lcd.displayShiftRight()
            oled.displayShiftRight()
            sleep(1)
            lcd.displayShiftRight()
            oled.displayShiftRight()
            sleep(1)
            lcd.displayShiftRight()
            oled.displayShiftRight()
            sleep(1)
        lcd.cursorOff()
        oled.cursorOff()

        # test the cursor shift left/right commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Cursor Shift L/R")
        oled.writeString("Cursor Shift L/R")
        lcd.cursorOn()
        oled.cursorOn()
        lcd.cursorMove(2, 7)
        oled.cursorMove(2, 7)
        for i in range(0,TESTNUM):
            lcd.cursorShiftLeft()
            oled.cursorShiftLeft()
            sleep(.5)
            lcd.cursorShiftLeft()
            oled.cursorShiftLeft()
            sleep(.5)
            lcd.cursorShiftLeft()
            oled.cursorShiftLeft()
            sleep(.5)
            lcd.cursorShiftRight()
            oled.cursorShiftRight()
            sleep(.5)
            lcd.cursorShiftRight()
            oled.cursorShiftRight()
            sleep(.5)
            lcd.cursorShiftRight()
            oled.cursorShiftRight()
            sleep(.5)
        lcd.cursorOff()
        oled.cursorOff()

        # test the displayLeftToRight and displayRightToLeft commands
        lcd.clear()
        oled.clear()
        for i in range(0,TESTNUM):
            lcd.displayLeftToRight()
            oled.displayLeftToRight()
            lcd.clear()
            oled.clear()
            lcd.writeString("Display L -> R")
            oled.writeString("Display  L -> R")
            lcd.cursorMove(2, 7)
            oled.cursorMove(2, 7)
            lcd.writeString("12345")
            oled.writeString("12345")
            sleep(2)
            lcd.clear()
            oled.clear()
            lcd.writeString("Display R -> L")
            oled.writeString("Display  R -> L")
            lcd.displayRightToLeft()
            oled.displayRightToLeft()
            lcd.cursorMove(2, 7)
            oled.cursorMove(2, 7)
            lcd.writeString("12345")
            oled.writeString("12345")
            sleep(2)
        lcd.displayLeftToRight()
        oled.displayLeftToRight()

        # test the displayShiftOn and displayShiftOff commands
        for i in range(0,TESTNUM):
            lcd.clear()
            oled.clear()
            lcd.writeString("Display Shift On")
            oled.writeString("Display Shift On")
            sleep(2)
            lcd.displayShiftOn()
            oled.displayShiftOn()
            lcd.cursorMove(2, 9)
            oled.cursorMove(2, 9)
            for i in range(0, 8):
                lcd.writeString("%s" %i)
                oled.writeString("%s" %i)
                sleep(.5)
            sleep(2)
            lcd.displayShiftOff()
            oled.displayShiftOff()
            lcd.clear()
            oled.clear()
            lcd.writeString("Disp Shift Off")
            oled.writeString("Disp Shift Off")
            sleep(2)
            lcd.cursorMove(2, 9)
            oled.cursorMove(2, 9)
            for i in range(0, 8):
                lcd.writeString("%s" %i)
                oled.writeString("%s" %i)
                sleep(.5)
            sleep(2)

        # test the lcd backlight on/off and the oled brightness commands
        lcd.clear()
        oled.clear()
        lcd.writeString("Backlight on/off")
        oled.writeString("Brightness test")
        for i in range(0,TESTNUM):
            sleep(1)
            lcd.backlightOff()
            oled.setBrightness(0)
            sleep(1)
            lcd.backlightOn()
            oled.setBrightness(255)

        # test creating and displaying custom characters
        # thanks to dfrobot.com for these custom characters
        bell     = [0x4, 0xe, 0xe, 0xe, 0x1f, 0x0, 0x4 ]
        note     = [0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0 ]
        clock1   = [0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0 ]
        heart    = [0x0, 0xa, 0x1f, 0x1f, 0xe, 0x4, 0x0 ]
        duck     = [0x0, 0xc, 0x1d, 0xf, 0xf, 0x6, 0x0 ]
        check    = [0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0 ]
        cross    = [0x0, 0x1b, 0xe, 0x4, 0xe, 0x1b, 0x0 ]
        retarrow = [0x1, 0x1, 0x5, 0x9, 0x1f, 0x8, 0x4 ]
        lcd.createCharacter(0, bell)
        lcd.createCharacter(1, note)
        lcd.createCharacter(2, clock1)
        lcd.createCharacter(3, heart)
        lcd.createCharacter(4, duck)
        lcd.createCharacter(5, check)
        lcd.createCharacter(6, cross)
        lcd.createCharacter(7, retarrow)
        oled.createCharacter(0, bell)
        oled.createCharacter(1, note)
        oled.createCharacter(2, clock1)
        oled.createCharacter(3, heart)
        oled.createCharacter(4, duck)
        oled.createCharacter(5, check)
        oled.createCharacter(6, cross)
        oled.createCharacter(7, retarrow)
        for i in range(0,TESTNUM):
            lcd.clear()
            oled.clear()
            sleep(.2)
            lcd.writeString("Custom Chars")
            oled.writeString("Custom Chars")
            lcd.cursorMove(2, 3)
            oled.cursorMove(2, 3)
            lcd.sendData(0)
            oled.sendData(0)
            sleep(.2)
            lcd.sendData(1)
            oled.sendData(1)
            sleep(.2)
            lcd.sendData(2)
            oled.sendData(2)
            sleep(.2)
            lcd.sendData(3)
            oled.sendData(3)
            sleep(.2)
            lcd.sendData(4)
            oled.sendData(4)
            sleep(.2)
            lcd.sendData(5)
            oled.sendData(5)
            sleep(.2)
            lcd.sendData(6)
            oled.sendData(6)
            sleep(.2)
            lcd.sendData(7)
            oled.sendData(7)
            sleep(2)

        # test printing some numbers
        x = 1.23
        j = 11
        for i in range(0,TESTNUM):
            lcd.clear()
            oled.clear()
            lcd.writeString("Printing Hex")
            oled.writeString("Printing Hex")
            lcd.cursorMove(2, 9)
            oled.cursorMove(2, 9)
            lcd.writeString("j= %#x" %j)                  # print in hex
            oled.writeString("j= %#x" %j)
            sleep(2)
            lcd.clear()
            oled.clear()
            lcd.writeString("Printing Numbers")
            oled.writeString("Printing Numbers")
            lcd.cursorMove(2, 1)               # move to 2nd line
            oled.cursorMove(2, 1)
            lcd.writeString("x= %s" %x)                    # print 1 decimal places
            oled.writeString("x= %s" %x)
            lcd.cursorMove(2, 9)
            oled.cursorMove(2, 9)
            lcd.writeString("j= %s" %j)                  # print in decimal
            oled.writeString("j= %s" %j)
            sleep(2)

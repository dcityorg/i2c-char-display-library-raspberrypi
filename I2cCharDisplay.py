# -*- coding: utf-8 -*-

'''
    I2cCharDisplay.py - class library for using LCD and OLED character displays

    Written by: Gary Muhonen  gary@dcity.org

    Versions
        1.0.0 - 8/2/2016
            Original release.
        1.0.1 - 9/1/2018
            Transfer to GM, and some minor changes
            Added these OLED "fade display" functions (not very useful for some types of OLED displays)
                void fadeOff()           - turns off the fade feature of the OLED
                void fadeOnce(value)   - fade out the display to off (fade time 0-16) - (on some display types, it doesn't work very well. It takes the display to half brightness and then turns off display)
                void fadeBlink(value)  - blinks the fade feature of the OLED (fade time 0-16) - (on some display types, it doesn't work very well. It takes the display to half brightness and then turns off display)
        1.0.2 - 7/1/2019
            The functions fadeOff(), faderOnce() and fadeBlink() did not get put into the I2cCharDisplay.py file (in version 1.0.1)
                and are added in this version.

    Short Description:

        These files provide a software library and demo program for the Raspberry Pi

        The library files provide useful functions to make it easy
        to communicate with OLED and LCD character
        display modules that use the I2C communication protocol. The demo
        program shows the usage of the functions in the library.

        The library will work with **LCD** and **OLED** character displays
        (e.g. 16x2, 20x2, 20x4, etc.). The LCD displays must use the the
        HD44780 controller chip and have a I2C PCA8574 i/o expander chip
        on a backpack board (which gives the display I2C capability).
        OLED display modules must have the US2066 controller chip
        (which has I2C built in). Backback boards are available and
        details are in the link below.


    https://www.dcity.org/portfolio/i2c-display-library/
    This link has details including:
        * software library installation for use with Arduino, Particle and Raspberry Pi boards
        * list of functions available in these libraries
        * a demo program (which shows the usage of most library functions)
        * info on OLED and LCD character displays that work with this software
        * hardware design for a backpack board for LCDs and OLEDs, available on github
        * info on backpack “bare” pc boards available from OSH Park.

    License Information:  https://www.dcity.org/license-information/


    Notes:
        1. You must enable I2C on your Raspberry Pi board (see your particular operating system documentation).
            On Raspian: Menu...Preferences...Raspberry Pi Configuration...Interfaces...Enable I2C
        2. This software was tested on a RASPBERRY PI 3 MODEL B, running Rasbian and Python 3.5.2

'''

import smbus                # import the i2c library
from time import sleep      # import the sleep functions

# python SMBus commands: http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
i2c = smbus.SMBus(1)        # create an i2c object for writing/reading from i2c

# create a class for the i2c LCD and OLED character displays
class I2cCharDisplay(object):

    # _displayType options
    LCD_TYPE = "LCD"                # if the display is an LCD using the PCA8574 outputting to the HD44780 lcd controller chip
    OLED_TYPE = "OLED"              # if the display is a OLED using the US2066 oled controller chip

    # oled specific constants
    OLED_COMMANDMODE =             0x80
    OLED_DATAMODE =                0x40
    OLED_SETBRIGHTNESSCOMMAND =    0X81
    OLED_SETFADECOMMAND =          0x23       # command address for setting the fade out command
    # bits for setting the fade command
    OLED_FADEOFF =                 0X00       # command value for setting fade mode to off
    OLED_FADEON =                  0X20       # command value for setting fade mode to on
    OLED_FADEBLINK =               0X30       # command value for setting fade mode to blink

    # lcd specific constants

    # bits on the PCA8574 chip for controlling the lcd
    LCD_BACKLIGHTON =     8 # backlight on bit
    LCD_BACKLIGHTOFF =    0 # backlight off
    LCD_ENABLEON =        4 # Enable bit on
    LCD_ENABLEOFF =       0 # Enable bit off
    LCD_READ =            2 # Read bit
    LCD_WRITE =           0 # Write bit
    LCD_DATA =            1 # Register Select bit for Data
    LCD_COMMAND =         0 # Register Select bit for Command

    # lcd and oled constants

    # lcd commands
    LCD_CLEARDISPLAYCOMMAND =      0x01
    LCD_RETURNHOMECOMMAND =        0x02
    LCD_ENTRYMODECOMMAND =         0x04
    LCD_DISPLAYCONTROLCOMMAND =    0x08
    LCD_SHIFTCOMMAND =             0x10
    LCD_FUNCTIONSETCOMMAND =       0x20
    LCD_SETCGRAMADDRCOMMAND =      0x40
    LCD_SETDDRAMADDRCOMMAND =      0x80

    # bits for _lcdEntryModeCommand
    LCD_DISPLAYLEFTTORIGHT =       0x02
    LCD_DISPLAYRIGHTTOLEFT =       0X00
    LCD_DISPLAYSHIFTON =           0x01
    LCD_DISPLAYSHIFTOFF =          0x00

    # bits for _lcdDisplayControlCommand
    LCD_DISPLAYON =                0x04
    LCD_DISPLAYOFF =               0x00
    LCD_CURSORON =                 0x02
    LCD_CURSOROFF =                0x00
    LCD_CURSORBLINKON =            0x01
    LCD_CURSORBLINKOFF =           0x00

    # bits for _lcdFunctionSetCommand
    LCD_8BITMODE =                 0x10
    LCD_4BITMODE =                 0x00
    LCD_2LINES =                   0x08
    LCD_1LINES =                   0x00
    LCD_5x10DOTS =                 0x04
    LCD_5x8DOTS =                  0x00

    # bits for shifting the display and the cursor
    LCD_DISPLAYSHIFT =             0x08
    LCD_CURSORSHIFT =              0x00
    LCD_SHIFTRIGHT =               0x04
    LCD_SHIFTLEFT =                0x00


    # constructor to create I2cCharDisplay object, and init the display
    def __init__(self, displayType, i2cAddress, rows):

        # vars used by functions in the class

        self._displayType = displayType  # keep track of the type of display we are using (e.g. lcd, oled, etc.)
        self._i2cAddress = i2cAddress
        self._rows = rows                # number of rows in the display (starting at 1)
        self._lcdBacklightControl = I2cCharDisplay.LCD_BACKLIGHTON     # 0 if backlight is off, 0x08 is on
        # keep track of these registers in the display
        self._lcdEntryModeCommand = 0
        self._lcdDisplayControlCommand = 0
        self._lcdFunctionSetCommand = 0

        # initialize the display, depending on if it is an OLED or LCD
        if self._displayType == I2cCharDisplay.LCD_TYPE:
            self.lcdBegin()
        elif self._displayType == I2cCharDisplay.OLED_TYPE:
            self.oledBegin()


    # write an ascii character (value) to the display
    def write(self, value):
        self.sendData(ord(value))


    # write a string (including formatting options)
    # For examples of printing numbers:  https:#mkaz.tech/python-string-format.html
    def writeString(self, value):
        for char in value:
            self.write(char)




    # functions that work with both OLED and LCD

    def clear(self):
        self.sendCommand(I2cCharDisplay.LCD_CLEARDISPLAYCOMMAND) # clear display
        sleep(.002)              # 1.53ms required


    def home(self):
        self.cursorMove(1, 1)    # use move command instead to avoid flicker on oled displays
        #  self.sendCommand(I2cCharDisplay.LCD_RETURNHOMECOMMAND) # move cursor to home
        #  sleep(.002)            # 1.53ms required


    # move cursor to new postion row,col  (both start at 1)
    def cursorMove(self,  row,  col):
        if (row > self._rows):              # if user points to a row too large, change row to the bottom row
            row = self._rows

        if (self._rows <= 2):               # if we have a 1 or 2 row display
            moveRowOffset2Rows =  [ 0x00, 0x40]
            self.sendCommand(I2cCharDisplay.LCD_SETDDRAMADDRCOMMAND | (col-1 + moveRowOffset2Rows[row-1]))
        else:                          # if we have a 3 or 4 line display
            if (self._displayType == I2cCharDisplay.LCD_TYPE):           # if using an LCD
                moveRowOffset4RowsLcd =  [ 0x00, 0x40, 0x14, 0x54 ]
                self.sendCommand(I2cCharDisplay.LCD_SETDDRAMADDRCOMMAND | (col-1 + moveRowOffset4RowsLcd[row-1]))
            else:                                    # if using an OLED
                moveRowOffset4RowsOled = [ 0x00, 0x20, 0x40, 0x60 ]
                self.sendCommand(I2cCharDisplay.LCD_SETDDRAMADDRCOMMAND | (col-1 + moveRowOffset4RowsOled[row-1]))



    # display on/off
    def displayOff(self):
        self._lcdDisplayControlCommand &= ~I2cCharDisplay.LCD_DISPLAYON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    def displayOn(self):
        self._lcdDisplayControlCommand |= I2cCharDisplay.LCD_DISPLAYON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    # cursor on/off
    def cursorOff(self):
        self._lcdDisplayControlCommand &= ~I2cCharDisplay.LCD_CURSORON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    def cursorOn(self):
        self._lcdDisplayControlCommand |= I2cCharDisplay.LCD_CURSORON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    # cursor blink on/off
    def cursorBlinkOff(self):
        self._lcdDisplayControlCommand &= ~I2cCharDisplay.LCD_CURSORBLINKON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    def cursorBlinkOn(self):
        self._lcdDisplayControlCommand |= I2cCharDisplay.LCD_CURSORBLINKON
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)


    # display shift left/right (also shifts the cursor)
    def displayShiftLeft(self):
        self.sendCommand(I2cCharDisplay.LCD_SHIFTCOMMAND | I2cCharDisplay.LCD_DISPLAYSHIFT | I2cCharDisplay.LCD_SHIFTLEFT)


    def displayShiftRight(self):
        self.sendCommand(I2cCharDisplay.LCD_SHIFTCOMMAND | I2cCharDisplay.LCD_DISPLAYSHIFT | I2cCharDisplay.LCD_SHIFTRIGHT)


    # cursor shift left/right and change the address counter
    def cursorShiftLeft(self):
        self.sendCommand(I2cCharDisplay.LCD_SHIFTCOMMAND | I2cCharDisplay.LCD_CURSORSHIFT | I2cCharDisplay.LCD_SHIFTLEFT)


    def cursorShiftRight(self):
        self.sendCommand(I2cCharDisplay.LCD_SHIFTCOMMAND | I2cCharDisplay.LCD_CURSORSHIFT | I2cCharDisplay.LCD_SHIFTRIGHT)



    # set text to flow left to right (DEFAULT MODE)
    def displayLeftToRight(self):
        self._lcdEntryModeCommand |= I2cCharDisplay.LCD_DISPLAYLEFTTORIGHT
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)


    # set text to flow right to left
    def displayRightToLeft(self):
        self._lcdEntryModeCommand &= ~I2cCharDisplay.LCD_DISPLAYLEFTTORIGHT
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)


    # entire display shifts when new data is written to display
    def displayShiftOn(self):
        self._lcdEntryModeCommand |= I2cCharDisplay.LCD_DISPLAYSHIFTON
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)


    # entire display does not shift when new data is written to display (NORMAL MODE)
    def displayShiftOff(self):
        self._lcdEntryModeCommand &= ~I2cCharDisplay.LCD_DISPLAYSHIFTON
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)


    # Fill one of the 8 CGRAM memory addresses (0-7) to create custom characters
    def createCharacter(self, address,  characterMap):
        address &= 0x7       # limit to the first 8 addresses
        self.sendCommand(I2cCharDisplay.LCD_SETCGRAMADDRCOMMAND | (address << 3))
        for i in range(0, 7):
            self.sendData(characterMap[i])



    # functions specific to LCD displays

    # Turn the lcd backlight off/on
    def backlightOff(self):
        self._lcdBacklightControl = I2cCharDisplay.LCD_BACKLIGHTOFF
        self.sendLcdByte(self._lcdBacklightControl)


    def backlightOn(self):
        self._lcdBacklightControl = I2cCharDisplay.LCD_BACKLIGHTON
        self.sendLcdByte(self._lcdBacklightControl)


    # functions specific to OLED displays

    def setBrightness(self,  value):
        self.sendCommand(0x80)        # set RE=1
        self.sendCommand(0x2A)

        self.sendCommand(0x80)        # set SD=1
        self.sendCommand(0x79)

        self.sendCommand(I2cCharDisplay.OLED_SETBRIGHTNESSCOMMAND)
        self.sendCommand(value)

        self.sendCommand(0x80)        # set SD=0
        self.sendCommand(0x78)

        self.sendCommand(0x80)        # set RE=0
        self.sendCommand(0x28)

    # Set the oled fade out feature to OFF
    def fadeOff(self):
        self.sendCommand(0x80)        # set RE=1
        self.sendCommand(0x2A)

        self.sendCommand(0x80)        # set SD=1
        self.sendCommand(0x79)

        self.sendCommand(I2cCharDisplay.OLED_SETFADECOMMAND)
        self.sendCommand(I2cCharDisplay.OLED_FADEOFF)      #set fade feature to OFF

        self.sendCommand(0x80)        # set SD=0
        self.sendCommand(0x78)

        self.sendCommand(0x80)        # set RE=0
        self.sendCommand(0x28)


    # Set the oled fade out feature to ON (value is the rate of fade 0-15)
    def fadeOnce(self,  value):
        self.sendCommand(0x80)        # set RE=1
        self.sendCommand(0x2A)

        self.sendCommand(0x80)        # set SD=1
        self.sendCommand(0x79)

        self.sendCommand(I2cCharDisplay.OLED_SETFADECOMMAND)
        self.sendCommand(I2cCharDisplay.OLED_FADEON | (0x0f & value))  # set fade feature to ON with a delay interval of value

        self.sendCommand(0x80)        # set SD=0
        self.sendCommand(0x78)

        self.sendCommand(0x80)        # set RE=0
        self.sendCommand(0x28)


    # Set the oled fade out feature to BLINK (value is the rate of fade 0-15)
    def fadeBlink(self,  value):
        self.sendCommand(0x80)        # set RE=1
        self.sendCommand(0x2A)

        self.sendCommand(0x80)        # set SD=1
        self.sendCommand(0x79)

        self.sendCommand(I2cCharDisplay.OLED_SETFADECOMMAND)
        self.sendCommand(I2cCharDisplay.OLED_FADEBLINK | (0x0f & value))  # set fade feature to BLINK with a delay interval of value

        self.sendCommand(0x80)        # set SD=0
        self.sendCommand(0x78)

        self.sendCommand(0x80)        # set RE=0
        self.sendCommand(0x28)


    # private functions ********************************

    def sendCommand(self,  value):
        if  (self._displayType == I2cCharDisplay.LCD_TYPE):
            self.sendLcdCommand(value)
        elif (self._displayType == I2cCharDisplay.OLED_TYPE):
            self.sendOledCommand(value)



    def sendData(self,  value):
        if  (self._displayType == I2cCharDisplay.LCD_TYPE):
            self.sendLcdData(value)
        elif (self._displayType == I2cCharDisplay.OLED_TYPE):
            self.sendOledData(value)



    # sendLcdByte - send one byte to the LCD module
    def sendLcdByte(self, value):
        try:
            i2c.write_byte(self._i2cAddress, value)
        except:
            pass



    # sendCommand - send command to the display
    # value is what is sent
    def sendLcdCommand(self,  value):
        # we need to break the value into 2 bytes, high nibble and a low nibble to send to lcd
        # and set the backlight bit which always need to be included.

        lowNibble = (value & 0xf0) | self._lcdBacklightControl | I2cCharDisplay.LCD_COMMAND
        highNibble = ((value << 4) & 0xf0) | self._lcdBacklightControl | I2cCharDisplay.LCD_COMMAND

        # write the byte of data to the display, 4 bits at a time

        self.sendLcdByte(lowNibble)      # write 4 bits with enable bit cleared
        self.sendLcdByte(lowNibble | I2cCharDisplay.LCD_ENABLEON)   # write 4 bits with enable bit set
        #sleep(.001)
        self.sendLcdByte(lowNibble)     # write 4 bits with enable bit cleared
        #sleep(.001)

        self.sendLcdByte(highNibble)      # write 4 bits with enable bit cleared
        self.sendLcdByte(highNibble | I2cCharDisplay.LCD_ENABLEON)   # write 4 bits with enable bit set
        #sleep(.001)
        self.sendLcdByte(highNibble)     # write 4 bits with enable bit cleared
        #sleep(.001)



    # sendData - send data to the display
    # value is what is sent
    def sendLcdData(self,  value):
        # we need to break the value into 2 bytes, high nibble and a low nibble to send to lcd
        # and set the backlight bit which always need to be included.
        lowNibble = (value & 0xf0) | self._lcdBacklightControl | I2cCharDisplay.LCD_DATA
        highNibble = ((value << 4) & 0xf0) | self._lcdBacklightControl | I2cCharDisplay.LCD_DATA

        # write the byte of data to the display, 4 bits at a time
        self.sendLcdByte(lowNibble)      # write 4 bits with enable bit cleared
        self.sendLcdByte(lowNibble | I2cCharDisplay.LCD_ENABLEON)   # write 4 bits with enable bit set
        #sleep(.001)
        self.sendLcdByte(lowNibble)     # write 4 bits with enable bit cleared
        #sleep(.001)

        self.sendLcdByte(highNibble)      # write 4 bits with enable bit cleared
        self.sendLcdByte(highNibble | I2cCharDisplay.LCD_ENABLEON)   # write 4 bits with enable bit set
        #sleep(.001)
        self.sendLcdByte(highNibble)     # write 4 bits with enable bit cleared
        #sleep(.001)



    # send an oled command
    def sendOledCommand(self,  value):
        try:
            i2c.write_byte_data(self._i2cAddress, I2cCharDisplay.OLED_COMMANDMODE,  value)
        except:
            pass
        sleep(.001)


    # send oled data
    def sendOledData(self,  value):
        try:
            i2c.write_byte_data(self._i2cAddress, I2cCharDisplay.OLED_DATAMODE,  value)
        except:
            pass
        sleep(.001)


    def oledBegin(self):
        sleep(.1)       # wait for the display to power up

        # begin OLED setup
        self.sendCommand(0x2A) # Set RE bit (RE=1, IS=0, SD=0)

        self.sendCommand(0x71) # Function Selection A
        self.sendData(0x5C)    # 5C = enable regulator (for 5V I/O), 00 = disable regulator (for 3.3V I/O)
                         #      Leave at 5C and then you can operate at either 3.3 or 5 volts.
                         #      The current draw of the regulator is minimal

        self.sendCommand(0x28) # Clear RE bit (RE=0, IS=0, SD=0)

        self.sendCommand(0x08) # Sleep Mode On (display, cursor & blink are off) during this setup

        self.sendCommand(0x2A) # Set RE bit (RE=1, IS=0, SD=0)
        self.sendCommand(0x79) # Set SD bit (RE=1, IS=0, SD=1)

        self.sendCommand(0xD5) # Set Display Clock Divide Ratio/ Oscillator Frequency
        self.sendCommand(0x70) #     set the Freq to 70h

        self.sendCommand(0x78) # Clear SD bit (RE=1, IS=0, SD=0)

        # Extended Function Set:
        if (self._rows > 2):
            self.sendCommand(0x09) # Set 5x8 chars, display inversion cleared, 3/4 line display
        else:
            self.sendCommand(0x08) # Set 5x8 chars, cursor inversion cleared, 1/2 line display

        self.sendCommand(0x06) # Set Advanced Entry Mode: COM0 -> COM31, SEG99 -> SEG0

        self.sendCommand(0x72) # Function Selection B:
        self.sendData(0x00)    #    Select ROM A and CGRAM 8 (which allows for custom characters)

        self.sendCommand(0x79) # Set SD bit  (RE=1, IS=0, SD=1)

        self.sendCommand(0xDA) # Set SEG Pins Hardware Configuration:
        self.sendCommand(0x10) #      Enable SEG Left, Seq SEG pin config

        self.sendCommand(0xDC) # Function Selection C
        self.sendCommand(0x00) #   Internal VSL, GPIO pin HiZ, input disabled

        self.sendCommand(0x81) # Set Contrast (brightness)
        self.sendCommand(0xFF) #       max value = 0xFF

        self.sendCommand(0xD9) # Set Phase Length
        self.sendCommand(0xF1) #       Phase 2 = 15(F), Phase 1 = 1   (power on = 0x78)

        self.sendCommand(0xDB) # set VCOMH deselect Level
        self.sendCommand(0x40) #       1 x Vcc  (previously 0x30)

        # Done with OLED Setup

        self.sendCommand(0x78)    # Clear SD bit  (RE=1, IS=0, SD=0)
        self.sendCommand(0x28)    # Clear RE and IS (RE=0, IS=0, SD=0)

        self.sendCommand(0x01)   # clear display
        self.sendCommand(0x80)   # Set DDRAM Address to 0x80 (line 1 start)

        sleep(.100)

        # send the function set command
        self._lcdFunctionSetCommand = I2cCharDisplay.LCD_1LINES | I2cCharDisplay.LCD_5x8DOTS
        if (self._rows > 1):
           self._lcdFunctionSetCommand |= I2cCharDisplay.LCD_2LINES

        self.sendCommand(I2cCharDisplay.LCD_FUNCTIONSETCOMMAND |self._lcdFunctionSetCommand)

        # send the display command
        # display on, no cursor and no blinking
        self._lcdDisplayControlCommand = I2cCharDisplay.LCD_DISPLAYON | I2cCharDisplay.LCD_CURSOROFF | I2cCharDisplay.LCD_CURSORBLINKOFF
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)

        # send the entry mode command
        self._lcdEntryModeCommand = I2cCharDisplay.LCD_DISPLAYLEFTTORIGHT | I2cCharDisplay.LCD_DISPLAYSHIFTOFF
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)

        # clear display and home cursor
        self.clear()
        self.home()



    def lcdBegin(self):
        # initialize the lcd
        sleep(.100)           # wait for lcd to power up

        # set all of the outputs on the PCA8574 chip to 0, except the backlight bit if on
        data = self._lcdBacklightControl
        self.sendLcdByte( data)
        sleep(1)

        # put lcd in 4 bit mode
        data = 0x30 | self._lcdBacklightControl
        self.sendLcdByte(data)
        # set the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEON)
        sleep(.001)
        # clear the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEOFF)
        sleep(.004300)  # wait min 4.1ms

        # put lcd in 4 bit mode again
        data = 0x30 | self._lcdBacklightControl
        self.sendLcdByte(data)
        # set the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEON)
        sleep(.001)
        # clear the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEOFF)
        sleep(.004300)  # wait min 4.1ms

        # put lcd in 4 bit mode again
        data = 0x30 | self._lcdBacklightControl
        self.sendLcdByte(data)
        # set the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEON)
        sleep(.001)
        # clear the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEOFF)
        sleep(.004300)  # wait min 4.1ms


        # set up 4 bit interface
        data = 0x20 | self._lcdBacklightControl
        self.sendLcdByte(data)
        # set the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEON)
        sleep(.001)
        # clear the enable bit and write again
        self.sendLcdByte(data | I2cCharDisplay.LCD_ENABLEOFF)
        sleep(.001)

        # send the function set command
        self._lcdFunctionSetCommand = I2cCharDisplay.LCD_4BITMODE | I2cCharDisplay.LCD_1LINES | I2cCharDisplay.LCD_5x8DOTS
        if self._rows > 1:
           self._lcdFunctionSetCommand |= I2cCharDisplay.LCD_2LINES
        self.sendCommand(I2cCharDisplay.LCD_FUNCTIONSETCOMMAND |self._lcdFunctionSetCommand)

        # send the display command
        # display on, no cursor and no blinking
        self._lcdDisplayControlCommand = I2cCharDisplay.LCD_DISPLAYON | I2cCharDisplay.LCD_CURSOROFF | I2cCharDisplay.LCD_CURSORBLINKOFF
        self.sendCommand(I2cCharDisplay.LCD_DISPLAYCONTROLCOMMAND |self._lcdDisplayControlCommand)

        # send the entry mode command
        self._lcdEntryModeCommand = I2cCharDisplay.LCD_DISPLAYLEFTTORIGHT | I2cCharDisplay.LCD_DISPLAYSHIFTOFF
        self.sendCommand(I2cCharDisplay.LCD_ENTRYMODECOMMAND |self._lcdEntryModeCommand)

        # clear display and home cursor
        self.clear()
        self.home()

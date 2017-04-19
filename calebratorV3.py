########################################################################
######################### The Calebrator 2000 ##########################
############################## Version 3 ###############################
########################################################################
## This is the code to the Calebrator 2000, a digital musical instru- ##
## ment designed by Caleb Long of Blackburn College for his senior    ##
## seminar project. The purpose of the Calebrator 2000 was to design  ##
## and build an instrument that is easy to play and inexpensive to    ##
## build. I happened to succeed and here is the brains of it. So      ##
## without further or do, here is the code...                         ##
########################################################################
########################################################################

from time import sleep
import RPi.GPIO as GPIO
# Make sure that you have gpiozero installed...
# First run "sudo apt-get update"
# Then run "sudo apt-get install python3-gpiozero"
# Or "sudo apt-get install python-gpiozero"
from gpiozero import Button, LED
import os
# Make sure you have this installed on the Pi that you are using
# To do so, download from...
# https://github.com/nwhitehead/pyfluidsynth/archive/master.zip
# Unzip and run, "sudo python setup.py install"
import fluidsynth
from subprocess import check_call
import glob
from Hover_library import Hover

########################################################################
############################# Device Setup #############################
########################################################################

# This is setting up the GPIO pins for use through RPi.GPIO. I don't
# think this necessarily needs to be included, but the Hover happens
# to use RPi.GPIO rather than using gpiozero. I threw it in because
# the script was throwing a lot of errors at me when I didn't include
# this. So here it will stay...
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Each of these values is the MIDI value for a specific note. All 12
# values are notes in Octave 4. I'm using them as reference values
# and if I want to get the notes in Octave 5 and 6, then I'll add 12
# or 24 respectively to the already define values here to get that
# note in the other octaves
noteC = 48
noteCS = 49
noteD = 50
noteDS = 51
noteE = 52
noteF = 53
noteFS = 54
noteG = 55
noteGS = 56
noteA = 57
noteAS = 58
noteB = 59

# Assigning buttons to GPIO pins. The parameter that is passed in when
# creating a new instance of Button() is the pin number that the button
# is connected to. The GPIO pin numbering system being used is BCM
# Button 1 = C
BUTTON1 = Button(27)
# Button 2 = C#
BUTTON2 = Button(22)
# Button 3 = D
BUTTON3 = Button(5)
# Button 4 = D#
BUTTON4 = Button(6)
# Button 5 = E
BUTTON5 = Button(13)
# Button 6 = F
BUTTON6 = Button(19)
# Button 7 = F#
BUTTON7 = Button(26)
# Button 8 = G
BUTTON8 = Button(18)
# Button 9 = G#
BUTTON9 = Button(23)
# Button 10 = A
BUTTON10 = Button(12)
# Button 11 = A#
BUTTON11 = Button(16)
# Button 12 = B
BUTTON12 = Button(20)
# The Power button. This bad boy will send the Calebrator into
# its shutdown cycle. However it will not turn the thing back
# on...
POWERBUTTON = Button(24)
# Assigning the octave switches to GPIO pins
# The first octave switch
SWITCH1 = Button(0)
# The second octave switch
SWITCH2 = Button(25)
# The third octave switch
SWITCH3 = Button(21)

# Assigning LED to GPIO pins. This light will turn on
# when the instrument is ready to be played
# Once again, the parameter provided to create a new instance
# of LED() is the pin number the LED is connected to.
blueStart = LED(14)

# Setting global boolean values. Each switch when set to "On"
# will be set to true. Each pitch key, when pressed, will look
# at these values to determine whether it should play notes in
# a specific octave or whether it should play any notes at all
global switch1_on
global switch2_on
global switch3_on

# Starting up fluidsynth
fs = fluidsynth.Synth()
# Telling fluidsynth to use the alsa sound driver because
# the Calebrator's sound card is alsa's default output
# device
fs.start(driver='alsa')

# Loading a SoundFont for fluidsynth to use
sfid = fs.sfload("guitar.sf2")
# Select the program with the desired SoundFont
fs.program_select(0, sfid, 0, 0)

# Creates instance of the Hover 2.0 to be used. There are three
# parameters that are passed in; the address (?) and the two
# general use GPIO pins that the Hover is attached to
hover = Hover(address=0x42, ts=4, reset=17)

########################################################################
######################### All of the commands ##########################
########################################################################

# Plays an instance of the C note. It uses the global variables created
# to determine if each octave switch is on. If it is, it plays the note
# in that respective octave.
def playButton1():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 48, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 60, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 72, 100)
	
# Stops the currently playing instance of the C note. Even though it
# would be unclear what notes are currently playing, it seemed like a
# safe bet to stop them all, even if they weren't.
def stopButton1():
	fs.noteoff(0, 48)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)
	
# Plays an instance of the C# note
def playButton2():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 49, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 61, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 73, 100)
	
# Stops the currently playing instance of the C# note
def stopButton2():
	fs.noteoff(0, 49)
	fs.noteoff(0, 61)
	fs.noteoff(0, 73)
	
# Plays an instance of the D note
def playButton3():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 50, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 62, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 74, 100)
	
# Stops the currently playing instance of the D note
def stopButton3():
	fs.noteoff(0, 50)
	fs.noteoff(0, 62)
	fs.noteoff(0, 74)

# Plays an instance of the D# note
def playButton4():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 51, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 63, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 75, 100)
	
# Stops the currently playing instance of the D# note
def stopButton4():
	fs.noteoff(0, 51)
	fs.noteoff(0, 63)
	fs.noteoff(0, 75)
	
# Plays an instance of the E note
def playButton5():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 52, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 64, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 76, 100)
	
# Stops the currently playing instance of the E note
def stopButton5():
	fs.noteoff(0, 52)
	fs.noteoff(0, 64)
	fs.noteoff(0, 76)
	
# Plays an instance of the F note
def playButton6():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 53, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 65, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 77, 100)
	
# Stops the currently playing instance of the F note
def stopButton6():
	fs.noteoff(0, 53)
	fs.noteoff(0, 65)
	fs.noteoff(0, 77)
	
# Plays an instance of the F# note
def playButton7():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 54, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 66, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 78, 100)
	
# Stops the currently playing instance of the F# note
def stopButton7():
	fs.noteoff(0, 54)
	fs.noteoff(0, 66)
	fs.noteoff(0, 78)
	
# Plays an instance of the G note
def playButton8():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 55, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 67, 100)

		
	if (switch3 == 1):
		fs.noteon(0, 79, 100)
	
# Stops the currently playing instance of the G note
def stopButton8():
	fs.noteoff(0, 55)
	fs.noteoff(0, 67)
	fs.noteoff(0, 79)
	
# Plays an instance of the G# note
def playButton9():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 56, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 68, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 80, 100)
		
# Stops the currently playing instance of the G# note
def stopButton9():
	fs.noteoff(0, 56)
	fs.noteoff(0, 68)
	fs.noteoff(0, 80)
	
# Plays an instance of the A note
def playButton10():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 57, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 69, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 81, 100)
	
# Stops the currently playing instance of the A note
def stopButton10():
	fs.noteoff(0, 57)
	fs.noteoff(0, 69)
	fs.noteoff(0, 81)
	
# Plays an instance of the A# note
def playButton11():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 58, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 70, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 82, 100)
	
# Stops the currently playing instance of the A# note
def stopButton11():
	fs.noteoff(0, 58)
	fs.noteoff(0, 70)
	fs.noteoff(0, 82)
	
# Plays an instance of the B note
def playButton12():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 59, 100)
		
	if (switch2 == 1):
		fs.noteon(0, 71, 100)
		
	if (switch3 == 1):
		fs.noteon(0, 83, 100)
	
# Stops the currently playing instance of the B note
def stopButton12():
	fs.noteoff(0, 59)
	fs.noteoff(0, 71)
	fs.noteoff(0, 83)

# Tells the user that they requested a shutdown. It does so
# by playing two notes in succession, serving as a warning.
def powerCheck():
	fs.noteon(0, 60, 100)
	sleep(0.5)
	fs.noteon(0, 72, 100)
	sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)
	
# Sets the global value that cooresponds to the switch to
# true, meaning that the notes that will be played will
# coorespond to watch switches are turned to "On"
def switch1_on():
	global switch1
	switch1 = 1
	
# Sets the value back to false when the switch is turned
# to "Off"
def switch1_off():
	global switch1
	switch1 = 0
	
def switch2_on():
	global switch2
	switch2 = 1
	
def switch2_off():
	global switch2
	switch2 = 0

def switch3_on():
	global switch3
	switch3 = 1
	
def switch3_off():
	global switch3
	switch3 = 0
	
# Runs through and checks the pitch keys and octave
# switches to see whether each one has been pressed
# or released. Each calls it's respective function
def checkPressedButtons():
	SWITCH1.when_pressed = switch1_on
	SWITCH1.when_released = switch1_off
	SWITCH2.when_pressed = switch2_on
	SWITCH2.when_released = switch2_off
	SWITCH3.when_pressed = switch3_on
	SWITCH3.when_released = switch3_off
	BUTTON1.when_pressed = playButton1
	BUTTON1.when_released = stopButton1
	BUTTON2.when_pressed = playButton2
	BUTTON2.when_released = stopButton2
	BUTTON3.when_pressed = playButton3
	BUTTON3.when_released = stopButton3
	BUTTON4.when_pressed = playButton4
	BUTTON4.when_released = stopButton4
	BUTTON5.when_pressed = playButton5
	BUTTON5.when_released = stopButton5
	BUTTON6.when_pressed = playButton6
	BUTTON6.when_released = stopButton6
	BUTTON7.when_pressed = playButton7
	BUTTON7.when_released = stopButton7
	BUTTON8.when_pressed = playButton8
	BUTTON8.when_released = stopButton8
	BUTTON9.when_pressed = playButton9
	BUTTON9.when_released = stopButton9
	BUTTON10.when_pressed = playButton10
	BUTTON10.when_released = stopButton10
	BUTTON11.when_pressed = playButton11
	BUTTON11.when_released = stopButton11
	BUTTON12.when_pressed = playButton12
	BUTTON12.when_released = stopButton12
	POWERBUTTON.when_pressed = powerCheck
	POWERBUTTON.when_released = shutdownCycle
	
# Closes out all of the instances of Button()
def closeButtons():
	BUTTON1.close()
	BUTTON2.close()
	BUTTON3.close()
	BUTTON4.close()
	BUTTON5.close()
	BUTTON6.close()
	BUTTON7.close()
	BUTTON8.close()
	BUTTON9.close()
	BUTTON10.close()
	BUTTON11.close()
	BUTTON12.close()
	POWERBUTTON.close()
	SWITCH1.close()
	SWITCH2.close()
	SWITCH3.close()
	
# Checks to see if the gesture pad has been interacted with
def checkGesture():
	# If the user interacted with it...
	if (hover.getStatus() == 0):
		# Figure out whether it was a touch or a gesture
		event = hover.getEvent()
		# If something happened, bend that pitch
		if event is not None:
			# It's important to note that the pitch is being
			# up a whole step
			fs.pitch_bend(0, 0 + 4096)
			sleep(.1)
			# Bends for a tenth of a second, then returns
			# to the default value
			fs.pitch_bend(0, 4096 - 4096)
		# Release the event, because you don't need it anymore
		hover.setRelease()
	
def startupCycle():
	# Light comes on indicating the Calebrator is ready to be played
	blueStart.on()
	# The light is then followed by notes playing to also indicate
	# that the Calebrator is ready to play. This might be a case of
	# "Wearing a belt and suspenders", but it's a nice touch.
	fs.noteon(0, 60, 100)
	sleep(0.5)
	fs.noteon(0, 72, 100)
	sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)

# This is what shuts down the Calebrator
def shutdownCycle():
	# Playing some notes, signifying that the Calebrator is shutting
	# down. Note that the notes being played are the same notes that
	# were played during the powerCheck() function, but in the
	# opposite order
	fs.noteon(0, 72, 100)
	sleep(0.5)
	fs.noteon(0, 60, 100)
	sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)
	# Deletes the instance of fluidsynth
	fs.delete()
	closeButtons()
	# Turns off the power light
	blueStart.off()
	# Shuts the bloody thing down
	check_call(['sudo', 'poweroff'])

########################################################################
####################### Where the magic happens... #####################
########################################################################	

# Going through the start up process...
startupCycle()

# Starting off by setting these values to false, because the
# octave switches should be set to "Off"
switch1 = 0
switch2 = 0
switch3 = 0

try:
	# Continuous Loop, this sucker runs until it doesn't
	while True:
		# Checks if the user is interacting with the gesture pad
		checkGesture()
		# Going through all of the buttons to check if they
		# have been pressed or if they've been released
		checkPressedButtons()
		sleep(0.1)

except KeyboardInterrupt:
	# Powers off the power light
	blueStart.off()
	# Deletes the instance of fluidsynth
	fs.delete()
	# Should delete the instance of the Hover. However,
	# I'm pretty sure this doesn't work...
	hover.end()
	
except:
	blueStart.off()
	fs.delete()
	hover.end()

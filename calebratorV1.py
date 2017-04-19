########################################################################
######################### The Calebrator 2000 ##########################
############################## Version 1 ###############################
########################################################################
## This is the code to the Calebrator 2000. No
########################################################################

from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Button, LED
import os
import fluidsynth
from subprocess import check_call
import glob
from Hover_library import Hover

########################################################################
############################# Device Setup #############################
########################################################################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Assigning buttons to GPIO pins
#Button 1 = C
BUTTON1 = Button(27)
#Button 2 = C#
BUTTON2 = Button(22)
#Button 3 = D
BUTTON3 = Button(5)
#Button 4 = D#
BUTTON4 = Button(6)
#Button 5 = E
BUTTON5 = Button(13)
#Button 6 = F
BUTTON6 = Button(19)
#Button 7 = F#
BUTTON7 = Button(26)
#Button 8 = G
BUTTON8 = Button(18)
#Button 9 = G#
BUTTON9 = Button(23)
#Button 10 = A
BUTTON10 = Button(12)
#Button 11 = A#
BUTTON11 = Button(16)
#Button 12 = B
BUTTON12 = Button(20)
#The Power button. This bad boy will turn off the Calebrator. However
# it will not turn it back on...
POWERBUTTON = Button(24)
#The first octave switch
SWITCH1 = Button(0)
#The second octave switch
SWITCH2 = Button(25)
#The third octave switch
SWITCH3 = Button(21)

#Assigning LED to GPIO pins. This light will turn on
#when the instrument is ready to be played
blueStart = LED(14)

#Setting global values that will 
global switch1_on
global switch2_on
global switch3_on

#Starting up fluidsynth
fs = fluidsynth.Synth()
#Telling fluidsynth to use the alsa sound driver because
#the Calebrator's sound card is alsa's default output
#device
fs.start(driver='alsa')

#NOTE: These print statements won't be seen unless a display
#is hooked up to the Calebrator via the HDMI port
print("Started FluidSynth")

#Loading a soundfont for fluidsynth to use
sfid = fs.sfload("guitar.sf2")
#Select the program with the desired soundfont
fs.program_select(0, sfid, 0, 0)

print("Loaded soundfont")

hover = Hover(address=0x42, ts=4, reset=17)

########################################################################
######################### All of the commands ##########################
########################################################################

#Plays an instance of the C note
def playButton1():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 48, 100)
		print("Button 1 (C4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 60, 100)
		print("Button 1 (C5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 72, 100)
		print("Button 1 (C6): On")
	
#Stops the currently playing instance of the C note
def stopButton1():
	fs.noteoff(0, 48)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)
	print("Button 1: Off")
	
#Plays an instance of the C# note
def playButton2():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 49, 100)
		print("Button 2 (C#4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 61, 100)
		print("Button 2 (C#5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 73, 100)
		print("Button 2 (C#6): On")
	
#Stops the currently playing instance of the C# note
def stopButton2():
	fs.noteoff(0, 49)
	fs.noteoff(0, 61)
	fs.noteoff(0, 73)
	print("Button 2: Off")
	
#Plays an instance of the D note
def playButton3():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 50, 100)
		print("Button 3 (D4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 62, 100)
		print("Button 3 (D5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 74, 100)
		print("Button 3 (D6): On")
	
#Stops the currently playing instance of the D note
def stopButton3():
	fs.noteoff(0, 50)
	fs.noteoff(0, 62)
	fs.noteoff(0, 74)
	print("Button 3: Off")

#Plays an instance of the D# note
def playButton4():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 51, 100)
		print("Button 4 (D#4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 63, 100)
		print("Button 4 (D#5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 75, 100)
		print("Button 4 (D#6): On")
	
#Stops the currently playing instance of the D# note
def stopButton4():
	fs.noteoff(0, 51)
	fs.noteoff(0, 63)
	fs.noteoff(0, 75)
	print("Button 4: Off")
	
#Plays an instance of the E note
def playButton5():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 52, 100)
		print("Button 5 (E4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 64, 100)
		print("Button 5 (E5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 76, 100)
		print("Button 5 (E6): On")
	
#Stops the currently playing instance of the E note
def stopButton5():
	fs.noteoff(0, 52)
	fs.noteoff(0, 64)
	fs.noteoff(0, 76)
	print("Button 5: Off")
	
#Plays an instance of the F note
def playButton6():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 53, 100)
		print("Button 6 (F4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 65, 100)
		print("Button 6 (F5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 77, 100)
		print("Button 6 (F6): On")
	
#Stops the currently playing instance of the F note
def stopButton6():
	fs.noteoff(0, 53)
	fs.noteoff(0, 65)
	fs.noteoff(0, 77)
	print("Button 6: Off")
	
#Plays an instance of the F# note
def playButton7():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 54, 100)
		print("Button 7 (F#4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 66, 100)
		print("Button 7 (F#5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 78, 100)
		print("Button 7 (F#6): On")
	
#Stops the currently playing instance of the F# note
def stopButton7():
	fs.noteoff(0, 54)
	fs.noteoff(0, 66)
	fs.noteoff(0, 78)
	print("Button 7: Off")
	
#Plays an instance of the G note
def playButton8():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 55, 100)
		print("Button 8 (G4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 67, 100)
		print("Button 8 (G5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 79, 100)
		print("Button 8 (G6): On")
	
#Stops the currently playing instance of the G note
def stopButton8():
	fs.noteoff(0, 55)
	fs.noteoff(0, 67)
	fs.noteoff(0, 79)
	print("Button 8: Off")
	
#Plays an instance of the G# note
def playButton9():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 56, 100)
		print("Button 9 (G#4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 68, 100)
		print("Button 9 (G#5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 80, 100)
		print("Button 9 (G#6): On")
		
#Stops the currently playing instance of the G# note
def stopButton9():
	fs.noteoff(0, 56)
	fs.noteoff(0, 68)
	fs.noteoff(0, 80)
	print("Button 9 (G#): Off")
	
#Plays an instance of the A note
def playButton10():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 57, 100)
		print("Button 10 (A4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 69, 100)
		print("Button 10 (A5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 81, 100)
		print("Button 10 (A6): On")
	
#Stops the currently playing instance of the A note
def stopButton10():
	fs.noteoff(0, 57)
	fs.noteoff(0, 69)
	fs.noteoff(0, 81)
	print("Button 10 (A): Off")
	
#Plays an instance of the A# note
def playButton11():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 58, 100)
		print("Button 11 (A#4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 70, 100)
		print("Button 11 (A#5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 82, 100)
		print("Button 11 (A#6): On")
	
#Stops the currently playing instance of the A# note
def stopButton11():
	fs.noteoff(0, 58)
	fs.noteoff(0, 70)
	fs.noteoff(0, 82)
	print("Button 11 (A#): Off")
	
#Plays an instance of the B note
def playButton12():
	global switch1
	global switch2
	global switch3
	if (switch1 == 1):
		fs.noteon(0, 59, 100)
		print("Button 12 (B4): On")
		
	if (switch2 == 1):
		fs.noteon(0, 71, 100)
		print("Button 12 (B5): On")
		
	if (switch3 == 1):
		fs.noteon(0, 83, 100)
		print("Button 12 (B6): On")
	
#Stops the currently playing instance of the B note
def stopButton12():
	fs.noteoff(0, 59)
	fs.noteoff(0, 71)
	fs.noteoff(0, 83)
	print("Button 12 (B): Off")

#Tells the user that they requested a shutdown. If they push the
# power button again, the Calebrator will go into the shutdown cycle	
def powerCheck():
	print("Shutdown requested")
	
def switch1_on():
	global switch1
	switch1 = 1
	print('s1-on')
	print(switch1)
	
def switch1_off():
	global switch1
	switch1 = 0
	print('s1-off')
	print(switch1)
	
def switch2_on():
	global switch2
	switch2 = 1
	print('s2-on')
	print(switch2)
	
def switch2_off():
	global switch2
	switch2 = 0
	print('s2-off')
	print(switch2)

def switch3_on():
	global switch3
	switch3 = 1
	print('s3-on')
	print(switch3)
	
def switch3_off():
	global switch3
	switch3 = 0
	print('s3-off')
	print(switch3)

def checkSwitches():
	SWITCH1.when_pressed = switch1_on
	SWITCH1.when_released = switch1_off
	SWITCH2.when_pressed = switch2_on
	SWITCH2.when_released = switch2_off
	SWITCH3.when_pressed = switch3_on
	SWITCH3.when_released = switch3_off
	
def closeSwitches():
	SWITCH1.close()
	SWITCH2.close()
	SWITCH3.close()
	
#Runs through the buttons to check whether each one has been
#pressed or released. Each calls it's respective function
def checkPressedButtons():
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
	
def checkGesture():
	if (hover.getStatus() == 0):
		event = hover.getEvent()
		if event is not None:
			fs.pitch_bend(0, 0 + 4096)
			sleep(.1)
			fs.pitch_bend(0, 4096 - 4096)
		hover.setRelease()
	
def startupCycle():
	#Light comes on indicating the Calebrator is ready to be played
	blueStart.on()
	#The light is then followed by notes playing to also indicate
	# that the Calebrator is ready to play. This might be a case of
	# "Wearing a belt and suspenders", but it's a nice touch.
	fs.noteon(0, 60, 100)
	sleep(0.5)
	fs.noteon(0, 72, 100)
	sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)

#This is what shuts down the Calebrator
def shutdownCycle():
	print("Shutting down the Calebrator...")
	#Playing some notes, signifying that the Calebrator is shutting
	# down
	fs.noteon(0, 72, 100)
	sleep(0.5)
	fs.noteon(0, 60, 100)
	sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 72)
	#Deletes the instance of fluidsynth
	fs.delete()
	closeButtons()
	closeSwitches()
	#Turns off the power light
	blueStart.off()
	#Shuts the bloody thing down
	check_call(['sudo', 'poweroff'])

########################################################################
####################### Where the magic happens... #####################
########################################################################	

startupCycle()

switch1 = 0
switch2 = 0
switch3 = 0

try:
	#Continuous Loop, this sucker runs until it doesn't
	while True:
		#Going through all 3 switches to check if any have been
		# turned on or off
		checkSwitches()
		checkGesture()
		#Going through all of the buttons to check if they
		#have been pressed or if they've been released
		checkPressedButtons()
		sleep(0.1)

except KeyboardInterrupt:
	blueStart.off()
	fs.delete()
	hover.end()
	
except:
	blueStart.off()
	fs.delete()
	hover.end()

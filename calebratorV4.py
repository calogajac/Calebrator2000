########################################################################
######################### The Calebrator 2000 ##########################
############################## Version 4 ###############################
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
########################## OctaveSwitch Class ##########################
########################################################################


class OctaveSwitch():
    def __init__(self, port):
        self.switch = Button(port)
        self.onVal = 0

    def set_on(self):
        self.onVal = 1
        return self.onVal

    def set_off(self):
        self.onVal = 0
        return self.onVal

    def get_on(self):
        return self.onVal


########################################################################
########################### PitchKey Class #############################
########################################################################

class PitchKey():
    def __init__(self, port, note):
        self.button = Button(port)
        self.note = note

    def get_note(self):
        return self.note

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

# Assigning buttons to GPIO pins. The parameter that is passed in when
# creating a new instance of Button() is the pin number that the button
# is connected to. The GPIO pin numbering system being used is BCM
# Button 1 = C
BUTTON1 = PitchKey(27, 48)
# Button 2 = C#
BUTTON2 = PitchKey(22, 49)
# Button 3 = D
BUTTON3 = PitchKey(5, 50)
# Button 4 = D#
BUTTON4 = PitchKey(6, 51)
# Button 5 = E
BUTTON5 = PitchKey(13, 52)
# Button 6 = F
BUTTON6 = PitchKey(19, 53)
# Button 7 = F#
BUTTON7 = PitchKey(26, 54)
# Button 8 = G
BUTTON8 = PitchKey(18, 55)
# Button 9 = G#
BUTTON9 = PitchKey(23, 56)
# Button 10 = A
BUTTON10 = PitchKey(12, 57)
# Button 11 = A#
BUTTON11 = PitchKey(16, 58)
# Button 12 = B
BUTTON12 = PitchKey(20, 59)
# The Power button. This bad boy will send the Calebrator into
# its shutdown cycle. However it will not turn the thing back
# on...
POWERBUTTON = Button(24)
# Assigning the octave switches to GPIO pins
# The first octave switch
SWITCH1 = OctaveSwitch(0)
# The second octave switch
SWITCH2 = OctaveSwitch(25)
# The third octave switch
SWITCH3 = OctaveSwitch(21)

# Assigning LED to GPIO pins. This light will turn on
# when the instrument is ready to be played
# Once again, the parameter provided to create a new instance
# of LED() is the pin number the LED is connected to.
blueStart = LED(14)

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
def play_button(note, switch1, switch2, switch3):
    if (switch1 == 1):
        fs.noteon(0, note, 100)

    if (switch2 == 1):
        fs.noteon(0, note + 12, 100)

    if (switch3 == 1):
        fs.noteon(0, note + 24, 100)
    return note


# Stops the currently playing instance of the C note. Even though it
# would be unclear what notes are currently playing, it seemed like a
# safe bet to stop them all, even if they weren't.
def stop_button(note):
    fs.noteoff(0, note)
    fs.noteoff(0, note + 12)
    fs.noteoff(0, note + 24)
    return note


# Tells the user that they requested a shutdown. It does so
# by playing two notes in succession, serving as a warning.
def power_check():
    fs.noteon(0, 60, 100)
    sleep(0.5)
    fs.noteon(0, 72, 100)
    sleep(0.5)
    fs.noteoff(0, 60)
    fs.noteoff(0, 72)


# Runs through and checks the pitch keys and octave
# switches to see whether each one has been pressed
# or released. Each calls it's respective function
def check_pressed_buttons():
    SWITCH1.switch.when_pressed = SWITCH1.set_on()
    SWITCH1.switch.when_released = SWITCH1.set_off()
    SWITCH2.switch.when_pressed = SWITCH2.set_on()
    SWITCH2.switch.when_released = SWITCH2.set_off()
    SWITCH2.switch.when_pressed = SWITCH2.set_on()
    SWITCH2.switch.when_released = SWITCH2.set_off()
    BUTTON1.button.when_pressed = \
        play_button(BUTTON1.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON1.button.when_released = stop_button(BUTTON1.get_note())
    BUTTON2.button.when_pressed = \
        play_button(BUTTON2.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON2.button.when_released = stop_button(BUTTON2.get_note())
    BUTTON3.button.when_pressed = \
        play_button(BUTTON3.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON3.button.when_released = stop_button(BUTTON3.get_note())
    BUTTON4.button.when_pressed = \
        play_button(BUTTON4.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON4.button.when_released = stop_button(BUTTON4.get_note())
    BUTTON5.button.when_pressed = \
        play_button(BUTTON5.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON5.button.when_released = stop_button(BUTTON5.get_note())
    BUTTON6.button.when_pressed = \
        play_button(BUTTON6.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON6.button.when_released = stop_button(BUTTON6.get_note())
    BUTTON7.button.when_pressed = \
        play_button(BUTTON7.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON7.button.when_released = stop_button(BUTTON7.get_note())
    BUTTON8.button.when_pressed = \
        play_button(BUTTON8.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON8.button.when_released = stop_button(BUTTON8.get_note())
    BUTTON9.button.when_pressed = \
        play_button(BUTTON9.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON9.button.when_released = stop_button(BUTTON9.get_note())
    BUTTON10.button.when_pressed = \
        play_button(BUTTON10.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON10.button.when_released = stop_button(BUTTON10.get_note())
    BUTTON11.button.when_pressed = \
        play_button(BUTTON11.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON11.button.when_released = stop_button(BUTTON11.get_note())
    BUTTON12.button.when_pressed = \
        play_button(BUTTON12.get_note(), SWITCH1.get_on(), SWITCH2.get_on(), SWITCH3.get_on())
    BUTTON12.button.when_released = stop_button(BUTTON12.get_note())
    POWERBUTTON.when_pressed = power_check
    POWERBUTTON.when_released = shutdown_cycle


# Closes out all of the instances of Button()
def close_hardware():
    BUTTON1.button.close()
    BUTTON2.button.close()
    BUTTON3.button.close()
    BUTTON4.button.close()
    BUTTON5.button.close()
    BUTTON6.button.close()
    BUTTON7.button.close()
    BUTTON8.button.close()
    BUTTON9.button.close()
    BUTTON10.button.close()
    BUTTON11.button.close()
    BUTTON12.button.close()
    POWERBUTTON.close()
    SWITCH1.switch.close()
    SWITCH2.switch.close()
    SWITCH3.switch.close()


# Checks to see if the gesture pad has been interacted with
def check_gesture():
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


def startup_cycle():
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
def shutdown_cycle():
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
    close_hardware()
    # Turns off the power light
    blueStart.off()
    # Shuts the bloody thing down
    check_call(['sudo', 'poweroff'])


########################################################################
####################### Where the magic happens... #####################
########################################################################

# Going through the start up process...
startup_cycle()

try:
    # Continuous Loop, this sucker runs until it doesn't
    while True:
        # Checks if the user is interacting with the gesture pad
        check_gesture()
        # Going through all of the buttons to check if they
        # have been pressed or if they've been released
        check_pressed_buttons()
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

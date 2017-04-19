########################################################################
######################### The Calebrator 2000 ##########################
############################## Version 2 ###############################
########################################################################
## This is the code to the Calebrator 2000. No
########################################################################

from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Button, LED
import fluidsynth
from subprocess import check_call
from Hover_library import Hover

########################################################################################################################
################################################## PitchKey Class ######################################################
########################################################################################################################

class PitchKey():
    def __init__(self, port, synth, note):
        self.button = Button(port)
        self.device = synth
        self.note = note

    def check(self, val1, val2, val3):
        self.button.when_pressed = self.play(val1, val2, val3)
        self.button.when_released = self.stop

    def play(self, val1, val2, val3):
        if val1 == 1:
            self.device.noteon(self.note)
        if val2 == 1:
            self.device.noteon(self.note + 12)
        if val3 == 1:
            self.device.noteon(self.note + 24)

    def stop(self):
        self.device.noteoff(self.note)
        self.device.noteoff(self.note + 12)
        self.device.noteoff(self.note + 24)

    def close(self):
        self.button.close()

########################################################################################################################
################################################## PowerButton Class ###################################################
########################################################################################################################

class PowerButton():
    def __init__(self, port):
        self.button = Button(port)

    def check(self):
        self.button.when_pressed = self.warning()
        self.button.when_released = self.shutdown()

    def warning(self):
        print("Shutdown Requested")

    def shutdown(self):
        print("Shutting down the Calebrator...")
        fs.noteon(0, 72, 100)
        sleep(0.5)
        fs.noteon(0, 60, 100)
        sleep(0.5)
        fs.noteoff(0, 60)
        fs.noteoff(0, 72)
        shutdownCycle()

    def close(self):
        self.button.close()

########################################################################################################################
################################################## GesturePad Class ####################################################
########################################################################################################################

class GesturePad():
    def __init__(self, synth):
        self.hover = Hover(address=0x42, ts=4, reset=17)
        self.device = synth

    def close(self):
        self.hover.end()

    def check(self):
        if self.hover.getStatus() == 0:
            event = self.hover.getEvent()
            if event is not None:
                self.device.pitch_bend(0, 0 + 4096)
                sleep(1)
                self.device.pitch_bend(0, 4096 - 4096)
            self.hover.setRelease()

########################################################################################################################
################################################## Device Setup ########################################################
########################################################################################################################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Assigning buttons to GPIO pins
# Button 1 = C

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

blueStart = LED(14)
print("Blue Light On")

fs = fluidsynth.Synth()
fs.start(driver='alsa')
sfid = fs.sfload("guitar.sf2")
fs.program_select(0, sfid, 0, 0)

BUTTON_C = PitchKey(27, fs, noteC)
# Button 2 = C#
BUTTON_CS = PitchKey(22, fs, noteCS)
# Button 3 = D
BUTTON_D = PitchKey(5, fs, noteD)
# Button 4 = D#
BUTTON_DS = PitchKey(6, fs, noteDS)
# Button 5 = E
BUTTON_E = PitchKey(13, fs, noteE)
# Button 6 = F
BUTTON_F = PitchKey(19, fs, noteF)
# Button 7 = F#
BUTTON_FS = PitchKey(26, fs, noteFS)
# Button 8 = G
BUTTON_G = PitchKey(18, fs, noteG)
# Button 9 = G#
BUTTON_GS = PitchKey(23, fs, noteGS)
# Button 10 = A
BUTTON_A = PitchKey(12, fs, noteA)
# Button 11 = A#
BUTTON_AS = PitchKey(16, fs, noteAS)
# Button 12 = B
BUTTON_B = PitchKey(20, fs, noteB)
# The Power button. This bad boy will turn off the Calebrator. However
# it will not turn it back on...
#POWERBUTTON = PowerButton(24)
# The first octave switch
SWITCH1 = OctaveSwitch(0)
# The second octave switch
SWITCH2 = OctaveSwitch(25)
# The third octave switch
SWITCH3 = OctaveSwitch(21)

GESTURE_PAD = GesturePad(fs)
########################################################################
######################### All of the commands ##########################
########################################################################

# Tells the user that they requested a shutdown. If they push the
# power button again, the Calebrator will go into the shutdown cycle

def closeSwitches():
    SWITCH1.close()
    SWITCH2.close()
    SWITCH3.close()
# Runs through the buttons to check whether each one has been
# pressed or released. Each calls it's respective function
def checkPressedButtons():
    BUTTON_C.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_CS.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_D.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_DS.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_E.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_F.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_FS.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_G.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_GS.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_A.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_AS.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    BUTTON_B.check(SWITCH1.getOn(), SWITCH2.getOn(), SWITCH3.getOn())
    #POWERBUTTON.check()

def closeButtons():
    BUTTON_C.close()
    BUTTON_CS.close()
    BUTTON_D.close()
    BUTTON_DS.close()
    BUTTON_E.close()
    BUTTON_F.close()
    BUTTON_FS.close()
    BUTTON_G.close()
    BUTTON_GS.close()
    BUTTON_A.close()
    BUTTON_AS.close()
    BUTTON_B.close()
    #POWERBUTTON.close()

def startupCycle():
    blueStart.on()
    fs.noteon(0, 60, 100)
    sleep(0.5)
    fs.noteon(0, 72, 100)
    sleep(0.5)
    fs.noteoff(0, 60)
    fs.noteoff(0, 72)


# This is what shuts down the Calebrator
def shutdownCycle():
    closeButtons()
    closeSwitches()
    # Turns off the power light
    blueStart.off()
    # Shuts the bloody thing down
    check_call(['sudo', 'poweroff'])


########################################################################
####################### Where the magic happens... #####################
########################################################################

startupCycle()

try:
    while True:
        GESTURE_PAD.check()
        checkPressedButtons()
        sleep(0.1)

except KeyboardInterrupt:
    blueStart.off()
    fs.delete()
    closeSwitches()
    closeButtons()
    GESTURE_PAD.close()

except:
    blueStart.off()
    fs.delete()
    closeSwitches()
    closeButtons()
    GESTURE_PAD.close()



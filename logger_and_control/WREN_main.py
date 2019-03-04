import os
from WREN_logger import LT_logger
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import WREN_shared
from WREN_graphics import Gui
import queue
import WREN_weighpad


'''Get system stuff '''
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
guisize = str(screensize[0]-2)+'x'+str(int(screensize[1]/2))
dirpath = os.path.realpath(__file__)
print(dirpath)

''' Define queue to contain events'''

states_queue = queue.Queue()


''' Define functions to handle phidgets events'''

def FindMySpot(self):
    ch_sn = self.getDeviceSerialNumber()
    ch_chnum = self.getChannel()
    try:
        loglist_id = WREN_shared.ch_map.index(ch_sn)+ ch_chnum
        if loglist_id > len(WREN_shared.ch_map) - 1:
            print("Attempted to map device signal out of list boundary")
            print("Serial number: {}".format(ch_sn))
            print("Channel number: {}".format(ch_chnum))
            print("Attempted to write to location {}".format(loglist_id))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
        else:
            return loglist_id
        

    except ValueError:
        print("Could not find device serial number in ch_map")
        print("Serial number: {}".format(ch_sn))
        print("Available in map: {}".format(WREN_shared.ch_map))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def FindMySpot_skinny(ch_sn, ch_chnum):
    try:
        print(ch_sn)
        print(ch_chnum)
        loglist_id = WREN_shared.ch_map.index(ch_sn) + ch_chnum
        if loglist_id > len(WREN_shared.ch_map) - 1:
            print("Attempted to map device signal out of list boundary")
            print("Serial number: {}".format(ch_sn))
            print("Channel number: {}".format(ch_chnum))
            print("Attempted to write to location {}".format(loglist_id))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
        else:
            return loglist_id


    except ValueError:
        print("Could not find device serial number in ch_map")
        print("Serial number: {}".format(ch_sn))
        print("Available in map: {}".format(WREN_shared.ch_map))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def addtoQueue(myspot, command):
    global states_queue
    commandID = WREN_shared.states_spots_key.get(str(myspot))
    if commandID:
        states_queue.put([commandID,command])


def TemperatureSensorAttached(self):
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("\n")
        myspot = FindMySpot(self)
        try:
            addtoQueue(myspot,True)
            WREN_shared.ch_states[myspot] = True
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def TemperatureSensorDetached(self):
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        myspot = FindMySpot(detached)
        try:
            addtoQueue(myspot,False)
            WREN_shared.ch_states[myspot] = False
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def ErrorEvent(self, eCode, description):
    print("Error %i : %s" % (eCode, description))


def TemperatureChangeHandler(self, temperature):
    myspot = FindMySpot(self)
    WREN_shared.ch_data[myspot] = temperature


def VoltageRatioInputAttached(self):
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("\n")
        myspot = FindMySpot(attached)
        try:
            addtoQueue(myspot,True)
            WREN_shared.ch_states[myspot] = True
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def VoltageRatioInputDetached(self):
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        myspot = FindMySpot(detached)
        try:
            addtoQueue(myspot,False)
            WREN_shared.ch_states[myspot] = False
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(WREN_shared.ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def VoltageRatioChangeHandler(self, voltageRatio):
    myspot = FindMySpot(self)
    WREN_shared.ch_data[myspot] = voltageRatio


def StepperAttached(self):
    global stepper_connected
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("\n")
        print("\n Setting up channel parameters")
        set_stepper_params(attached)
        stepper_connected = True
        addtoQueue("stp","attached")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def set_stepper_params(self):
    ''' Put here all initialisation for stepper motor parameters
    '''
    stp_scalefactor = 0.001
    print("\nSetting stepper scale factor to %.2f" % stp_scalefactor)
    self.setRescaleFactor(stp_scalefactor)


def StepperDetached(self):
    global stepper_connected
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        addtoQueue('stp','detached')
        stepper_connected = False
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def PositionChangeHandler(self, position):
    WREN_shared.stepper_position = position


def StepperStoppedHandler(self):
    addtoQueue('stp','stopped')
    WREN_shared.stepper_moving = False

def DCMotorAttached(e):
    try:
        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("\n")
        sn = attached.getDeviceSerialNumber()
        if sn == 146593:
            addtoQueue('dc1','attached')
            print("dc 1 attached")
        elif sn == 146812:
            addtoQueue('dc2', 'attached')
            print("dc 2 attached")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def DCMotorDetached(e):
    detached = e
    try:
        sn = detached.getDeviceSerialNumber()
        if sn == 146593:
            addtoQueue('dc1','detached')
        elif sn == 146812:
            addtoQueue('dc2', 'detached')
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def EncoderAttached(self):
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("\n")
        if(not(self.getEnabled())):
            self.setEnabled(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def EncoderDetached(self):
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def EncoderPositionChangeHandler(self, positionChange, timeChange, indexTriggered):
    sn = self.getDeviceSerialNumber()
    if sn==146593:
        WREN_shared.DC1_pos_feedback = WREN_shared.DC1_pos_feedback + positionChange
    elif sn== 146812:
        WREN_shared.DC2_pos_feedback = WREN_shared.DC2_pos_feedback + positionChange


''' Create channels and do all work to initialise and open them'''
print("Point 1")
try:
    # Open channels for all voltage ratio inputs (16 of them)
    vr_channels = [VoltageRatioInput() for _ in range(16)]

    # Open temperature channel
    t_channels = [TemperatureSensor() for _ in range(1)]

    # Create stepper channel
    stp_channel = Stepper()

    # Create DC motors channels
    dc_channels = [DCMotor(), DCMotor()]

    # Create encoders channels
    enc_channels = [Encoder(), Encoder()]

    print("Point 2")
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

# Assign event handlers to all channels and open them
try:
    for x in vr_channels:
        x.setOnAttachHandler(VoltageRatioInputAttached)
        x.setOnDetachHandler(VoltageRatioInputDetached)
        x.setOnErrorHandler(ErrorEvent)
        x.setOnVoltageRatioChangeHandler(VoltageRatioChangeHandler)
        # Set channel and device serial number to ANY
        x.setChannel(-1)
        x.setDeviceSerialNumber(-1)

    for x in t_channels:
        x.setOnAttachHandler(TemperatureSensorAttached)
        x.setOnDetachHandler(TemperatureSensorDetached)
        x.setOnErrorHandler(ErrorEvent)
        x.setOnTemperatureChangeHandler(TemperatureChangeHandler)

    for x in dc_channels:
        x.setOnAttachHandler(DCMotorAttached)
        x.setOnDetachHandler(DCMotorDetached)
        x.setChannel(-1)
        x.setDeviceSerialNumber(-1)

    for x in enc_channels:
        x.setOnAttachHandler(EncoderAttached)
        x.setOnDetachHandler(EncoderDetached)
        x.setOnErrorHandler(ErrorEvent)
        x.setOnPositionChangeHandler(EncoderPositionChangeHandler)
        x.setChannel(-1)
        x.setDeviceSerialNumber(-1)

    stp_channel.setOnAttachHandler(StepperAttached)
    stp_channel.setOnDetachHandler(StepperDetached)
    stp_channel.setOnErrorHandler(ErrorEvent)
    stp_channel.setOnPositionChangeHandler(PositionChangeHandler)
    stp_channel.setDeviceSerialNumber(WREN_shared.stp_serial)
    stp_channel.setOnStoppedHandler(StepperStoppedHandler)

    print("Point 4")

    print("Open phidget channels")
    for x in vr_channels:
        x.open()
    for x in t_channels:
        x.open()
    for x in dc_channels:
        x.open()
    for x in enc_channels:
        x.open()

    stp_channel.open()

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

#####################################
#####################################
# Finished setting up the phidget stuff
# Create logger and GUI now
#####################################

wp = WREN_weighpad.weighpad_handler(1,3,states_queue)
wp.connect_WFE()

logger_set = []
logger_labels = []
for x in WREN_shared.logger_config:
    print(x)
    itemspot = FindMySpot_skinny(x[0], x[1])
    logger_set.append(itemspot)
    logger_labels.append(x[2])
print(logger_labels)
print(logger_set)
log = LT_logger(WREN_shared.ch_data, 5, 10, logger_set, logger_labels)

gui = Gui(WREN_shared.ch_data, WREN_shared.ch_states, stp_channel, log,states_queue,wp)

''' Do cleanup after GUI has been closed'''
print("Cleaning up")
try:
    for x in vr_channels:
        x.close()
    for x in t_channels:
        x.close()
    for x in dc_channels:
        x.close()
    stp_channel.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

print("Cleaned up")

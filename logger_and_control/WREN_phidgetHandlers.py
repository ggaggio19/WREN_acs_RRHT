from Phidget22.Net import *
import WREN_shared
import queue

''' Define queue to contain events'''

states_queue = queue.Queue()

''' Define functions to handle phidgets events'''


def FindMySpot(self):
    ch_sn = self.getDeviceSerialNumber()
    ch_chnum = self.getChannel()
    try:
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
        states_queue.put([commandID, command])


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
            addtoQueue(myspot, True)
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
            addtoQueue(myspot, False)
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
            addtoQueue(myspot, True)
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
            addtoQueue(myspot, False)
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
        addtoQueue("stp", "attached")

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
        addtoQueue('stp', 'detached')
        stepper_connected = False
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def PositionChangeHandler(self, position):
    WREN_shared.stepper_position = position


def StepperStoppedHandler(self):
    addtoQueue('stp', 'stopped')
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
            addtoQueue('dc1', 'attached')
            WREN_shared.DC1_cmd_connected = True
            print("dc 1 attached")
        elif sn == 146812:
            addtoQueue('dc2', 'attached')
            WREN_shared.DC2_cmd_connected = True
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
            WREN_shared.DC1_cmd_connected = False
            addtoQueue('dc1', 'detached')
        elif sn == 146812:
            WREN_shared.DC2_cmd_connected = False
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
        sn = attached.getDeviceSerialNumber()
        if sn == 146593:
            WREN_shared.DC1_enc_connected = True
        elif sn == 146812:
            WREN_shared.DC2_enc_connected = True
        if (not (self.getEnabled())):
            self.setEnabled(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def EncoderDetached(self):
    detached = self
    sn = detached.getDeviceSerialNumber()
    if sn == 146593:
        WREN_shared.DC1_enc_connected = False
    elif sn == 146812:
        WREN_shared.DC2_enc_connected = False
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def EncoderPositionChangeHandler(self, positionChange, timeChange, indexTriggered):
    sn = self.getDeviceSerialNumber()
    if sn == 146593:
        WREN_shared.DC1_pos_feedback = WREN_shared.DC1_pos_feedback + positionChange
    elif sn == 146812:
        WREN_shared.DC2_pos_feedback = WREN_shared.DC2_pos_feedback + positionChange


def DCVelocityUpdateHandler(self, velocity):
    sn = self.getDeviceSerialNumber()
    if sn == 146593:
        WREN_shared.DC1_vel_feedback = velocity
    elif sn == 146812:
        WREN_shared.DC2_vel_feedback = velocity
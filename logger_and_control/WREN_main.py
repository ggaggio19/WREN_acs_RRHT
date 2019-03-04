import os
from WREN_logger import LT_logger
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Net import *
import WREN_shared
from WREN_graphics import Gui
import WREN_weighpad
import WREN_revcounter
import WREN_PIDcontrol
from WREN_phidgetHandlers import states_queue as states_queue
from WREN_phidgetHandlers import FindMySpot_skinny as FindMySpot_skinny
from WREN_phidgetHandlers import TemperatureSensorAttached as TemperatureSensorAttached
from WREN_phidgetHandlers import TemperatureSensorDetached as TemperatureSensorDetached
from WREN_phidgetHandlers import ErrorEvent as ErrorEvent
from WREN_phidgetHandlers import TemperatureChangeHandler as TemperatureChangeHandler
from WREN_phidgetHandlers import VoltageRatioInputAttached as VoltageRatioInputAttached
from WREN_phidgetHandlers import VoltageRatioInputDetached as VoltageRatioInputDetached
from WREN_phidgetHandlers import VoltageRatioChangeHandler as VoltageRatioChangeHandler
from WREN_phidgetHandlers import StepperAttached as StepperAttached
from WREN_phidgetHandlers import StepperDetached as StepperDetached
from WREN_phidgetHandlers import PositionChangeHandler as PositionChangeHandler
from WREN_phidgetHandlers import StepperStoppedHandler as StepperStoppedHandler
from WREN_phidgetHandlers import DCMotorAttached as DCMotorAttached
from WREN_phidgetHandlers import DCMotorDetached as DCMotorDetached
from WREN_phidgetHandlers import EncoderAttached as EncoderAttached
from WREN_phidgetHandlers import EncoderDetached as EncoderDetached
from WREN_phidgetHandlers import EncoderPositionChangeHandler as EncoderPositionChangeHandler
from WREN_phidgetHandlers import DCVelocityUpdateHandler as DCVelocityUpdateHandler


'''Get system stuff '''
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
guisize = str(screensize[0]-2)+'x'+str(int(screensize[1]/2))
dirpath = os.path.realpath(__file__)
print(dirpath)



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

    dccount = 1
    for x in dc_channels:
        x.setOnAttachHandler(DCMotorAttached)
        x.setOnDetachHandler(DCMotorDetached)
        x.setOnVelocityUpdateHandler(DCVelocityUpdateHandler)
        x.setChannel(-1)
        if dccount == 1:
            x.setDeviceSerialNumber(146593)
        elif dccount == 2:
            x.setDeviceSerialNumber(146812)

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

wfe_place = WREN_shared.mapped_channels.index('wfe')
wp = WREN_weighpad.weighpad_handler(1,3,states_queue,wfe_place)
wp.connect_WFE()

n_place = WREN_shared.mapped_channels.index('n')
np = WREN_revcounter.revcount_handler(10,5,states_queue,n_place)
np.connect_N()

# Create PID controllers
DC1_controller = WREN_PIDcontrol.PID_run_Thread(10,1,1,0,0,0,dc_channels[0])
DC2_controller = WREN_PIDcontrol.PID_run_Thread(10,2,1,0,0,0,dc_channels[1])

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

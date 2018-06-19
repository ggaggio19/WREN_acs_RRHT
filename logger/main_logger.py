from time import sleep
import os
from random import randint
from random import uniform
import threading
from LT_logger import LT_logger
import ctypes
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import tkinter
from tkinter import ttk

'''Get system stuff '''
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
guisize = str(screensize[0]-2)+'x'+str(int(screensize[1]/2))
dirpath = os.path.realpath(__file__)
print(dirpath)

'''Define variables used for management of phidget data'''
# Hub board
hub_vi = [178866]*8
# Thermocouple input
tc_i = [118257]
# DC motor 1 and 2
dcm1_vi = [146593]*2
dcm2_vi = [146812]*2
# Stepper motor controller
stm_di = [267223]*4
# Create full lists for logging (concatenate all previous lists, repeat those that have more than one kind of input)
ch_map = hub_vi*2 + tc_i + dcm1_vi*2 + dcm2_vi*2 + stm_di

ch_states = [False]*len(ch_map)
ch_data = [0.0]*len(ch_map)

''' Define GUI object class '''

class Gui(object):
    def __init__(self, allvalues, allstates):
        ''' Variables links'''
        self.allvalues = allvalues
        self.currstates = allstates
        self.laststates = allstates[:]
        
        ''' Gui objects '''
        ''' Main window'''
        self.root = tkinter.Tk()
        self.root.title("Test monitor")
        
        self.mainframe = ttk.Frame(self.root, padding ="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.statusSTR = tkinter.StringVar()
        self.statusSTR.set("Ready")
        
        ''' Build the iterables to manage gui visualisation'''
        # Labels of two rows
        gui_labels_r1 = ['TAMB','PAMB','PTOT','DP','TTOT']
        gui_labels_r2 = ['FN1','FN2','FN3','FN4', 'WFE']
        # Define correspondence of channels to GUI slots
        gui_l_slot_r1 = [178866, 178867, 178868, 178869, 118257]
        gui_l_slot_r2 = [178870, 178871, 178872, 178873]
        
        ''' Labels for all items '''
        # First column labels
        self.lab01 = ttk.Label(self.mainframe,text = gui_labels_r1[0],background="red")
        self.lab02 = ttk.Label(self.mainframe,text = gui_labels_r1[1],background="red")
        self.lab03 = ttk.Label(self.mainframe,text = gui_labels_r1[2],background="red")
        self.lab04 = ttk.Label(self.mainframe,text = gui_labels_r1[3],background="red")
        self.lab05 = ttk.Label(self.mainframe,text = gui_labels_r1[4],background="red")
        self.lab01.grid(column=0,row=0,sticky=tkinter.S)
        self.lab02.grid(column=0,row=1,sticky=tkinter.S)
        self.lab03.grid(column=0,row=2,sticky=tkinter.S)
        self.lab04.grid(column=0,row=3,sticky=tkinter.S)
        self.lab05.grid(column=0,row=4,sticky=tkinter.S)
        
        # Second column labels
        self.lab11 = ttk.Label(self.mainframe,text = gui_labels_r2[0],background="red")
        self.lab12 = ttk.Label(self.mainframe,text = gui_labels_r2[1],background="red")
        self.lab13 = ttk.Label(self.mainframe,text = gui_labels_r2[2],background="red")
        self.lab14 = ttk.Label(self.mainframe,text = gui_labels_r2[3],background="red")
        self.lab15 = ttk.Label(self.mainframe,text = gui_labels_r2[4],background="red")
        self.lab11.grid(column=2,row=0,sticky=tkinter.S)
        self.lab12.grid(column=2,row=1,sticky=tkinter.S)
        self.lab13.grid(column=2,row=2,sticky=tkinter.S)
        self.lab14.grid(column=2,row=3,sticky=tkinter.S)
        self.lab15.grid(column=2,row=4,sticky=tkinter.S)
        
        ''' Create items to display data values'''
        self.DispVal01 = tkinter.StringVar()
        self.DispVal02 = tkinter.StringVar()
        self.DispVal03 = tkinter.StringVar()
        self.DispVal04 = tkinter.StringVar()
        self.DispVal05 = tkinter.StringVar()
        self.DispVal11 = tkinter.StringVar()
        self.DispVal12 = tkinter.StringVar()
        self.DispVal13 = tkinter.StringVar()
        self.DispVal14 = tkinter.StringVar()
        self.DispVal15 = tkinter.StringVar()

        # Initialise at 0
        self.DispVal01.set('%.2f' % 0)
        self.DispVal02.set('%.2f' % 0)
        self.DispVal03.set('%.2f' % 0)
        self.DispVal04.set('%.2f' % 0)
        self.DispVal05.set('%.2f' % 0)
        self.DispVal11.set('%.2f' % 0)
        self.DispVal12.set('%.2f' % 0)
        self.DispVal13.set('%.2f' % 0)
        self.DispVal14.set('%.2f' % 0)
        self.DispVal15.set('%.2f' % 0)
        
        ''' Create labels for values '''
        ttk.Label(self.mainframe,textvariable = self.DispVal01).grid(column=1,row=0,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal02).grid(column=1,row=1,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal03).grid(column=1,row=2,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal04).grid(column=1,row=3,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal05).grid(column=1,row=4,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal11).grid(column=3,row=0,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal12).grid(column=3,row=1,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal13).grid(column=3,row=2,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal14).grid(column=3,row=3,sticky=tkinter.S)
        ttk.Label(self.mainframe,textvariable = self.DispVal15).grid(column=3,row=4,sticky=tkinter.S)

        ''' Active buttons'''
        self.btn_start = ttk.Button(self.mainframe, text="Start transient log")
        self.btn_stop = ttk.Button(self.mainframe, text="Stop transient log")
        self.btn_Pscan = ttk.Button(self.mainframe, text="Take P scan")
        
        self.btn_start.grid(column=5, row=3, sticky=tkinter.W)
        self.btn_stop.grid(column=5, row=4, sticky=tkinter.W)
        self.btn_stop.state(['disabled'])
        self.btn_Pscan.grid(column=6, row=3, sticky=tkinter.W)
        
        self.btn_stop.configure(command = self.stopTR_callback)
        self.btn_start.configure(command = self.startTR_callback)
        self.btn_Pscan.configure(command = self.TakePscan_callback)
        
        ''' Status text '''
        ttk.Label(self.mainframe,textvariable = self.statusSTR).grid(column=5,row=7,sticky=(tkinter.S,tkinter.E))
        
        ''' Pack all up '''
        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        ''' Create logger '''
        self.log = LT_logger(self.allvalues, 5, 10)
        
        ''' Setup updater functions '''
        self.root.after(500,self.updater)
        self.root.after(1000,self.col_updater)
        
        ''' Start GUI'''
        self.mainframe.mainloop()
        
    def updater(self):
        sinks = [self.DispVal01, self.DispVal02, self.DispVal03, self.DispVal04, self.DispVal05, self.DispVal11, self.DispVal12, self.DispVal13, self.DispVal14, self.DispVal15]
        sources = [(self.allvalues[0] * 5 * 44.444 - 61.111), (self.allvalues[1] * 36.2595 + 1.45038), (self.allvalues[2] * 36.2595 + 1.45038), (self.allvalues[3] * 8.05 - 4.0277), self.allvalues[16], self.allvalues[4], self.allvalues[5], self.allvalues[6], self.allvalues[7], self.allvalues[8]]
        vcount = 0
        for _ in sinks:
            sinks[vcount].set('%.2f' % sources[vcount])
            vcount = vcount + 1
        self.root.after(500,self.updater)
        
    def col_updater(self):
        st_count = 0
        sinks = [self.lab01, self.lab02, self.lab03, self.lab04, self.lab05, self.lab11, self.lab12, self.lab13, self.lab14, self.lab15]
        sources = [self.currstates[0], self.currstates[1], self.currstates[2], self.currstates[3], self.currstates[16], self.currstates[4], self.currstates[5], self.currstates[6], self.currstates[7], self.currstates[8]]
        for _ in sources:
            if not(sources[st_count] == self.laststates[st_count]):
                if sources[st_count]:
                    sinks[st_count].config(background="green")
                else:
                    sinks[st_count].config(background="red")
            st_count = st_count + 1
        self.laststates = sources
        self.root.after(1000,self.col_updater)
        
    def startTR_callback(self):
        self.log.start_TR_shot(timeout=60)
        self.statusSTR.set("Transient log started")
        self.btn_stop.state(['!disabled'])
        self.btn_start.state(['disabled'])


    def stopTR_callback(self):
        self.log.stop_TR_shot()
        self.btn_stop.state(['disabled'])
        self.btn_start.state(['!disabled'])
        self.statusSTR.set("Transient log stopped \nSaving data")
    
    def TakePscan_callback(self):
        self.statusSTR.set("Taking P scan...")
        self.log.start_P_scan()
        self.btn_start.state(['disabled'])
        self.btn_Pscan.state(['disabled'])
        threading.Timer(self.log.Ptime, self.end_Pscan).start()
        
    def end_Pscan(self):
        self.log.end_P_scan()
        self.btn_start.state(['!disabled'])
        self.btn_Pscan.state(['!disabled'])
        self.statusSTR.set("P scan complete \nSaving data")
        
''' Define functions to handle phidgets events'''

def FindMySpot(self):
    ch_sn = self.getDeviceSerialNumber()
    ch_chnum = self.getChannel()
    try:
        loglist_id = ch_map.index(ch_sn) + ch_chnum
        if loglist_id > len(ch_map) - 1:
            print("Attempted to map device signal out of list boundary")
            print("Serial number: {}".format(ch_sn))
            print("Channel number: {}".format(ch_chnum))
            print("Attempted to write to location {}".format(loglist_id))
            print("Size of data storage list: {}".format(len(ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
        else:
            return loglist_id

    except ValueError:
        print("Could not find device serial number in ch_map")
        print("Serial number: {}" .format(ch_sn))
        print("Available in map: {}" .format(ch_map))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)
        
def TemperatureSensorAttached(self):
    global ch_states
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
            ch_states[myspot] = True
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(ch_map)))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)
        
        
def TemperatureSensorDetached(self):
    global ch_states
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        myspot = FindMySpot(detached)
        try:
            ch_states[myspot] = False
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(ch_map)))
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
    ch_data[myspot] = temperature
    
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
            ch_states[myspot] = True
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(ch_map)))
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
            ch_states[myspot] = True
        except IndexError:
            print("Attempted to map device signal out of list boundary")
            print("Attempted to write to location {}".format(myspot))
            print("Size of data storage list: {}".format(len(ch_map)))
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
    ch_data[myspot] = voltageRatio
    
''' Create channels and do all work to initialise and open them'''
print("Point 1")
try:
    # Open channels for all voltage ratio inputs (16 of them)
    vr_channels = [VoltageRatioInput() for _ in range(16)]

    # Open temperature channel
    t_channels = [TemperatureSensor() for _ in range(1)]
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

    print("Point 4")

    print("Open phidget channels")
    for x in vr_channels:
        x.open()
    for x in t_channels:
        x.open()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

#####################################
#####################################
# Finished setting up the phidget stuff - create GUI now
#####################################

gui = Gui(ch_data, ch_states)

''' Do cleanup after GUI has been closed'''
print("Cleaning up")
try:
    for x in vr_channels:
        x.close()
    for x in t_channels:
        x.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

print("Cleaned up")

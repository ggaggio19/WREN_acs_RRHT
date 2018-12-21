import tkinter
from tkinter import ttk
import threading
import WREN_shared

bue
class Gui(object):
    def __init__(self, allvalues, allstates, stepperchan, log_in,queuein, WFEHandler):
        ''' Variables links'''
        self.allvalues = allvalues
        self.currstates = allstates
        self.laststates = allstates[:]
        self.queuein = queuein

        ''' Channel links'''
        self.stepperchan = stepperchan

        ''' Connect logger '''
        self.log = log_in

        ''' Connect WFE handler thread'''
        self.WFEHandler = WFEHandler

        ''' Gui objects '''
        ''' Main window'''
        self.root = tkinter.Tk()
        self.root.title("Test monitor")

        '''Data logger frame'''
        ttk.Label(self.root, text="Data Logger").grid(column=0, row=0, sticky=(tkinter.S, tkinter.W))
        self.mainframe = ttk.Frame(self.root, padding ="3 3 12 12")
        self.mainframe.grid(column=0, row=1, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.statusSTR = tkinter.StringVar()
        self.statusSTR.set("Ready")


        ''' Stepper frame '''
        ttk.Label(self.root, text="Stepper motor").grid(column=1, row=0, sticky=(tkinter.S, tkinter.W))
        self.stepframe = ttk.Frame(self.root, padding ="3 3 12 12")
        self.stepframe.grid(column=1, row=1, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.stepframe.columnconfigure(0, weight=1)
        self.stepframe.rowconfigure(0, weight=1)

        ''' DC 1'''
        ttk.Label(self.root, text="DC motor 1").grid(column=0, row=2, sticky=(tkinter.N, tkinter.W))
        self.dc1frame = ttk.Frame(self.root, padding ="3 3 12 12")
        self.dc1frame.grid(column=0, row=3, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.dc1frame.columnconfigure(0, weight=1)
        self.dc1frame.rowconfigure(0, weight=1)

        ''' DC 2'''
        ttk.Label(self.root, text="DC motor 2").grid(column=1, row=2, sticky=(tkinter.N, tkinter.W))
        self.dc2frame = ttk.Frame(self.root, padding ="3 3 12 12")
        self.dc2frame.grid(column=1, row=3, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.dc2frame.columnconfigure(0, weight=1)
        self.dc2frame.rowconfigure(0, weight=1)


        ''' #########################################################################
        Here starts the data logger frame build
        #############################################################################'''

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
        self.btn_Pscan = ttk.Button(self.mainframe, text="Take SS scan")
        #self.link_wp = ttk.Button(self.mainframe, text="Connect WFE")
        
        self.btn_start.grid(column=5, row=3, sticky=tkinter.W)
        self.btn_stop.grid(column=5, row=4, sticky=tkinter.W)
        self.btn_stop.state(['disabled'])
        self.btn_Pscan.grid(column=6, row=3, sticky=tkinter.W)
        #self.link_wp.grid(column=6, row=4, sticky=tkinter.W)
        
        self.btn_stop.configure(command = self.stopTR_callback)
        self.btn_start.configure(command = self.startTR_callback)
        self.btn_Pscan.configure(command = self.TakePscan_callback)
        #self.link_wp.configure(command=self.LinkWFE_callback)
        
        ''' Status text '''
        ttk.Label(self.mainframe,textvariable = self.statusSTR).grid(column=5,row=7,sticky=(tkinter.S,tkinter.E))
        
        ''' Pack all up '''
        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


        '''#################################################################################################
        End of data logger frame build
        ################################################################################################'''

        ''' ###############################################################################################
        Start of stepper motor control frame build
        ###############################################################################################'''

        ''' Build buttons'''
        self.btn_engage = ttk.Button(self.stepframe, text="Engage")
        self.btn_setzero = ttk.Button(self.stepframe, text="Set 0 position")
        self.btn_gotopos = ttk.Button(self.stepframe, text="Go to position")
        self.btn_minus5 = ttk.Button(self.stepframe, text="-5")
        self.btn_minus1 = ttk.Button(self.stepframe, text="-1")
        self.btn_plus1 = ttk.Button(self.stepframe, text="+1")
        self.btn_plus5 = ttk.Button(self.stepframe, text="+5")

        ''' Position buttons'''
        self.btn_engage.grid(column=0, row=1, columnspan = 2, sticky=tkinter.W)
        self.btn_setzero.grid(column=0, row=5, columnspan=4, sticky=tkinter.W)
        self.btn_gotopos.grid(column=0, row=3, columnspan=2, sticky=tkinter.W)
        self.btn_minus5.grid(column=0, row=4, sticky=tkinter.W)
        self.btn_minus1.grid(column=1, row=4, sticky=tkinter.W)
        self.btn_plus1.grid(column=2, row=4, sticky=tkinter.W)
        self.btn_plus5.grid(column=3, row=4, sticky=tkinter.W)

        ''' Support flag'''
        self.steppercontrolenabled = False

        ''' Create labels '''
        ''' Unplugged/stopped/moving'''
        self.step_move_lab = ttk.Label(self.stepframe,text = "Unplugged",background="red")
        self.step_move_lab.grid(column=3,row=1,columnspan = 2, sticky=(tkinter.S,tkinter.E))
        '''Current position '''
        ttk.Label(self.stepframe, text="Current position").grid(column=0, row=2, columnspan=2,
                                                                   sticky=(tkinter.S, tkinter.W))
        self.step_pos = tkinter.StringVar()
        self.step_pos.set('%.2f' % 0)
        ttk.Label(self.stepframe,textvariable = self.step_pos).grid(column=2,row=2,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Create input '''
        self.step_gotopos = tkinter.IntVar()
        self.step_goto_input = ttk.Entry(self.stepframe,textvariable = self.step_gotopos)
        self.step_goto_input.grid(column=2,row=3,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Set button callbacks'''
        self.btn_engage.configure(command=self.stepper_engage)
        self.btn_setzero.configure(command=self.stepper_setzero)
        self.btn_gotopos.configure(command=self.stepper_gototarget)
        self.btn_minus5.configure(command=lambda : self.stepper_changetarget(-5))
        self.btn_minus1.configure(command=lambda : self.stepper_changetarget(-1))
        self.btn_plus1.configure(command=lambda : self.stepper_changetarget(1))
        self.btn_plus5.configure(command=lambda : self.stepper_changetarget(5))

        ''' Disable all inputs until stepper is connected'''
        self.btn_engage.state(['disabled'])
        self.btn_setzero.state(['disabled'])
        self.btn_gotopos.state(['disabled'])
        self.btn_minus5.state(['disabled'])
        self.btn_minus1.state(['disabled'])
        self.btn_plus1.state(['disabled'])
        self.btn_plus5.state(['disabled'])
        self.step_goto_input.state(['disabled'])

        ''' Pack all up '''
        for child in self.stepframe.winfo_children(): child.grid_configure(padx=3, pady=1)

        ''' ###############################################################################################
         Start of DC motor 1 control frame build
         ###############################################################################################'''

        ''' Build buttons'''
        self.btn_dc1_setzero = ttk.Button(self.dc1frame, text="Set 0 position")
        self.btn_dc1_gotopos = ttk.Button(self.dc1frame, text="Go to position")

        ''' Position buttons'''
        self.btn_dc1_setzero.grid(column=0, row=5, columnspan=4, sticky=tkinter.W)
        self.btn_dc1_gotopos.grid(column=0, row=3, columnspan=2, sticky=tkinter.W)

        '''Current position '''
        ttk.Label(self.dc1frame, text="Current position").grid(column=0, row=2, columnspan=2,
                                                                   sticky=(tkinter.S, tkinter.W))
        self.dc1_pos = tkinter.StringVar()
        self.dc1_pos.set('%.2f' % 0)
        ttk.Label(self.dc1frame,textvariable = self.dc1_pos).grid(column=2,row=2,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        '''Current status'''
        self.dc1state_lab = ttk.Label(self.dc1frame,text = "Unplugged",background="red")
        self.dc1state_lab.grid(column=2,row=5,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Create input '''
        self.dc1_gotopos = tkinter.IntVar()
        self.dc1_goto_input = ttk.Entry(self.dc1frame,textvariable = self.dc1_gotopos)
        self.dc1_goto_input.grid(column=2,row=3,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Disable all inputs until DC1 is connected'''
        self.btn_dc1_setzero.state(['disabled'])
        self.btn_dc1_gotopos.state(['disabled'])
        self.dc1_goto_input.state(['disabled'])

        ''' Pack all up '''
        for child in self.dc1frame.winfo_children(): child.grid_configure(padx=3, pady=1)

        ''' ###############################################################################################
         Start of DC motor 2 control frame build
         ###############################################################################################'''

        ''' Build buttons'''
        self.btn_dc2_setzero = ttk.Button(self.dc2frame, text="Set 0 position")
        self.btn_dc2_gotopos = ttk.Button(self.dc2frame, text="Go to position")

        ''' Position buttons'''
        self.btn_dc2_setzero.grid(column=0, row=5, columnspan=4, sticky=tkinter.W)
        self.btn_dc2_gotopos.grid(column=0, row=3, columnspan=2, sticky=tkinter.W)

        '''Current position '''
        ttk.Label(self.dc2frame, text="Current position").grid(column=0, row=2, columnspan=2,
                                                                   sticky=(tkinter.S, tkinter.W))
        self.dc2_pos = tkinter.StringVar()
        self.dc2_pos.set('%.2f' % 0)
        ttk.Label(self.dc2frame,textvariable = self.dc2_pos).grid(column=2,row=3,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        '''Current status'''
        self.dc2state_lab = ttk.Label(self.dc2frame,text = "Unplugged",background="red")
        self.dc2state_lab.grid(column=2,row=5,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Create input '''
        self.dc2_gotopos = tkinter.IntVar()
        self.dc2_goto_input = ttk.Entry(self.dc2frame,textvariable = self.dc2_gotopos)
        self.dc2_goto_input.grid(column=2,row=3,columnspan = 2, sticky=(tkinter.S,tkinter.E))

        ''' Disable all inputs until DC2 is connected'''
        self.btn_dc2_setzero.state(['disabled'])
        self.btn_dc2_gotopos.state(['disabled'])
        self.dc2_goto_input.state(['disabled'])

        ''' Pack all up '''
        for child in self.dc2frame.winfo_children(): child.grid_configure(padx=3, pady=1)

        ''' Setup updater functions '''
        self.root.after(500,self.updater)

        ''' Start GUI'''
        self.mainframe.mainloop()
        
    def updater(self):
        valsinks = [self.DispVal01, self.DispVal02, self.DispVal03, self.DispVal04, self.DispVal05, self.DispVal11, self.DispVal12, self.DispVal13, self.DispVal14, self.DispVal15]
        labsinks = [self.lab01, self.lab02, self.lab03, self.lab04, self.lab05, self.lab11, self.lab12, self.lab13,
                 self.lab14, self.lab15]
        sources = [(self.allvalues[0] * 5 * 44.444 - 61.111), (self.allvalues[1] * 36.2595 + 1.45038), (self.allvalues[2] * 36.2595 + 1.45038), (self.allvalues[3] * 8.05 - 4.0277), self.allvalues[16], self.allvalues[4] * 1000, self.allvalues[5], self.allvalues[6], self.allvalues[7], self.allvalues[len(self.allvalues)-1]]
        vcount = 0
        for _ in valsinks:
            valsinks[vcount].set('%.2f' % sources[vcount])
            vcount = vcount + 1

        self.step_pos.set('%.2f' % WREN_shared.stepper_position)

        ''' If weighpad is not connected, try connection'''
        #if not WREN_shared.WFE_IsConnected:
            #self.WFEHandler.connect_WFE()

        ''' Now empty the queue'''
        while not self.queuein.empty():
            cmd_in = self.queuein.get()
            posid = cmd_in[0]
            cmd_spec = cmd_in[1]
            if posid == 'stp':
                if cmd_spec == 'attached':
                    self.enable_stepperengage()
                elif cmd_spec == 'detached':
                    self.disable_steppercontrol()
                elif cmd_spec == 'stopped':
                    if self.steppercontrolenabled:
                        self.step_move_lab.config(text="Ready")
                        self.step_move_lab.config(background="blue")
            elif posid == 'dc1':
                if cmd_spec == 'attached':
                    self.enable_DCcontrol(1)

                elif cmd_spec == 'detached':
                    self.disable_DCcontrol(1)

            elif posid == 'dc2':
                if cmd_spec == 'attached':
                    self.enable_DCcontrol(2)
                elif cmd_spec == 'detached':
                    self.disable_DCcontrol(2)
            elif posid == "wfe":
                if cmd_spec:
                    labsinks[9].config(background="green")
                    #self.link_wp.state(['disabled'])
                else:
                    labsinks[9].config(background="red")
                    #self.link_wp.state(['!disabled'])
            else:
                if cmd_spec:
                    print(posid)
                    labsinks[posid-1].config(background="green")
                else:
                    labsinks[posid-1].config(background="red")

        self.root.after(500,self.updater)

        
    def startTR_callback(self):
        self.log.start_TR_shot(timeout=300)
        self.statusSTR.set("Transient log started")
        self.btn_stop.state(['!disabled'])
        self.btn_start.state(['disabled'])


    def stopTR_callback(self):
        self.log.stop_TR_shot()
        self.btn_stop.state(['disabled'])
        self.btn_start.state(['!disabled'])
        self.statusSTR.set("Transient log stopped \nSaving data")
    
    def TakePscan_callback(self):
        self.statusSTR.set("Taking SS scan...")
        self.log.start_P_scan()
        self.btn_start.state(['disabled'])
        self.btn_Pscan.state(['disabled'])
        threading.Timer(self.log.Ptime, self.end_Pscan).start()
        
    def end_Pscan(self):
        self.log.end_P_scan()
        self.btn_start.state(['!disabled'])
        self.btn_Pscan.state(['!disabled'])
        self.statusSTR.set("SS scan complete \nSaving data")

    def enable_steppercontrol(self):
        self.btn_gotopos.state(['!disabled'])
        self.btn_minus5.state(['!disabled'])
        self.btn_minus1.state(['!disabled'])
        self.btn_plus1.state(['!disabled'])
        self.btn_plus5.state(['!disabled'])
        self.step_goto_input.state(['!disabled'])
        self.step_move_lab.config(text = "Ready")
        self.step_move_lab.config(background="blue")
        self.steppercontrolenabled = True

    def enable_stepperengage(self):
        WREN_shared.stepper_position = 0.0
        self.btn_engage.state(['!disabled'])
        self.btn_setzero.state(['!disabled'])
        self.step_move_lab.config(text = "Not engaged")
        self.step_move_lab.config(background="orange")

    def disable_steppercontrol(self):
        WREN_shared.stepper_position = 0.0
        self.btn_engage.state(['disabled'])
        self.btn_setzero.state(['disabled'])
        self.btn_gotopos.state(['disabled'])
        self.btn_minus5.state(['disabled'])
        self.btn_minus1.state(['disabled'])
        self.btn_plus1.state(['disabled'])
        self.btn_plus5.state(['disabled'])
        self.step_goto_input.state(['disabled'])
        self.step_move_lab.config(text = "Unplugged")
        self.step_move_lab.config(background="red")
        self.steppercontrolenabled = False

    def disable_steppercontrol_minor(self):
        self.btn_gotopos.state(['disabled'])
        self.btn_minus5.state(['disabled'])
        self.btn_minus1.state(['disabled'])
        self.btn_plus1.state(['disabled'])
        self.btn_plus5.state(['disabled'])
        self.step_goto_input.state(['disabled'])
        self.step_move_lab.config(text = "Not engaged")
        self.step_move_lab.config(background="orange")
        self.steppercontrolenabled = False

    def stepper_engage(self):
        # Qua ci va la roba che gli fa fare engage
        self.stepperchan.setEngaged(1)
        self.enable_steppercontrol()
        self.btn_engage.configure(command=self.stepper_disengage,text="Disengage")

    def stepper_disengage(self):
        # Qua ci va la roba che gli fa fare disengage
        self.stepperchan.setEngaged(0)
        self.disable_steppercontrol_minor()
        self.btn_engage.configure(command=self.stepper_engage,text="Engage")

    def stepper_setzero(self):
        # Qua ci va la roba che gli fa azzerare la posizione
        offset = self.stepperchan.getPosition()
        self.stepperchan.addPositionOffset(-offset)
        WREN_shared.stepper_position = 0.0
        self.step_pos.set('%.2f' % 0)

    def stepper_gototarget(self):
        curr_target_position = self.step_gotopos.get()
        print(curr_target_position)
        # qua ci va la roba che manda il motore nella posizione richiesta
        self.stepperchan.setTargetPosition(curr_target_position)
        WREN_shared.stepper_moving = True
        self.step_move_lab.config(text = "Moving")
        self.step_move_lab.config(background="green")

    def stepper_changetarget(self,delta):
        print(delta)
        curr_target_position = WREN_shared.stepper_position + delta
        # qua ci va la roba che manda il motore nella posizione richiesta
        self.stepperchan.setTargetPosition(curr_target_position)
        WREN_shared.stepper_moving = True
        self.step_move_lab.config(text = "Moving")
        self.step_move_lab.config(background="green")

    def enable_DCcontrol(self,dcnum):
        if dcnum == 1:
            self.btn_dc1_setzero.state(['!disabled'])
            self.btn_dc1_gotopos.state(['!disabled'])
            self.dc1_goto_input.state(['!disabled'])
            self.dc1state_lab.config(background="green")
            self.dc1state_lab.config(text="Connected")
        elif dcnum == 2:
            self.btn_dc2_setzero.state(['!disabled'])
            self.btn_dc2_gotopos.state(['!disabled'])
            self.dc2_goto_input.state(['!disabled'])
            self.dc2state_lab.config(background="green")
            self.dc2state_lab.config(text="Connected")

    def disable_DCcontrol(self,dcnum):
        if dcnum==1:
            self.btn_dc1_setzero.state(['disabled'])
            self.btn_dc1_gotopos.state(['disabled'])
            self.dc1_goto_input.state(['disabled'])
            self.dc1state_lab.config(background="red")
            self.dc1state_lab.config(text="Unplugged")
        elif dcnum == 2:
            self.btn_dc2_setzero.state(['disabled'])
            self.btn_dc2_gotopos.state(['disabled'])
            self.dc2_goto_input.state(['disabled'])
            self.dc2state_lab.config(background="red")
            self.dc2state_lab.config(text="Unplugged")

    def LinkWFE_callback(self):
        self.WFEHandler.connect_WFE()





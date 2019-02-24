import time
import serial
import WREN_shared
import threading

class REVReaderThread (threading.Thread):

    def __init__(self,rate, comp, queue,isconnected,place):
        super().__init__()
        self.comp = comp
        self.queue = queue
        self.isconnected = isconnected
        self.daemon = True
        self.place = place
        if rate > 30:
            self.rate = 30
        else:
            self.rate = rate

    def run(self):
        self.timestep = 1/float(self.rate)

        while True:
            try:
                '''
                First line is for Mac. Second line for Win.
                '''
                #        print 1
             #   ser = serial.Serial(port='/dev/tty.usbmodem1411', baudrate=115200)
                ser = serial.Serial(port='COM'+str(self.comp),baudrate=115200)
                self.isconnected.set()
                WREN_shared.N_IsConnected = True
                self.queue.put(["n", True])
            except serial.SerialException:
                WREN_shared.N_IsConnected = False
                self.queue.put(["n", False])
                return None
            except TypeError as e:
                ser.close()
                WREN_shared.N_IsConnected = False
                self.queue.put(["n", False])
                return None

            time1 = time.time()
            rpm_all=''
            rpm = 0

            while self.isconnected.is_set():
                time.sleep(self.timestep * 0.8)

                while (time.time() - time1) < self.timestep:
                    pass
                try:
                    rpm_all = ser.read(ser.inWaiting())

                    if '\n' in rpm_all:
                        rpm_list = rpm_all.split('\n')  # Guaranteed to have at least 2 entries
                    #                    print('Time: ' + str(time1))
                    else:
                        rpm_list = [rpm, rpm]
                    rpm = rpm_list[-2]
                    #                rpm = ser.readline()  Not robust: keep waiting
                    try:
                        rpm = float(rpm)
                        WREN_shared.ch_data[self.place] = rpm
                    except ValueError as e:
                        rpm = 0
                except serial.SerialException:
                    self.isconnected.clear()
                    WREN_shared.N_IsConnected = False
                    self.queue.put(["n", False])
                except TypeError as e:
                    ser.close()
                    self.isconnected.clear()
                    WREN_shared.N_IsConnected = False
                    self.queue.put(["n", False])
                except IOError as e:
                    ser.close()
                    self.isconnected.clear()
                    WREN_shared.N_IsConnected = False
                    self.queue.put(["n", False])

                time1 = time.time()


class revcount_handler:

    def __init__(self,rate, comp, queue,place):
        self.rate = rate
        self.comp = comp
        self.queue = queue
        self.place = place
        self.isConnected = threading.Event()


    def connect_N(self):
        self.isConnected.clear()
        self.reader = REVReaderThread(self.rate, self.comp, self.queue,self.isConnected, self.place)
        self.reader.start()
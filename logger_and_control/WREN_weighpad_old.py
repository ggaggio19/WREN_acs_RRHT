import serial
import time
import WREN_shared
import threading


class WFEReaderThread (threading.Thread):

    def __init__(self,rate, comp, queue,isconnected):
        super().__init__()
        self.rate = rate
        self.comp = comp
        self.queue = queue
        self.isconnected = isconnected
        self.daemon = True

    def run(self):
        timestep = 1 / float(self.rate)

        try:
            ser = serial.Serial(port='COM' + str(self.comp), baudrate=9600)
        except serial.SerialException:
            self.isconnected.clear()
            WREN_shared.WFE_IsConnected = False
            self.queue.put(["wfe", False])
            return None
        except TypeError as e:
            ser.close()
            self.isconnected.clear()
            WREN_shared.WFE_IsConnected = False
            self.queue.put(["wfe", False])
            return None

        self.isconnected.set()
        WREN_shared.WFE_IsConnected = True
        self.queue.put(["wfe", True])

        i = 0

        while self.isconnected.is_set():

            try:
                weight = str(ser.readline())
            except serial.SerialException:
                self.isconnected.clear()
                WREN_shared.WFE_IsConnected = False
                self.queue.put(["wfe", False])
            except TypeError as e:
                ser.close()
                self.isconnected.clear()
                WREN_shared.WFE_IsConnected = False
                self.queue.put(["wfe", False])

            if i == 0:
                i = i + 1
                time2 = time.clock()
                time1 = time2
                try:
                    w2 = float(weight[10:15])
                except ValueError as e:
                    w2 = 0
                WREN_shared.mapped_ch_data[5] = 0
            else:
                time2 = time.clock()
                if (time2 - time1) > timestep:
                    w1 = w2
                    try:
                        w2 = float(weight[9:14])
                    except ValueError as e:
                        w2 = 0
                    WREN_shared.mapped_ch_data[5] = (w1 - w2) / (time2 - time1)
                    time1 = time2


class weighpad_handler:

    def __init__(self,rate, comp, queue):
        self.rate = rate
        self.comp = comp
        self.queue = queue
        self.isConnected = threading.Event()


    def connect_WFE(self):
        self.isConnected.clear()
        self.reader = WFEReaderThread(self.rate, self.comp, self.queue,self.isConnected)
        self.reader.start()




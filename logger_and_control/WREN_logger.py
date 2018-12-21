import time
import threading
import datetime
import os
import WREN_shared



def data_postproc(data_in, selection):
    conv_data = []
    for x in data_in:
        slice = x[1:]
        selected = []
        for k in selection:
            selected.append(slice[k])

        x_let = WREN_shared.applyLets(selected)
        tmp = [x[0]]+x_let
        conv_data.append(tmp)
    return conv_data


def data_postproc_P(data_in, selection):
    avg_data = [0]*(len(data_in[0])-1)
    points_num = len(data_in)
    for x in data_in:
        slice = x[1:]
        selected = []
        for k in selection:
            selected.append(slice[k])
        tmp = WREN_shared.applyLets(x[1:])
        y = 0
        for _ in tmp:
            avg_data[y] = avg_data[y] + tmp[y]
            y = y + 1
            
    y = 0    
    for _ in avg_data:
        avg_data[y] = avg_data[y]/points_num
        y = y+1
    return avg_data


def savetofile(filename, data, path, labels = None):
    if labels is None:
        print("Labels not specified - defaulting to dummy values")
        labels = 'a'*len(data[1])
    else:
        labels = ['TIME']+labels

    labels_str = str(labels[0])
    for lj in labels[1:]:
        labels_str = labels_str + ","
        labels_str = labels_str + str(lj)

    labels_str = labels_str+"\n"

    print('Saving to csv file...')
    success = False
    tryname = path + "\\"+ filename + ".csv"
    while not(success):
        with open(tryname,"w") as csvfile:
            # Write header
            csvfile.write(labels_str)
            # Write data
            for x in data:
                xstr = str('%.3f' % x[0])
                for xval in x[1:]:
                    xstr = xstr + "," + ('%.3f' % xval)
                xstr = xstr + "\n"
                csvfile.write(xstr)
        success = True

def savetofile_P(filename, data, path, labels = None):
    if labels is None:
        print("Labels not specified - defaulting to dummy values")
        labels = 'a'*len(data[1])

    labels_str = str(labels[0])
    for lj in labels[2:]:
        labels_str = labels_str + ","
        labels_str = labels_str + str(lj)

    labels_str = labels_str+"\n"

    print('Saving to csv file...')
    success = False
    tryname = path + "\\"+ filename + ".csv"
    while not(success):
        with open(tryname,"w") as csvfile:
            # Write header
            csvfile.write(labels_str)
            # Write data
            xstr = str('%.3f' % data[0])
            for xval in data[1:]:
                xstr = xstr + "," + ('%.3f' % xval)
            xstr = xstr + "\n"
            csvfile.write(xstr)
        success = True

class logger_base(threading.Thread):
    tolerance = 0.0005

    def __init__(self,dt, values, storage, stopper,timeout,subset):
        super().__init__()
        self.storage = storage
        self.values = values
        self.dt = dt
        self.stopper = stopper
        self.storage.append([0]+values)
        self.timeout = timeout
        self.subset = subset

    def run(self):
        ST_firstpass = time.perf_counter()
        while not self.stopper.is_set():
            st = time.perf_counter()
            time.sleep(self.dt / 2)
            while(time.perf_counter()-st) < self.dt + self.tolerance:
                pass
            self.storage.append([time.perf_counter()-ST_firstpass]+self.values)
            if time.perf_counter() - ST_firstpass > self.timeout:
                print("Log timed out")
                self.stopper.set()
                print("Saving data to timeout file")
                convdata = data_postproc(self.storage, self.subset)
                savetofile("Timed_out_TLOG", convdata)



class LT_logger:

    def __init__(self, target, TR_scanrate, SS_scanT, selection, labels=None):
        if TR_scanrate > 100:
            print('Transient recording rate capped at 100 Hz')
            self.TR_dt = 0.001
        else:
            self.TR_dt = 1/TR_scanrate

        if SS_scanT > 30:
            print('P scan duration capped at 30s')
            self.Ptime = 30
        else:
            self.Ptime = SS_scanT

        if not(labels):
            self.labels = ['TAMB', 'PAMB', 'PTOT', 'DP', 'FN1', 'FN2', 'FN3', 'FN4', 'TTOT']
        else:
            self.labels = labels

        self.values = target
        self.subset = selection
        if not(len(self.subset)==len(self.labels)):
            print("WARNING - variables and labels list size do not match!")

        self.values_storage = []
        self.TLOG_timestamp = []
        self.Pscan_timestamp = []
        self.TLOGstopper = threading.Event()
        self.Pscanstopper = threading.Event()
        self.savepath = os.path.dirname(os.path.abspath(__file__))

    def setlabels(self,newlabels):
        self.labels = newlabels
        if not(len(self.values)==len(self.labels)):
            print("WARNING - variables and labels list size do not match!")

    def set_timers(self, newTR, newSS):
        if newTR > 100:
            print('Transient recording rate capped at 100 Hz')
            self.TR_dt = 0.001
        else:
            self.TR_dt = 1/newTR

        if newSS > 30:
            print('P scan duration capped at 30s')
            self.Ptime = 30
        else:
            self.Ptime = newSS

    def start_TR_shot(self,timeout=300):
        self.values_storage = []
        self.TLOGstopper.clear()
        self.TLOG_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
        self.TLOG = logger_base(self.TR_dt,self.values,self.values_storage,self.TLOGstopper,timeout,self.subset)
        self.TLOG.start()
        print("Started log")


    def stop_TR_shot(self):
        if self.TLOG.is_alive():
            self.TLOGstopper.set()
            print("Log stopped")
            print("Saving data")
            convdata = data_postproc(self.values_storage,self.subset)
            savename = "TLOG_" + self.TLOG_timestamp
            savetofile(savename, convdata, self.savepath, self.labels)

    def start_P_scan(self,timeout=300):
        self.values_storage = []
        self.Pscanstopper.clear()
        self.Pscan_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
        self.PLOG = logger_base(self.Ptime/100,self.values,self.values_storage,self.Pscanstopper,2*self.Ptime,self.subset)
        self.PLOG.start()
        print("Started P scan")
        
    def end_P_scan(self):
        self.Pscanstopper.set()
        print("P scan finished, saving data")
        convdata = data_postproc_P(self.values_storage,self.subset)
        savename = "PSCAN_" + self.Pscan_timestamp
        savetofile_P(savename, convdata, self.savepath, self.labels)

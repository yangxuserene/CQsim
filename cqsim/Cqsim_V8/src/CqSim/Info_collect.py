from datetime import datetime
import time
from datetime import datetime
__metaclass__ = type

class Info_collect:
    def __init__(self, ave_uti = None, debug = None):
        self.myInfo = "Info Collect"
        self.ave_uti_in = ave_uti
        self.debug = debug
        self.sys_info = []
        self.start_date = datetime.now()
        self.reset_ave_uti_interval()
        
        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        
    def reset(self, ave_uti = None, debug = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if debug:
            self.debug = debug
        if ave_uti:
            self.ave_uti_in = ave_uti
        self.sys_info = []
        self.reset_ave_uti_interval()
    
    def reset_start_date (self,date):
        self.start_date = date       
        
    def info_collect(self, time, event, uti, waitNum = -1, waitSize = -1, inter = -1.0, extend = None):
        #self.debug.debug("* "+self.myInfo+" -- info_collect",5)
        event_date = self.start_date.strftime("%m/%d/%Y %H:%M:%S")
        temp_info = {'date': event_date, 'time': time, 'event': event, 'uti': uti, 'waitNum': waitNum, \
                     'waitSize': waitSize, 'inter': inter, 'extend': extend, 'tot_ave_uti': 0.0, 'ave_uti':[]}
                    
        if (len(self.sys_info)<=1):
            self.total_uti = 0.0
        else:
            self.total_uti += (time-self.sys_info[len(self.sys_info)-1]['time']) * self.sys_info[len(self.sys_info)-1]['uti']
            if (time-self.sys_info[0]['time']>0 ):
                temp_info['tot_ave_uti'] = self.total_uti*1.0/(time-self.sys_info[0]['time'])
            
        self.sys_info.append(temp_info)
        self.calculate_ave_uti()
        #self.debug.debug("   "+"<"+str(self.total_uti)+">"+str(temp_info),4) 
        
    def info_analysis(self):
        #self.debug.debug("* "+self.myInfo+" -- info_analysis",5)
        return 1
    
    def get_info(self, index):
        #self.debug.debug("* "+self.myInfo+" -- get_info",6)
        if index>=len(self.sys_info):
            return None
        return self.sys_info[index]
    
    def get_len(self):
        #self.debug.debug("* "+self.myInfo+" -- get_len",6)
        return len(self.sys_info)
    
    def calculate_ave_uti (self):
        i = 0
        while (i < len(self.ave_uti_interval)):
            self.sys_info[len(self.sys_info)-1]['ave_uti'].append(-1)
            i += 1
        
        i = len(self.sys_info) - 2
        j = 0
        temp_num = len(self.order_seq)
        current_time = self.sys_info[len(self.sys_info)-1]['time']
        temp_time = current_time
        temp_uti = 0
        while (i>=0 and j<temp_num):
            if (current_time-self.sys_info[i]['time']>=self.ave_uti_interval[self.order_seq[j]]):
                temp_uti_B = temp_uti +(self.ave_uti_interval[self.order_seq[j]] - (current_time - temp_time)) * self.sys_info[i]['uti']
                self.sys_info[len(self.sys_info)-1]['ave_uti'][self.order_seq[j]] = temp_uti_B/self.ave_uti_interval[self.order_seq[j]]
                #self.debug.debug("    {"+str(self.order_seq[j])+":"+str(self.ave_uti_interval[self.order_seq[j]])+"}:"+str(temp_uti_B),2)
                j += 1
            elif (i > 0):
                temp_uti += (temp_time - self.sys_info[i]['time']) * self.sys_info[i]['uti']
                temp_time = self.sys_info[i]['time']  
                i -= 1
            else:
                temp_uti += (temp_time - self.sys_info[i]['time']) * self.sys_info[i]['uti']
                temp_interval = current_time-self.sys_info[i]['time']
                while (j<temp_num):
                    if temp_interval == 0:
                        self.sys_info[len(self.sys_info)-1]['ave_uti'][self.order_seq[j]] = 0
                    else:
                        self.sys_info[len(self.sys_info)-1]['ave_uti'][self.order_seq[j]] = temp_uti/temp_interval
                    #self.debug.debug("    x{"+str(self.order_seq[j])+":"+str(self.ave_uti_interval[self.order_seq[j]])+"}:"+str(temp_uti),2)
                    j += 1
        
    def reset_ave_uti_interval (self):
        self.total_uti = 0
        self.order_seq = []
        self.ave_uti_interval = []
        if self.ave_uti_in != None:
            for ave_uti in self.ave_uti_in:
                self.ave_uti_interval.append(float(ave_uti))
            
    def reorder_uti_interval (self):
        self.order_seq = []
        i = 0
        uti_len = len(self.ave_uti_interval)
        while (i<uti_len):
            j = 0
            while (j<len(self.order_seq)):
                if (self.ave_uti_interval[i]<self.ave_uti_interval[self.order_seq[j]]):
                    break
                j += 1
            if (j>=len(self.order_seq)):
                self.order_seq.append(i)
            else:
                self.order_seq.insert(j,i)  
            i += 1
    
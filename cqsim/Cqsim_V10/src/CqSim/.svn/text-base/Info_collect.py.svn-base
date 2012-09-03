from datetime import datetime
import time
from datetime import datetime
__metaclass__ = type

class Info_collect:
    def __init__(self, avg_inter = None, debug = None):
        self.myInfo = "Info Collect"
        self.avg_inter_in = avg_inter
        self.debug = debug
        self.sys_info = []
        self.current_index=-1
        self.start_date = datetime.now()
        self.reset_avg_interval()
        self.show_module_info()
        self.overall_info={}
        self.overall_info['job_submit'] = [0,0]
        self.overall_info['job_start'] = [0,0]
        self.overall_info['job_end'] = [0,0]
        self.overall_info['tot_slowdown'] = [0,0]
        self.overall_info['tot_wait'] = [0,0]
        self.overall_info['tot_queue_depth'] = [0,0]
        self.overall_info['time'] = [0,0]
        
        
    def reset(self, avg_inter = None, debug = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if debug:
            self.debug = debug
        if avg_inter:
            self.avg_inter_in = avg_inter
        self.current_index=0
        self.sys_info = []
        self.reset_avg_interval()
        self.overall_info={}
        self.overall_info['job_submit'] = [0,0]
        self.overall_info['job_start'] = [0,0]
        self.overall_info['job_end'] = [0,0]
        self.overall_info['tot_slowdown'] = [0,0]
        self.overall_info['tot_wait'] = [0,0]
        self.overall_info['tot_queue_depth'] = [0,0]
        self.overall_info['time'] = [0,0]
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)
    
    def reset_start_date (self,date):
        self.start_date = date       
        
    def info_collect(self, time, event, uti, waitNum = -1, waitSize = -1, inter = -1.0, extend = None, current_para = None):
        #self.debug.debug("* "+self.myInfo+" -- info_collect",5)
        self.current_para=current_para
        event_date = self.start_date.strftime("%m/%d/%Y %H:%M:%S")
        temp_info = {'date': event_date, 'time': time, 'event': event, 'uti': uti, 'waitNum': waitNum, \
                     'waitSize': waitSize, 'inter': inter, 'extend': extend, 'tot_avg_uti': 0.0, 'avg_uti':[],\
                     'job_start':self.overall_info['job_start'][0], 'job_end':self.overall_info['job_end'][0], 'job_submit':self.overall_info['job_submit'][0],\
                     'slowdown':-1.0, 'waittime':-1.0, 'queue_depth':-1.0}
                    
        if (len(self.sys_info)<=1):
            self.total_uti = 0.0
        else:
            self.total_uti += (time-self.sys_info[len(self.sys_info)-1]['time']) * self.sys_info[len(self.sys_info)-1]['uti']
            if (time-self.sys_info[0]['time']>0 ):
                temp_info['tot_avg_inter'] = self.total_uti*1.0/(time-self.sys_info[0]['time'])
            
        self.sys_info.append(temp_info)
        self.current_index += 1
        self.calculate_avg_uti()
        self.info_analysis(event,current_para)
        #self.debug.debug("   "+"<"+str(self.total_uti)+">"+str(temp_info),4) 
        
    def info_analysis(self,event_type,job_para):
        #self.debug.debug("* "+self.myInfo+" -- info_analysis",5)
        if (event_type == 'E'):
            self.sys_info[self.current_index]['waittime'] = job_para['start']-job_para['submit']
            self.sys_info[self.current_index]['slowdown'] = (job_para['end']-job_para['submit'])*1.0/job_para['run']
            self.overall_info['tot_slowdown'][0] += self.sys_info[self.current_index]['slowdown']
            self.overall_info['tot_wait'][0] += self.sys_info[self.current_index]['waittime'] 
            self.overall_info['job_end'][0] += 1
            self.sys_info[self.current_index]['job_end'] = self.overall_info['job_end'][0]
            
        if (event_type == 'Q'):
            self.overall_info['job_submit'][0] += 1
            self.overall_info['tot_queue_depth'][0] -= (self.sys_info[self.current_index]['time']-self.overall_info['time'][1])
            self.sys_info[self.current_index]['job_submit'] = self.overall_info['job_submit'][0]
        if (event_type == 'S'):
            self.overall_info['job_start'][0] += 1
            self.overall_info['tot_queue_depth'][0] += (self.sys_info[self.current_index]['time']-self.overall_info['time'][1])
            self.sys_info[self.current_index]['job_start'] = self.overall_info['job_start'][0]
        elif (event_type == 'C'):
            i = self.current_index
            current_time = self.sys_info[len(self.sys_info)-1]['time']
            temp_time = current_time
            temp_uti = 0
            self.overall_info['time'][0] = self.sys_info[self.current_index]['time'] 
            temp_time2 = self.overall_info['time'][0] - self.overall_info['time'][1]
            temp_job = self.overall_info['job_end'][0] - self.overall_info['job_end'][1]
            temp_w = self.overall_info['tot_wait'][0]-self.overall_info['tot_wait'][1]
            temp_s = self.overall_info['tot_slowdown'][0]-self.overall_info['tot_slowdown'][1]
            temp_job_wait = self.overall_info['job_submit'][0] - self.overall_info['job_start'][0]
            self.overall_info['tot_queue_depth'][0] += temp_time2*temp_job_wait
            
            self.sys_info[self.current_index]['job_submit'] = self.overall_info['job_submit'][0]-self.overall_info['job_submit'][1]
            self.sys_info[self.current_index]['job_start'] = self.overall_info['job_start'][0]-self.overall_info['job_start'][1]
            self.sys_info[self.current_index]['job_end'] = self.overall_info['job_end'][0]-self.overall_info['job_end'][1]
            
            if temp_job>0:
                self.sys_info[self.current_index]['waittime'] = temp_w/temp_job
                self.sys_info[self.current_index]['slowdown'] = temp_s/temp_job
            else:
                self.sys_info[self.current_index]['waittime'] = 0
                self.sys_info[self.current_index]['slowdown'] = 0
            if (temp_time2>0):
                 self.sys_info[self.current_index]['queue_depth'] = ((self.overall_info['tot_queue_depth'][0]-self.overall_info['tot_queue_depth'][1])*1.0/temp_time2)*1800
            else:
                self.sys_info[self.current_index]['queue_depth'] = 0
                
                
            self.overall_info['job_submit'][1] = self.overall_info['job_submit'][0]
            self.overall_info['job_start'][1] = self.overall_info['job_start'][0]
            self.overall_info['job_end'][1] = self.overall_info['job_end'][0]
            self.overall_info['tot_slowdown'][1] = self.overall_info['tot_slowdown'][0]
            self.overall_info['tot_wait'][1] = self.overall_info['tot_wait'][0]
            self.overall_info['tot_queue_depth'][1] = self.overall_info['tot_queue_depth'][0]
            
        return 1
    
    def get_info(self, index):
        #self.debug.debug("* "+self.myInfo+" -- get_info",6)
        if index>=len(self.sys_info):
            return None
        return self.sys_info[index]
    
    def get_len(self):
        #self.debug.debug("* "+self.myInfo+" -- get_len",6)
        return len(self.sys_info)
    
    def calculate_avg_uti (self):
        i = 0
        while (i < len(self.avg_inter)):
            self.sys_info[len(self.sys_info)-1]['avg_uti'].append(-1)
            i += 1
        
        i = len(self.sys_info) - 2
        j = 0
        temp_num = len(self.order_seq)
        current_time = self.sys_info[len(self.sys_info)-1]['time']
        temp_time = current_time
        temp_uti = 0
        while (i>=0 and j<temp_num):
            if (current_time-self.sys_info[i]['time']>=self.avg_inter[self.order_seq[j]]):
                temp_uti_B = temp_uti +(self.avg_inter[self.order_seq[j]] - (current_time - temp_time)) * self.sys_info[i]['uti']
                self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = temp_uti_B/self.avg_inter[self.order_seq[j]]
                #self.debug.debug("    {"+str(self.order_seq[j])+":"+str(self.avg_inter[self.order_seq[j]])+"}:"+str(temp_uti_B),2)
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
                        self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = 0
                    else:
                        self.sys_info[len(self.sys_info)-1]['avg_uti'][self.order_seq[j]] = temp_uti/temp_interval
                    #self.debug.debug("    x{"+str(self.order_seq[j])+":"+str(self.avg_uti[self.order_seq[j]])+"}:"+str(temp_uti),2)
                    j += 1
        
    def reset_avg_interval (self):
        self.total_uti = 0
        self.order_seq = []
        self.avg_inter = []
        if self.avg_inter_in != None:
            for avg_inter in self.avg_inter_in:
                self.avg_inter.append(float(avg_inter))
            
    def reorder_avg_interval (self):
        self.order_seq = []
        i = 0
        uti_len = len(self.avg_inter)
        while (i<uti_len):
            j = 0
            while (j<len(self.order_seq)):
                if (self.avg_inter[i]<self.avg_inter[self.order_seq[j]]):
                    break
                j += 1
            if (j>=len(self.order_seq)):
                self.order_seq.append(i)
            else:
                self.order_seq.insert(j,i)  
            i += 1
    
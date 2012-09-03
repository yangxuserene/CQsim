from datetime import datetime
import time
import re

__metaclass__ = type

class Node_struc:
    def __init__(self, debug=None):
        self.myInfo = "Node Structure"
        self.debug = debug
        self.nodeStruc = []
        self.nodePool = []
        self.temp_nodePool = []
        self.job_list = []
        self.predict_node = []
        self.predict_job = []
        self.tot = -1
        self.idle = -1
        self.avail = -1
        self.show_module_info()
        
        
    def reset(self, debug=None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        self.debug = debug
        self.nodeStruc = []
        self.nodePool = []
        self.job_list = []
        self.predict_job = []
        self.predict_node = []
        self.temp_nodePool = []
        self.tot = -1
        self.idle = -1
        self.avail = -1
    
    def show_module_info (self):
        #self.debug.line(1," ")
        self.debug.debug("-- "+self.myInfo,1)   
        
    def read_list(self,source_str):
        #self.debug.debug("* "+self.myInfo+" -- read_list",5)
        result_list=[]
        regex_str = "[\[,]([^,\[\]]*)"
        result_list=re.findall(regex_str,source_str)
        for item in result_list:
            item=int(item)
        return result_list
    
    def import_node_file(self, node_file):
        #self.debug.debug("* "+self.myInfo+" -- import_node_file",5)
        regex_str = "([^;\\n]*)[;\\n]"
        nodeFile = open(node_file,'r')
        self.nodeStruc = []
        
        i = 0
        while (1):
            tempStr = nodeFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
                
            self.debug.debug("  node["+str(i)+"]: "+str(temp_dataList),4)
            tempInfo = {"id": int(temp_dataList[0]), \
                          "location": self.read_list(temp_dataList[1]), \
                          "group": int(temp_dataList[2]), \
                          "state": int(temp_dataList[3]), \
                          "proc": int(temp_dataList[4]), \
                          "start": -1, \
                          "end": -1, \
                          "extend": None}
            self.nodeStruc.append(tempInfo)
            self.nodePool.append(i)
            i += 1
        nodeFile.close()
        self.tot = len(self.nodeStruc)
        self.idle = self.tot
        self.avail = self.tot
        self.debug.debug("  Tot:"+str(self.tot)+" Idle:"+str(self.idle)+" Avail:"+str(self.avail)+" ",4)
        return
        
    def import_node_config (self, config_file):
        #self.debug.debug("* "+self.myInfo+" -- import_node_config",5)
        regex_str = "([^=\\n]*)[=\\n]"
        nodeFile = open(config_file,'r')
        config_data={}
                
        self.debug.line(4)
        while (1):
            tempStr = nodeFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            config_data[temp_dataList[0]]=temp_dataList[1]
            self.debug.debug(str(temp_dataList[0])+": "+str(temp_dataList[1]),4)
        self.debug.line(4)
        nodeFile.close()
        
    def import_node_data(self, node_data):
        #self.debug.debug("* "+self.myInfo+" -- import_node_data",5)
        self.nodeStruc = []
        
        temp_len = len(node_data)
        i=0
        while (i<temp_len):
            temp_dataList = node_data[i]
                
            tempInfo = {"id": temp_dataList[0], \
                          "location": temp_dataList[1], \
                          "group": temp_dataList[2], \
                          "state": temp_dataList[3], \
                          "proc": temp_dataList[4], \
                          "start": -1, \
                          "end": -1, \
                          "extend": None}
            self.nodePool.append(i)
            self.nodeStruc.append(tempInfo)
            i += 1
        self.tot = len(self.nodeStruc)
        self.idle = self.tot
        self.avail = self.tot
        
    def is_available(self, node_req):
        #self.debug.debug("* "+self.myInfo+" -- is_available",6)
        proc_num = node_req['proc']
        result = 0
        if self.avail >= proc_num:
            result = 1
        self.debug.debug("[Avail Check] "+str(result),6)
        return result
        
    def get_tot(self):
        #self.debug.debug("* "+self.myInfo+" -- get_tot",6)
        return self.tot
        
    def get_idle(self):
        #self.debug.debug("* "+self.myInfo+" -- get_idle",6)
        return self.idle
        
    def get_avail(self):
        #self.debug.debug("* "+self.myInfo+" -- get_avail",6)
        return self.avail
        
    def node_allocate(self, node_req, job_index, start, end):
        #self.debug.debug("* "+self.myInfo+" -- node_allocate",5)
        proc_num = node_req['proc']
        if self.is_available(node_req) == 0:
            return 0
        temp_node=self.find_place(node_req)
        temp_job_info = {'job':job_index, 'end': end, 'node': proc_num,'allocate':temp_node}
        j = 0
        is_done = 0
        temp_num = len(self.job_list)
        while (j<temp_num):
            if (temp_job_info['end']<self.job_list[j]['end']):
                self.job_list.insert(j,temp_job_info)
                is_done = 1
                break
            j += 1
            
        if (is_done == 0):
            self.job_list.append(temp_job_info)
        self.debug.debug("  Job"+"["+str(job_index)+"]"+" Req:"+str(proc_num)+" Avail:"+str(self.avail)+" "+" Allocate:"+str(temp_job_info['allocate'])+" ",4)
        return temp_job_info['allocate']
        
    def node_release(self, job_index, end):
        #self.debug.debug("* "+self.myInfo+" -- node_release",5)
        '''
        self.debug.line(2,"...")
        for job in self.job_list:
            self.debug.debug(job['job'],2)
        self.debug.line(2,"...")
        '''
        #print job_index
            
        temp_node = 0
        j = 0
        temp_num = len(self.job_list)
        while (j<temp_num):
            if (job_index==self.job_list[j]['job']):
                temp_node = self.job_list[j]['node']
                break
            j += 1
            
        self.recover_place(self.job_list[j]['allocate'])
        self.job_list.pop(j)
        self.debug.debug("  Release"+"["+str(job_index)+"]"+" Req:"+str(temp_node)+" Avail:"+str(self.avail)+" ",4)
        return 1
        
    def find_place(self,node_req):  
        proc_num = node_req['proc']
        result = []
        i = 0 
        if self.avail >= proc_num:
            while(i<proc_num):
                result.append(self.nodePool.pop())
                i += 1
            self.idle -= proc_num
            self.avail = self.idle
        return result
    
    def recover_place(self,node_list):
        self.nodePool[0:0]=node_list[:]
        self.idle += len(node_list)
        self.avail = self.idle
    
    def pre_avail(self, node_req, start, end = None):
        #self.debug.debug("* "+self.myInfo+" -- pre_avail",6)
        #self.debug.debug("pre avail check: "+str(proc_num)+" (" +str(start)+";"+str(end)+")",6)
        proc_num = node_req['proc']
        if not end or end < start:
            end = start
             
        i = 0
        temp_job_num = len(self.predict_node)
        while (i < temp_job_num):
            if (self.predict_node[i]['time']>=start and self.predict_node[i]['time']<end):
                if (proc_num>self.predict_node[i]['avail']):
                    return 0
            i += 1
        return 1
        
    def reserve(self, node_req, job_index, time, start = None, index = -1 ):
        #self.debug.debug("* "+self.myInfo+" -- reserve",5)
            
        proc_num = node_req['proc']
        temp_max = len(self.predict_node)
        if (start):
            if (self.pre_avail(proc_num,start,start+time)==0):
                return -1
        else:
            i = 0
            j = 0
            if (index >= 0 and index < temp_max):
                i = index
            elif(index >= temp_max):
                return -1
            #kk = []
            while (i<temp_max): 
                if (proc_num<=self.predict_node[i]['avail']):
                    j = self.find_res_place(node_req,i,time)
                    #kk.append(j)
                    if (j == -1):
                        start = self.predict_node[i]['time']
                        break
                    else:
                        i = j + 1
                else:
                    #kk.append('-')
                    i += 1
        '''
        if ( not start):
            print i,temp_max
            print kk
            print proc_num,self.tot
            for x in self.predict_node:
                print x
        '''
        end = start + time
        j = i
                
        is_done = 0
        start_index = j
        while (j < temp_max):
            if (self.predict_node[j]['time']<end):
                self.predict_node[j]['idle'] -= proc_num
                self.predict_node[j]['avail'] = self.predict_node[j]['idle']
                j += 1
            elif (self.predict_node[j]['time']==end):
                is_done = 1
                break
            else:
                self.predict_node.insert(j,{'time':end,\
                 'idle':self.predict_node[j-1]['idle'], 'avail':self.predict_node[j-1]['avail']})
                #self.debug.debug("xx   "+str(proc_num),4)
                self.predict_node[j]['idle'] += proc_num
                self.predict_node[j]['avail'] = self.predict_node[j]['idle']
                is_done = 1
                
                #self.debug.debug("xx   "+str(n)+"   "+str(k),4)
                break
            
        if (is_done != 1):
            self.predict_node.append({'time':end,'idle':self.tot,'avail':self.tot})
                
        self.predict_job.append({'job':job_index, 'start':start, 'end':end})
        '''
        i = 0
        self.debug.line(2,'.')
        temp_num = len(self.predict_node)
        self.debug.debug("<> "+str(job_index) +"   "+str(proc_num) +"   "+str(time) +"   ",2)
        while (i<temp_num):
            self.debug.debug("O "+str(self.predict_node[i]),2)
            i += 1
        self.debug.line(2,'.')
        ''' 
        return start_index
     
    def pre_delete(self, node_req, job_index):
        #self.debug.debug("* "+self.myInfo+" -- pre_delete",5)
        return 1
        
    def pre_modify(self, node_req, start, end, job_index):  
        #self.debug.debug("* "+self.myInfo+" -- pre_modify",5)  
        return 1
        
    def pre_get_last(self):
        #self.debug.debug("* "+self.myInfo+" -- pre_get_last",6)
        pre_info_last= {'start':-1, 'end':-1}
        for temp_job in self.predict_job:
            #self.debug.debug("xxx   "+str(temp_job),4)
            if (temp_job['start']>pre_info_last['start']):
                pre_info_last['start'] = temp_job['start']
            if (temp_job['end']>pre_info_last['end']):
                pre_info_last['end'] = temp_job['end']
        return pre_info_last
        
    def pre_reset(self, time):
        #self.debug.debug("* "+self.myInfo+" -- pre_reset",5)  
        self.predict_node = []
        self.predict_job = []
        self.predict_node.append({'time':time, 'idle':self.idle, 'avail':self.avail})
                            
                            
        temp_job_num = len(self.job_list)
        '''
        i = 0
        self.debug.line(2,'==')
        while (i<temp_job_num):
            self.debug.debug("[] "+str(self.job_list[i]),2)
            i += 1
        self.debug.line(2,'==')
        '''
        
        i = 0
        j = 0
        while i< temp_job_num:
            if (self.predict_node[j]['time']!=self.job_list[i]['end'] or i == 0):
                self.predict_node.append({'time':self.job_list[i]['end'],\
                                    'idle':self.predict_node[j]['idle'], 'avail':self.predict_node[j]['avail']})
                j += 1
            self.predict_node[j]['idle'] += self.job_list[i]['node']
            self.predict_node[j]['avail'] = self.predict_node[j]['idle']
            i += 1
        ''' 
        i = 0
        self.debug.line(2,'..')
        temp_num = len(self.predict_node)
        while (i<temp_num):
            self.debug.debug("O "+str(self.predict_node[i]),2)
            i += 1
        self.debug.line(2,'..')
        '''
        return 1
        
    
    def find_res_place(self, node_req, index, time):
        #self.debug.debug("* "+self.myInfo+" -- find_res_place",5)  
        proc_num = node_req['proc']
        if index>=len(self.predict_node):
            index = len(self.predict_node) - 1
             
        i = index
        end = self.predict_node[index]['time']+time
        temp_node_num = len(self.predict_node)
        
        while (i < temp_node_num):
            if (self.predict_node[i]['time']<end):
                if (proc_num>self.predict_node[i]['avail']):
                    #print "xxxxx   ",temp_node_num,proc_num,self.predict_node[i]
                    return i
            i += 1
        return -1
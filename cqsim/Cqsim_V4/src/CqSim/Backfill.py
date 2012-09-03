import cqsim_path
import re

__metaclass__ = type

class Backfill:
    def __init__(self, mode = 0, ad_mode = 0, node_module = None, info_module = None, debug = None, para_list = None, ad_para_list = None):
        self.myInfo = "Backfill"
        self.para={}
        self.para['mode'] = mode
        self.para['ad_mode'] = ad_mode
        self.para['size'] = 0
        if para_list:
            self.para['size'] = para_list[0]
        if ad_para_list:
            self.para['ad_config'] = cqsim_path.path_config+ad_para_list[0]
        self.node_module = node_module
        self.info_module = info_module
        self.debug = debug
        self.para_list_in = para_list
        self.ad_para_list_in = ad_para_list
        self.ad_current_para = []
        self.current_para = []
        self.wait_job = []

        self.debug.line(4," ")
        self.debug.line(4,"#")
        self.debug.debug("# "+self.myInfo,1)
        self.debug.line(4,"#")
        
        self.adapt_reset()
            
        
        
    def reset (self, mode = None, ad_mode = None, node_module = None, info_module = None, debug = None, para_list = None, ad_para_list = None):
        #self.debug.debug("* "+self.myInfo+" -- reset",5)
        if mode:
            self.para['mode'] = mode
        if ad_mode :
            self.para['ad_mode'] = ad_mode 
        if ad_para_list:
            self.ad_para_list_in = ad_para_list 
            self.para['ad_config'] = ad_para_list[0]
        if node_module:
            self.node_module = node_module
        if info_module:
            self.info_module = info_module
        if debug:
            self.debug = debug
        if para_list:
            self.para_list_in = para_list
            self.para['size'] = para_list[0]
        self.current_para = []
        self.wait_job = []
        self.current_para = []
        self.adapt_reset()
    
    def backfill (self, wait_job, para_in = None):
        #self.debug.debug("* "+self.myInfo+" -- backfill",5)
        if (len(wait_job) <= 1):
            return []
        self.current_para = para_in
        self.wait_job = wait_job
        job_list = self.main()
        return job_list
    
    def main (self):
        #self.debug.debug("* "+self.myInfo+" -- main",5)
        result = []
        if (self.para['mode'] == 1):
            # EASY backfill
            result = self.backfill_EASY()
        elif (self.para['mode'] == 2):
            # Conservative backfill
            result = self.backfill_cons() 
        else:
            return None
        return result
    
    def backfill_EASY(self):
        #self.debug.debug("* "+self.myInfo+" -- backfill_EASY",5)
        backfill_list=[]
        self.node_module.pre_reset(self.current_para['time'])
        '''
        self.debug.line(4,'.')
        for job in self.wait_job:
            self.debug.debug(job,4)
        self.debug.line(4,'.')
        '''
            
        self.node_module.reserve(self.wait_job[0]['proc'], self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            backfill_test = self.node_module.pre_avail(self.wait_job[i]['proc'],\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
                self.node_module.reserve(self.wait_job[i]['proc'], self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1
        return backfill_list
        
    def backfill_cons(self):
        #self.debug.debug("* "+self.myInfo+" -- backfill_cons",5)
        backfill_list=[]
        self.node_module.pre_reset(self.current_para['time'])
        self.node_module.reserve(self.wait_job[0]['proc'], self.wait_job[0]['index'], self.wait_job[0]['run'])
        i = 1
        job_num = len(self.wait_job)
        while (i < job_num):
            backfill_test = 0
            backfill_test = self.node_module.pre_avail(self.wait_job[i]['proc'],\
                    self.current_para['time'], self.current_para['time']+self.wait_job[i]['run'])
            if (backfill_test == 1):
                backfill_list.append(self.wait_job[i]['index'])
            self.node_module.reserve(self.wait_job[i]['proc'], self.wait_job[i]['index'], self.wait_job[i]['run'])
            i += 1  
        return backfill_list
    
    def adapt_reset(self):
        #self.debug.debug("* "+self.myInfo+" -- adapt_reset",5)
        self.adapt_data = []
        self.check_data_name = []
        self.check_data_para = []
        self.ave_uti_interval = []
        self.ave_uti_index = []
        self.adapt_item = []
        self.adapt_data_name = "ad_bf"
        if (self.para['ad_config']):
            self.adapt_read_config(self.para['ad_config'])
            
        i = 0
        while (i < len(self.ave_uti_interval)):
            item = self.ave_uti_interval[i]
            item_exist = 0
            j = 0
            while (j < len(self.info_module.ave_uti_interval)):
                if item == self.info_module.ave_uti_interval[j]:
                    item_exist = 1
                    break
                j += 1
            if (item_exist == 0):
                self.info_module.ave_uti_interval.append(item)
            self.ave_uti_index.append(j)
            i += 1
                
        i = 0
        while (i < len(self.check_data_name)):
            if self.check_data_name[i] == 'ave_uti':
                self.check_data_para[i]=self.ave_uti_index[self.check_data_para[i]]
            i += 1
        self.info_module.reorder_uti_interval()
        
        self.debug.line(2,"**")
        self.debug.line(2,"**")
        self.debug.line(2,"**")
        self.debug.debug(self.adapt_data,2)
        self.debug.debug(self.check_data_name,2)
        self.debug.debug(self.check_data_para,2)
        self.debug.debug(self.ave_uti_interval,2)
        self.debug.debug(self.adapt_item,2)
        self.debug.debug(self.info_module.ave_uti_interval,2)
        self.debug.line(2,"**")
        self.debug.line(2,"**")
        self.debug.line(2,"**")
        '''
        '''
        
    def get_adapt_data (self):
        return
        
    def get_adapt_data_name(self):
        return self.adapt_data_name
        
    def adapt_read_config(self,fileName):
        #self.debug.debug("* "+self.myInfo+" -- adapt_read_config",5)
        regex_str = "([^=\\n]*)[=\\n]"
        configFile = open(fileName,'r')
                
        while (1):
            tempStr = configFile.readline()
            if not tempStr :    # break when no more line
                break
            temp_dataList=re.findall(regex_str,tempStr)
            if (temp_dataList[0] == 'adapt_data'):
                self.adapt_data = self.get_list(temp_dataList[1])
            elif (temp_dataList[0] == 'check_data_name'):
                self.check_data_name = self.get_list(temp_dataList[1])
            elif (temp_dataList[0] == 'check_data_para'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.check_data_para = temp_list
            elif (temp_dataList[0] == 'ave_uti'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.ave_uti_interval = temp_list
            elif (temp_dataList[0] == 'adapt_item'):
                temp_list=self.get_list(temp_dataList[1])
                i = 0
                while i<len(temp_list):
                    temp_list[i] = int(temp_list[i])
                    i += 1
                self.adapt_item.append(temp_list)
                
        configFile.close()
        return 1
    
    def backfill_adapt (self,para_in):
        self.ad_current_para = para_in
        if (self.para['ad_mode'] == 1):
            return self.adapt_1()
    
    def adapt_1(self):
        action = 0
        max_check = len(self.check_data)
        for item in self.adapt_item:
            i = 0
            action = 1
            while (i < max_check and action == 1):
                if (self.ad_current_para[self.check_data[i]]>=item[i*2+3] and \
                 self.ad_current_para[self.check_data[i]]<item[i*2+4]):
                    action = 1
                else:
                    action = 0
            if (action != 0):
                if (item[1]==0):
                    self.para[self.adapt_data[item[0]]] = item[2]
                elif (item[1]==1):
                    self.para[self.adapt_data[item[0]]] += item[2]
                break
            
        return action
    
    def get_list (self,inputstring,regex=r'([^,]+)'):
        return re.findall(regex,inputstring)
    
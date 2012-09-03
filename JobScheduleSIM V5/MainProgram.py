import sys
sys.path.append('/home/JobSchedule_SIM/')

import InputManager
import ShowGraph
#import SimulatorProc2 as SimulatorProc

#import SimulatorProc_old as SimulatorProc
import SimulatorProc

__metaclass__ = type
class MainProgram:
	def init(self):
		
		self.jobData=[]
		self.sysData={'fileName':"",'saveFN':"JS",'readNum':0,'submitModify':1, 'dropPer':0, 'dropNum':0, 'interTime':600, 'timeSpace':604800,'aveUti':[], 'aveUtiNum':0 , 'sim_Num':0, 'jobNum':0, 'nodeNum':0, 'ft_job':".rst", 'ft_uti':".uti"}
		
		self.dropQueue=[]
		self.graphColor=[]	#bar color
		self.graphData1=[]	#waiting time
		self.graphData2=[]	#response time
		self.graphData3=[]	#BSD
		self.graphData4=[]	#happyness job number
		self.graphData5=[]	#system utilization ratio
		self.graphData6=[]	#system utilization single (time/uti) exactly
		self.graphData6_a=[]	#system utilization single (time/uti) every n time
		self.graphData6_b=[]	#average system utilization single (time/uti) every n time
			
		self.graphData7=[]	#system utilization single (min_start/max_end)
		self.graphData8=[]	#system fragment
		self.graphData9=[]	#wait job number exactly
		self.graphData9_a=[]	#wait job number every n time
		self.graphData10=[]	#wait job total size exactly
		self.graphData10_a=[]	#wait job total size every n time
		self.graphData11=[]	#time space info
		
		self.maxWaitNum = []
		self.maxWaitNum_a = []
		self.maxWaitSize = []
		self.maxWaitSize_a = []
		self.showIt = ShowGraph.ShowGraph()
		self.showIt.init()
		self.showIt.resetPara(1,['unname'])
		self.algNames =[]
		self.jobData=[]
		self.xLabelNum = 10
		self.shadowMode = 1
		# algs: string
		# BFmode: int
		# name: string
		
	def set_AveUtiInter(self,aveUti_in,aveUtiName_in,interTime_in,timeSpace_in):
		self.sysData['aveUti']=aveUti_in
		self.sysData['aveUtiNum']=len(aveUti_in)
		self.sysData['aveUtiName']=aveUtiName_in
		self.sysData['interTime']=interTime_in
		self.sysData['timeSpace']=timeSpace_in
		
	def set_graph_uti(self, xLabelNum = 10, shadowMode_in = 1):
		# shadow mode: 1. wait job number  2. wait job total size
		self.xLabelNum = xLabelNum
		self.shadowMode = shadowMode_in

	def set_submitDensity(self,submitModify_in):
		self.sysData['submitModify']=submitModify_in		
		
	def set_dropPercent(self,per_in):
		self.sysData['dropPer']=per_in	
		
	def set_fileType(self,type_job_in,type_uti_in):
		self.sysData['ft_job']=type_job_in		
		self.sysData['ft_uti']=type_uti_in		
		
	def set_SWFfile(self,swf_FN,saveFN_in,readNum_in=None):
		self.sysData['fileName']=swf_FN	
		self.sysData['saveFN']=saveFN_in	
		if (readNum_in==None):
			readNum_in = 0
		self.sysData['readNum']=readNum_in	
		
	def addTask(self,prioStr_in,winSize_in,BFmode_in,algName_in,FN_in = None,color="blue"):
		if (FN_in==None or FN_in==""):
			temp_r='999'
			try:
				w=1
				z=1
				l=0
				t=1
				temp_r=str(int(eval(prioStr_in)))
				while (len(temp_r)<3):
					temp_r='0'+temp_r
			except:
				temp_r='999'
			FN_in = 'JS_'+self.sysData['saveFN']+'_W'+str(winSize_in)+'_B'+str(BFmode_in)+'_A'+temp_r
		self.jobData.append({'algs':prioStr_in,'BFmode':BFmode_in,'name':algName_in, 'saveFN':FN_in, 'winSize':winSize_in, 'color':color,'jobResult':[], 'utiResult':[]})
			
		self.graphColor.append(color)	#bar color
		self.graphData1.append(0.0)	#waiting time
		self.graphData2.append(0.0)	#response time
		self.graphData3.append(0.0)	#BSD
		self.graphData4.append(0)	#happyness job number
		self.graphData5.append(0.0)	#system utilization ratio
		self.graphData6.append({'time':[],'uti':[]})    #system utilization single (time/uti) exactly
		self.graphData6_a.append({'time':[],'uti':[]})    #system utilization single (time/uti) every n time
		self.graphData6_b.append({'time':[],'uti':[]})
		tempIndex=len(self.graphData6_b)-1
		self.maxWaitNum.append(0)
		self.maxWaitNum_a.append(0)
		self.maxWaitSize.append(0)
		self.maxWaitSize_a.append(0)
		i=0
		while (i<self.sysData['aveUtiNum']):
			self.graphData6_b[tempIndex]['time'].append([])
			self.graphData6_b[tempIndex]['uti'].append([])
			i += 1
			
		self.graphData7.append({'min':0,'max':0})    #system utilization single (min_start/max_end)
		self.graphData8.append(0.0)	#system fragment
		self.graphData9.append({'time':[],'wait':[]})	#wait job number exactly
		self.graphData9_a.append({'time':[],'wait':[]})	#wait job number every n time
		self.graphData10.append({'time':[],'size':[]})	#wait job total size exactly
		self.graphData10_a.append({'time':[],'size':[]})	#wait job total size every n time
		self.graphData11.append([])		#time space info
		self.algNames.append(algName_in)
		self.sysData['sim_Num'] += 1
		
	def startSImulation(self):
			
		for i2 in range(self.sysData['sim_Num']):
			self.IM=InputManager.InputManager()
			self.IM.init(self.sysData['readNum'])
			self.IM.setSubmitPara(self.sysData['submitModify'])
			self.simulator=SimulatorProc.SimulatorProc()
			self.IM.SWFReader(self.sysData['fileName'] )
			self.simulator.init()
			tempttt=self.IM.getSWFData()
			self.simulator.dataIn(self.IM.getSWFData(),self.IM.getSysInfo())
				
			self.sysData['jobNum']=self.IM.getJobNum()
			self.sysData['nodeNum']=self.IM.getNodeStruc()
			self.simulator.parameterIn(self.sysData['jobNum'],self.sysData['nodeNum'])
			self.sysData['dropNum']=self.sysData['jobNum']*self.sysData['dropPer']/100
			if (self.sysData['dropPer']>0 and self.sysData['dropNum']<1):
				self.sysData['dropNum'] = 1
				
			self.IM.setBackFilling(self.jobData[i2]['BFmode'])
			self.IM.scheAlgorithmIn(self.jobData[i2]['algs'])
			self.IM.setWinSize(self.jobData[i2]['winSize'])
			self.simulator.dataIn(self.IM.getSWFData(),self.IM.getSysInfo())
			self.simulator.parameterIn(self.sysData['jobNum'],self.sysData['nodeNum'])
			self.simulator.winSizeIn(self.IM.getWinSize())
			self.simulator.paraReset()
			print (">>>>>>>>>>>>>>>>>>>>>>  ALG: " + str(self.jobData[i2]['name'])+" (" +str(self.jobData[i2]['algs'])+")")
			if (self.IM.algorithmCheck() <= 0):
				print "Algorithm \""+str(self.jobData[i2]['algs'])+"\" illegal!"
				break
			else:
				self.simulator.prioFuncIn(self.IM.getPrioFunc(),self.IM.getBFStr())
				self.simulator.beginSimulation()
				self.simulator.exportResult(self.jobData[i2][ 'saveFN']+self.sysData['ft_job'], self.jobData[i2][ 'saveFN']+self.sysData['ft_uti'])
				self.jobData[i2][ 'jobResult']=self.simulator.getResult()
				self.jobData[i2][ 'utiResult']=self.simulator.getSysUti()
				for j3 in range(self.sysData['jobNum']):
					print str(self.jobData[i2][ 'jobResult'][j3])+"   "+str(self.jobData[i2][ 'jobResult'][j3]['start'] - self.jobData[i2][ 'jobResult'][j3]['submit'])

				for j4 in range(len(self.jobData[i2][ 'utiResult'])):
					print str(self.jobData[i2][ 'utiResult'][j4])

				
	def readJobResult(self):
		read_index=0
		while (read_index<self.sysData['sim_Num']):
			fileNameIn= self.jobData[read_index][ 'saveFN']+self.sysData['ft_job']
			swfFile = open(fileNameIn,'r')
			j = 0
			self.jobData[read_index]['happyNum'] = 0
			jr_alg=""
			jr_bf=-1
			jr_winsize=-1
			jr_nodeNum=-1
			while 1:
				tempStr = swfFile.readline()
				if not tempStr :
					break
				if tempStr[0] != ';':
					#print tempStr
					strNum = len(tempStr)
					newWord = 1
					k = 0
					ID = ""
					submit = ""
					runTime = ""
					reqTime = ""
					reqNodes = ""
					userID = ""
					groupID = ""
					start=""
					end=""
					state=""
					happy=""
					estStart=""
					for i in range(strNum):
						if tempStr[i] == " ":
							if newWord == 0:
								newWord = 1
								k = k+1
						else:
							newWord = 0
							if k == 0:
								ID=ID+ tempStr[i] 
							elif k == 1:
								start=start+ tempStr[i] 
							elif k == 2:
								end=end+ tempStr[i] 
							elif k == 3:
								runTime=runTime+ tempStr[i] 
							elif k == 4:
								submit=submit+ tempStr[i] 
							elif k == 5:
								reqTime=reqTime+ tempStr[i] 
							elif k == 6:
								reqNodes=reqNodes+ tempStr[i] 
							elif k == 7:
								userID=userID+ tempStr[i] 
							elif k == 8:
								groupID=groupID+ tempStr[i] 
							elif k == 9:
								state=state+ tempStr[i] 
							elif k == 10:
								happy=happy+ tempStr[i] 
							elif k == 11:
								estStart=estStart+ tempStr[i] 
					tempInfo = {'id':int(ID), 'submit':float(submit), 'run':float(runTime), 'reqTime':float(reqTime), 'reqNode':float(reqNodes), 'user':int(userID), 'group':int(groupID), 'start':float(start), 'end':float(end), 'score':0, 'state':int(state), 'happy':float(happy),'estStart':float(estStart)}
					self.jobData[read_index]['jobResult'].append(tempInfo)
					j = j + 1
				else:
					tempStr2=tempStr[2:]
					aaa=0
					exec(tempStr2)
			self.sysData['jobNum'] = j
			self.sysData['nodeNum'] =jr_nodeNum
			swfFile.close()
							
			fileNameIn= self.jobData[read_index][ 'saveFN']+self.sysData['ft_uti']
			swfFile = open(fileNameIn,'r')
			j = 0
			while 1:
				tempStr = swfFile.readline()
				if not tempStr :
					break
				if tempStr[0] != ';':
					#print tempStr
					strNum = len(tempStr)
					newWord = 1
					k = 0
					time = ""
					inter = ""
					uti = ""
					delta = ""
					waitNum = ""
					waitSize = ""
					for i in range(strNum):
						if tempStr[i] == " ":
							if newWord == 0:
								newWord = 1
								k = k+1
						else:
							newWord = 0
							if k == 0:
								time=time+ tempStr[i] 
							elif k == 1:
								inter=inter+ tempStr[i] 
							elif k == 2:
								uti=uti+ tempStr[i] 
							elif k == 3:
								delta=delta+ tempStr[i] 
							elif k == 4:
								waitNum=waitNum+ tempStr[i] 
							elif k == 5:
								waitSize=waitSize+ tempStr[i] 
								
					tempInfo = {'time':float(time), 'inter':float(inter), 'uti':float(uti), 'delta':int(delta), 'waitNum':int(waitNum), 'waitSize':float(waitSize)}
					self.jobData[read_index]['utiResult'].append(tempInfo)
					j = j + 1
			swfFile.close()
			print ""
			print str(read_index)+"  "+str(self.jobData[read_index]['saveFN'])
			for j3 in range(self.sysData['jobNum']):
				print str(self.jobData[read_index][ 'jobResult'][j3])+"   "+str(self.jobData[read_index][ 'jobResult'][j3]['start'] - self.jobData[read_index][ 'jobResult'][j3]['submit'])
			
			for j4 in range(len(self.jobData[read_index][ 'utiResult'])):
				print str(self.jobData[read_index][ 'utiResult'][j4])
			
			read_index += 1
			
			
	def analysisResult(self):
		for i2 in range(self.sysData['sim_Num']):
			tempR=self.jobData[i2][ 'jobResult']
			tempR3=self.jobData[i2][ 'utiResult']
			'''
			for j3 in range(self.sysData['jobNum']):
				print str(tempR[j3])+"   "+str(tempR[j3]['start'] - tempR[j3]['submit'])
			'''
			self.getWaitTime(self.sysData['jobNum'],tempR,i2)
			self.getResponseTime(self.sysData['jobNum'],tempR,i2)
			self.getBSD(self.sysData['jobNum'],tempR,i2)
			self.getUtiRatio(tempR3,self.sysData['nodeNum'],i2)
			self.getSysFraRatio(tempR3,self.sysData['nodeNum'],i2)
			self.getHappyNum(self.sysData['jobNum'],tempR,i2)
			self.getSysUti(tempR3,0,self.sysData['interTime'],self.sysData['nodeNum'],i2)
		
		
	def showResUtiG(self):
		self.showIt.resetPara(self.sysData['sim_Num'],self.algNames)
		
		self.showIt.graphA(1,self.graphData1,self.graphColor,"Overall Average Waiting Time(sec)", saveGraph="1. AveWaitTime")
		self.showIt.graphA(2,self.graphData2,self.graphColor,"Overall Average Response Time(sec)", saveGraph="2. AveRespTime")
		self.showIt.graphA(3,self.graphData3,self.graphColor,"Overall Average Slowdown", saveGraph="3. AveSD")
		self.showIt.graphA(4,self.graphData4,self.graphColor,"Happy Job Number", saveGraph="4. FairNum")
		self.showIt.graphB(5,self.graphData4,self.sysData['jobNum'],self.graphColor,"Happy Job Ratio", saveGraph="5. FairRatio")
		self.showIt.graphB(6,self.graphData5,self.sysData['nodeNum'],self.graphColor,"System Utilization", saveGraph="6. SysUti")
		self.showIt.graphB(7,self.graphData8,self.sysData['nodeNum'],self.graphColor,"Loss Of Capacity", saveGraph="7. LOC")
		
		temp_graphSeq = 8
		for i4 in range(self.sysData['sim_Num']):
			#self.showIt.graphC(8+i4,self.graphData6[i4]['time'], self.graphData6[i4]['uti'],self.IM.getNodeStruc(), self.graphData7[i4]['min'], self.graphData7[i4]['max'], 10, "System Utilization\n("+str(self.jobData[i4]['algs'])+"   BF:"+str(self.jobData[i4]['BFmode'])+"   WIN:"+str(self.jobData[i4]['winSize'])+")")
			self.showIt.graphD(temp_graphSeq,self.graphData6_a[i4]['time'], self.graphData6_a[i4]['uti'],self.sysData['nodeNum'], \
				self.graphData7[i4]['min'], self.graphData7[i4]['max'], self.xLabelNum, \
				"System Utilization\n("+str(self.jobData[i4]['algs'])+"   BF:"+str(self.jobData[i4]['BFmode'])+"   WIN:"+str(self.jobData[i4]['winSize'])+")", \
				saveGraph=str(temp_graphSeq)+". aveSU"+str(self.sysData['interTime'])+"_"+self.jobData[i4]['saveFN'])
			temp_graphSeq += 1
			
			temp_shadowX=[]
			temp_shadowY=[]
			temp_shadowMax=0
			temp_shadowName=""
			if (self.shadowMode == 1):
				#wait job number
				temp_shadowX = self.graphData9_a[i4]['time']
				temp_shadowY = self.graphData9_a[i4]['wait']
				temp_shadowMax = self.maxWaitNum_a[i4]
				temp_shadowName = "Waiting Job Number"
			elif (self.shadowMode == 2):
				#wait job total size
				temp_shadowX = self.graphData10_a[i4]['time']
				temp_shadowY = self.graphData10_a[i4]['size']
				temp_shadowMax = self.maxWaitSize_a[i4]
				temp_shadowName = "Waiting Job Size"
				
			#print temp_shadowName
			uti_count=1
			uti_max=len(self.graphData11[i4])
			for timeGroup in self.graphData11[i4]:
				self.showIt.graphE(temp_graphSeq,4,self.graphData6_b[i4]['time'], self.graphData6_b[i4]['uti'],timeGroup,self.sysData['nodeNum'], \
					self.graphData6_b[i4]['time'][0][timeGroup[0]], self.graphData6_b[i4]['time'][0][timeGroup[1]-1],self.xLabelNum, \
					"Average System Utilization ("+str(uti_count)+"-"+str(uti_max)+")\n("+str(self.jobData[i4]['algs'])+"   BF:"+str(self.jobData[i4]['BFmode'])+"   WIN:"+str(self.jobData[i4]['winSize'])+")", self.sysData['aveUtiName'],\
					shadowX = temp_shadowX, shadowY = temp_shadowY, shadowMax = temp_shadowMax, shadowName = temp_shadowName, \
					saveGraph=str(temp_graphSeq)+". SU_"+self.jobData[i4]['saveFN']+"_"+str(uti_count))
				uti_count += 1
				temp_graphSeq += 1
			
		self.showIt.showPlt()
			
	def printResult(self):
		result_i=0
		temp_count=0
		print "[Ave Waiting Time]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData1[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
		
		result_i=0
		print "[Ave Waiting Time (minute)]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData1[result_i]/60
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
		
		result_i=0
		temp_count=0
		print "[Ave Response Time]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData2[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
			
		result_i=0
		temp_count=0
		print "[Ave Slowdown]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData3[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
			
		result_i=0
		temp_count=0
		print "[Happy Job Number]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData4[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
		
		result_i=0
		temp_count=0
		print "[Ave System Utilization Ratio]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData5[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
		
		result_i=0
		temp_count=0
		print "[Loc]  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while (result_i<self.sysData['sim_Num']):
			print self.graphData8[result_i]
			result_i += 1
			temp_count += 1
			if (temp_count>=5):
				temp_count=0
				print "  "
		print " "
			
			
		
	def getWaitTime(self,inJobNum,inResUtis,indexNum):
		tempWT = 0.0
		tempNum=0.0
		self.dropQueue = []
		for i3 in range(inJobNum):
			tempNum=(inResUtis[i3]['start'] - inResUtis[i3]['submit'])
			tempWT += tempNum
			if (self.sysData['dropNum']>=1):
				self.checkDrop(tempNum)
				
		self.graphData1[indexNum] = (tempWT-self.addDrop())*1.0/(inJobNum-self.sysData['dropNum'])
		
	def getUtiRatio(self,inUti,inNodeNum,indexNum):
		tempItem=inUti[len(inUti)-1]
		tempTime=tempItem['time']

		temUti=0
		for item in inUti:
			temUti +=(item['uti']*1.00/inNodeNum)*item['inter']
		try:
			self.graphData5[indexNum] =temUti*100.00/tempTime
		except:
			self.graphData5[indexNum]=0
		
	def getResponseTime(self,inJobNum,inResUtis,indexNum2):
		tempRT = 0.0
		self.dropQueue = []
		for i3 in range(inJobNum):
			tempRT += (inResUtis[i3]['end'] - inResUtis[i3]['submit'])
			if (self.sysData['dropNum']>=1):
				self.checkDrop(inResUtis[i3]['end'] - inResUtis[i3]['submit'])
		self.graphData2[indexNum2] = (tempRT-self.addDrop())*1.0/(inJobNum-self.sysData['dropNum'])
		
	def getBSD(self,inJobNum,inResUtis,indexNum3):
		tempRT = 0.0
		tempRT3 = 0.0
		tempRT4 = 0.0	
		tempRT5 = 0.0	
		self.dropQueue = []
		for i3 in range(inJobNum):
			tempRT = (inResUtis[i3]['end'] - inResUtis[i3]['submit'])
			tempRT4 = inResUtis[i3]['run'] 
			if (tempRT4<10):
				tempRT4 = 10
			tempRT5 = tempRT*1.0/tempRT4 
			if (self.sysData['dropNum']>=1):
				self.checkDrop(tempRT5)
			tempRT3 += tempRT5
				
		self.graphData3[indexNum3] = ((tempRT3-self.addDrop())*1.0/(inJobNum-self.sysData['dropNum']))*1.0
		
	def getHappyNum(self,inJobNum,inResUtis,indexNum4):
		self.graphData4[indexNum4] = 0
		
		for jobResult in inResUtis:
			if (jobResult['start']<=jobResult['estStart']):
				self.graphData4[indexNum4] += 1
				
		
	def getSysUti(self,inSysUti,timeMode,timeIn,totalNode_in,indexNum4):
		temp_time=[]
		temp_Uti=[]
		temp_dis=0
		sep_num=0
		temp_len=len(inSysUti)
		self.maxWaitNum[indexNum4] = 0
		self.maxWaitSize[indexNum4] = 0
		for items in inSysUti:
			self.graphData6[indexNum4]['time'].append(items['time'])
			self.graphData6[indexNum4]['uti'].append(items['uti']*100.0/totalNode_in)
			self.graphData6[indexNum4]['time'].append(items['time']+items['inter'])
			self.graphData6[indexNum4]['uti'].append(items['uti']*100.0/totalNode_in)
			self.graphData9[indexNum4]['time'].append(items['time'])
			self.graphData9[indexNum4]['wait'].append(items['waitNum'])
			self.graphData10[indexNum4]['time'].append(items['time'])
			self.graphData10[indexNum4]['size'].append(items['waitSize'])
			if (items['waitNum']>self.maxWaitNum[indexNum4]):
				self.maxWaitNum[indexNum4]=items['waitNum']
			if (items['waitSize']>self.maxWaitSize[indexNum4]):
				self.maxWaitSize[indexNum4]=items['waitSize']
		x=self.graphData6[indexNum4]['time'].pop()
		self.graphData6[indexNum4]['uti'].pop()
		self.graphData7[indexNum4]={'min':inSysUti[0]['time'],'max':inSysUti[len(inSysUti)-1]['time']}
		#print self.graphData6[indexNum4]
		
		# timeMode: 0.time_dis  1.sep_num
		if (timeMode==0):
			temp_dis=int(timeIn)
			sep_num=int((self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])/temp_dis)
		else:
			sep_num=int(timeIn)
			temp_dis=int((self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])/sep_num)
		#if ((sep_num*timeIn)<(self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])):
			#sep_num += 1
		if (sep_num<1):
			sep_num = 1
		
		temp_index=0
		temp_i=0
		temp_i2=0
		temp_i3=0
		self.maxWaitNum_a[indexNum4] = 0
		while (temp_i<sep_num) :
			self.graphData6_a[indexNum4]['time'].append(temp_i*temp_dis+self.graphData7[indexNum4]['min'])
			self.graphData9_a[indexNum4]['time'].append(temp_i*temp_dis+self.graphData7[indexNum4]['min'])
			self.graphData10_a[indexNum4]['time'].append(temp_i*temp_dis+self.graphData7[indexNum4]['min'])
			while (temp_i2<temp_len):
				if (inSysUti[temp_i2]['time']+inSysUti[temp_i2]['inter']>self.graphData6_a[indexNum4]['time'][temp_i]):
					break
				temp_i2 += 1
			self.graphData6_a[indexNum4]['uti'].append(inSysUti[temp_i2]['uti']*100.0/totalNode_in)
			self.graphData9_a[indexNum4]['wait'].append(inSysUti[temp_i2]['waitNum'])
			self.graphData10_a[indexNum4]['size'].append(inSysUti[temp_i2]['waitSize'])
			if (inSysUti[temp_i2]['waitNum']>self.maxWaitNum_a[indexNum4]):
				self.maxWaitNum_a[indexNum4]=inSysUti[temp_i2]['waitNum']
			if (inSysUti[temp_i2]['waitSize']>self.maxWaitSize_a[indexNum4]):
				self.maxWaitSize_a[indexNum4]=inSysUti[temp_i2]['waitSize']
			temp_i += 1
			
		if (self.graphData6_a[indexNum4]['time'][sep_num-1]==self.graphData7[indexNum4]['max']):
			self.graphData6_a[indexNum4]['uti'][sep_num-1]=inSysUti[temp_len-2]['uti']*100.0/totalNode_in
			self.graphData9_a[indexNum4]['wait'][sep_num-1]=inSysUti[temp_len-2]['waitNum']
			self.graphData10_a[indexNum4]['size'][sep_num-1]=inSysUti[temp_len-2]['waitSize']
		else:
			self.graphData6_a[indexNum4]['time'].append(self.graphData7[indexNum4]['max'])
			self.graphData6_a[indexNum4]['uti'].append(inSysUti[temp_len-2]['uti']*100.0/totalNode_in)
			self.graphData9_a[indexNum4]['time'].append(self.graphData7[indexNum4]['max'])
			self.graphData9_a[indexNum4]['wait'].append(inSysUti[temp_len-2]['waitNum'])
			self.graphData10_a[indexNum4]['time'].append(self.graphData7[indexNum4]['max'])
			self.graphData10_a[indexNum4]['size'].append(inSysUti[temp_len-2]['waitSize'])
			if (inSysUti[temp_len-2]['waitNum']>self.maxWaitNum_a[indexNum4]):
				self.maxWaitNum_a[indexNum4]=inSysUti[temp_len-2]['waitNum']
			if (inSysUti[temp_len-2]['waitSize']>self.maxWaitSize_a[indexNum4]):
				self.maxWaitSize_a[indexNum4]=inSysUti[temp_len-2]['waitSize']
			
		temp_k = 0
		while (temp_k < self.sysData['aveUtiNum']):
			temp_index=0
			temp_i=0
			temp_i2=0
			temp_i3=0
			temp_dis_B = self.sysData['aveUti'][temp_k]
			#temp_dis=self.sysData['aveUti'][temp_k]
			#sep_num=(self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])/temp_dis+1
			temp_lastTime=0
			temp_partUti=0
			#print "[sep_num] " + str(sep_num)
			while (temp_i<sep_num) :
				self.graphData6_b[indexNum4]['time'][temp_k].append(temp_i*temp_dis+self.graphData7[indexNum4]['min'])
				temp_partUti = 0
				while (temp_i2<temp_len):
					if (inSysUti[temp_i2]['time']+inSysUti[temp_i2]['inter']>self.graphData6_b[indexNum4]['time'][temp_k][temp_i]):
						break
					temp_i2 += 1
					
				temp_lastTime=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]
				temp_i3 = temp_i2
				temp_timeSpend=0
				while (temp_i3>=0):
					if (inSysUti[temp_i3]['time']<=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]-temp_dis_B):
						temp_timeSpend += (temp_lastTime - self.graphData6_b[indexNum4]['time'][temp_k][temp_i]+temp_dis_B)
						temp_partUti+=(temp_lastTime - self.graphData6_b[indexNum4]['time'][temp_k][temp_i]+temp_dis_B)*inSysUti[temp_i3]['uti']*100.0/totalNode_in
						temp_lastTime=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]
						break
					else:
						temp_timeSpend += (temp_lastTime - inSysUti[temp_i3]['time'])
						temp_partUti+=(temp_lastTime - inSysUti[temp_i3]['time'])*inSysUti[temp_i3]['uti']*100.0/totalNode_in
						temp_lastTime=inSysUti[temp_i3]['time']
					temp_i3 -= 1
				if (temp_timeSpend!=0):
					self.graphData6_b[indexNum4]['uti'][temp_k].append(temp_partUti*1.0/temp_timeSpend)
				else:
					self.graphData6_b[indexNum4]['uti'][temp_k].append(0)
				temp_i += 1
				
			if (self.graphData6_b[indexNum4]['time'][temp_k][sep_num-1]!=self.graphData7[indexNum4]['max']):
				self.graphData6_b[indexNum4]['time'][temp_k].append(self.graphData7[indexNum4]['max'])
				temp_partUti = 0
				temp_lastTime=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]
				temp_i3= temp_len-1
				temp_timeSpend=0
				while (temp_i3>=0):
					if (inSysUti[temp_i3]['time']<=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]-temp_dis_B):
						temp_timeSpend += (temp_lastTime - self.graphData6_b[indexNum4]['time'][temp_k][temp_i]+temp_dis_B)
						temp_partUti+=(temp_lastTime - self.graphData6_b[indexNum4]['time'][temp_k][temp_i]+temp_dis_B)*inSysUti[temp_i3]['uti']*100.0/totalNode_in
						temp_lastTime=self.graphData6_b[indexNum4]['time'][temp_k][temp_i]
						break
					else:
						temp_timeSpend += (temp_lastTime - inSysUti[temp_i3]['time'])
						temp_partUti+=(temp_lastTime - inSysUti[temp_i3]['time'])*inSysUti[temp_i3]['uti']*100.0/totalNode_in
						temp_lastTime=inSysUti[temp_i3]['time']
					temp_i3 -= 1
				if (temp_timeSpend!=0):
					self.graphData6_b[indexNum4]['uti'][temp_k].append(temp_partUti*1.0/temp_timeSpend)
				else:
					self.graphData6_b[indexNum4]['uti'][temp_k].append(0)
				temp_i += 1
			temp_k += 1
		
		self.graphData6_b[indexNum4]['uti'].insert(0,self.graphData6_a[indexNum4]['uti'])
		self.graphData6_b[indexNum4]['time'].insert(0,self.graphData6_a[indexNum4]['time'])
		if (len(self.sysData['aveUtiName'])<len(self.graphData6_b[indexNum4]['time'])):
			self.sysData['aveUtiName'].insert(0,"System Utilization")
		self.timeSpaceCal(self.sysData['timeSpace'],indexNum4)
		
	def getSysFraRatio(self,inUti,inNodeNum,indexNum5):
		tempItem=inUti[len(inUti)-1]
		tempTime=tempItem['time']

		temUti=0
		#print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		for item in inUti:
			temUti +=((inNodeNum-item['uti'])*item['delta']*1.00/inNodeNum)*item['inter']
			#print "             "+str(item)
		try:
			self.graphData8[indexNum5] =temUti*100.00/tempTime
		except:
			self.graphData8[indexNum5]=0
		#print "<"+str(indexNum5)+">  "+str(self.graphData8[indexNum5])+"    "+str(temUti)+"    "+str(tempTime)
		

	def checkDrop(self,in_value):
		drop_i=0
		while (drop_i < self.sysData['dropNum'] and drop_i<len(self.dropQueue)):
			if (self.dropQueue[drop_i]>in_value):
				break
			drop_i+=1
		self.dropQueue.insert(drop_i,in_value)
		if (len(self.dropQueue)>self.sysData['dropNum']):
			self.dropQueue.pop(0)
			
	def addDrop(self):
		drop_i=0
		temp_dropR=0
		while (drop_i < self.sysData['dropNum']):
			#print drop_i
			temp_dropR += self.dropQueue[drop_i]
			drop_i+=1
		return temp_dropR
		
	def timeSpaceCal(self,inGraphSpace,indexNum6):
		temp_start=0
		temp_end=temp_start
		temp_i5=0
		temp_len=len(self.graphData6_a[indexNum6]['time'])
		#print self.graphData6[indexNum6]['time']
		while (temp_i5<temp_len):
			temp_end=temp_i5
			if ((self.graphData6_a[indexNum6]['time'][temp_end]-self.graphData6_a[indexNum6]['time'][temp_start])>=inGraphSpace or temp_i5==(temp_len-1)) :
				self.graphData11[indexNum6].append([temp_start,temp_end+1])
				#print [temp_start,temp_end]
				temp_start=temp_i5
			temp_i5 += 1
		#print "xxxxxxxxx   " + str(temp_i5)
	
a = MainProgram()
a.init()

a.set_AveUtiInter([3600,36000,86400],["1 hr","10 hr","1 day"],600,604800)
a.set_submitDensity(1.0)
a.set_dropPercent(0)
a.set_graph_uti(10,2)
a.set_fileType(".rst",".uti")

a.set_SWFfile("CTC-SP2-1996-3.1-cln.swf","CTC-SP2",5000)
'''
a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",1,'k',"1",color="darkred")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",1,'k',"2",color="darkred")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",1,'k',"3",color="darkred")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",1,'k',"4",color="darkred")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",1,'k',"5",color="darkred")

a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",2,'k',"1",color="darkblue")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",2,'k',"2",color="darkblue")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",2,'k',"3",color="darkblue")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",2,'k',"4",color="darkblue")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",2,'k',"5",color="darkblue")

a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",3,'k',"1",color="orange")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",3,'k',"2",color="orange")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",3,'k',"3",color="orange")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",3,'k',"4",color="orange")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",3,'k',"5",color="orange")

a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",4,'k',"1",color="darkgreen")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",4,'k',"2",color="darkgreen")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",4,'k',"3",color="darkgreen")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",4,'k',"4",color="darkgreen")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",4,'k',"5",color="darkgreen")

a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",5,'k',"1",color="purple")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",5,'k',"2",color="purple")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",5,'k',"3",color="purple")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",5,'k',"4",color="purple")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",5,'k',"5",color="purple")
'''

a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",1,'k',"1",color="darkred")
a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",2,'k',"1",color="darkblue")
a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",3,'k',"1",color="orange")
a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",4,'k',"1",color="darkgreen")
a.addTask("1.0*(w*100.0/z)+0.0*(l*100/t)",5,'k',"1",color="purple")

a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",1,'k',"2",color="darkred")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",2,'k',"2",color="darkblue")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",3,'k',"2",color="orange")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",4,'k',"2",color="darkgreen")
a.addTask("0.75*(w*100.0/z)+0.25*(l*100/t)",5,'k',"2",color="purple")

a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",1,'k',"3",color="darkred")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",2,'k',"3",color="darkblue")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",3,'k',"3",color="orange")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",4,'k',"3",color="darkgreen")
a.addTask("0.5*(w*100.0/z)+0.5*(l*100/t)",5,'k',"3",color="purple")

a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",1,'k',"4",color="darkred")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",2,'k',"4",color="darkblue")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",3,'k',"4",color="orange")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",4,'k',"4",color="darkgreen")
a.addTask("0.25*(w*100.0/z)+0.75*(l*100/t)",5,'k',"4",color="purple")

a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",1,'k',"5",color="darkred")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",2,'k',"5",color="darkblue")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",3,'k',"5",color="orange")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",4,'k',"5",color="darkgreen")
a.addTask("0.0*(w*100.0/z)+1.0*(l*100/t)",5,'k',"5",color="purple")

#a.startSImulation()
a.readJobResult()
a.analysisResult()
a.printResult()
a.showResUtiG()

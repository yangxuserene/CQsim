import sys
sys.path.append('/home/JobSchedule_SIM/')

import InputManager
import ShowGraph
#import SimulatorProc2 as SimulatorProc

#import SimulatorProc_old as SimulatorProc
import SimulatorProc

__metaclass__ = type
class MainProgram:
	def init(self,aveUti_in):
		self.aveUti=aveUti_in
		self.graphColor=[]	#bar color
		self.graphData1=[]	#waiting time
		self.graphData2=[]	#response time
		self.graphData3=[]	#BSD
		self.graphData4=[]	#happyness job number
		self.graphData5=[]	#system utilization ratio
		self.graphData6=[]	#system utilization single (time/uti) exactly
		self.graphData6_a=[]	#system utilization single (time/uti) every n time
		self.graphData7=[]	#system utilization single (min_start/max_end)
		self.graphData8=[]	#system fragment
		self.outputFN=[]
		self.sim_Num = 0
		self.aveUtiNum=len(aveUti_in)
		self.showIt = ShowGraph.ShowGraph()
		self.showIt.init()
		self.showIt.resetPara(1,['unname'])
		self.algNames =[]
		self.taskParameter=[]
		# algs: string
		# BFmode: int
		# name: string
		
	def addTask(self,prioStr_in,winSize_in,BFmode_in,algName_in,FN_in,color_in):
		self.taskParameter.append({'algs':prioStr_in,'BFmode':BFmode_in,'name':algName_in,'winSize':winSize_in})
		self.graphColor.append(color_in)	#bar color
		self.graphData1.append(0.0)	#waiting time
		self.graphData2.append(0.0)	#response time
		self.graphData3.append(0.0)	#BSD
		self.graphData4.append(0)	#happyness job number
		self.graphData5.append(0.0)	#system utilization ratio
		self.graphData6.append({'time':[],'uti':[]})    #system utilization single (time/uti) exactly
		self.graphData6_a.append({'time':[],'uti':[]})    #system utilization single (time/uti) every n time
		i=0
		self.graphData7.append({'min':0,'max':0})    #system utilization single (min_start/max_end)
		self.graphData8.append(0.0)	#system fragment
		self.algNames.append(algName_in)
		self.outputFN.append(FN_in)
		self.sim_Num += 1
		
	def startSImulation(self, fileName):
		self.IM=InputManager.InputManager()
		self.IM.init()
		self.IM.setSubmitPara(1)
		self.simulator=SimulatorProc.SimulatorProc()
		self.IM.SWFReader(fileName)
		self.simulator.init()
		self.simulator.dataIn(self.IM.getSWFData(),self.IM.getSysInfo())
		self.simulator.parameterIn(self.IM.getJobNum(),self.IM.getNodeStruc())
		ttt = self.simulator.getResult()
		
		print"+++++++++++++++++++++++++++++++++++++++++++++++"
		print "Job Number: " + str(self.IM.getJobNum())
		print "CPU Number: " + str(self.IM.getNodeStruc())
		for j2 in range(self.IM.getJobNum()):
			print str(ttt[j2])
		print"+++++++++++++++++++++++++++++++++++++++++++++++"
		
		for i2 in range(self.sim_Num):
			self.IM.setBackFilling(self.taskParameter[i2]['BFmode'])
			self.IM.scheAlgorithmIn(self.taskParameter[i2]['algs'])
			self.IM.setWinSize(self.taskParameter[i2]['winSize'])
			self.simulator.dataIn(self.IM.getSWFData(),self.IM.getSysInfo())
			self.simulator.parameterIn(self.IM.getJobNum(),self.IM.getNodeStruc())
			self.simulator.winSizeIn(self.IM.getWinSize())
			self.simulator.paraReset()
			print (">>>>>>>>>>>>>>>>>>>>>>  ALG: " + str(self.taskParameter[i2]['name'])+" (" +str(self.taskParameter[i2]['algs'])+")")
			if (self.IM.algorithmCheck() <= 0):
				print "Algorithm \""+str(self.taskParameter[i2]['algs'])+"\" illegal!"
				break
			else:
				self.simulator.prioFuncIn(self.IM.getPrioFunc(),self.IM.getBFStr())
				self.simulator.beginSimulation()
				self.simulator.exportResult(self.outputFN[i2])
				tempR=self.simulator.getResult()
				tempR3=self.simulator.getSysUti()
				for j3 in range(self.IM.getJobNum()):
					print str(tempR[j3])+"   "+str(tempR[j3]['start'] - tempR[j3]['submit'])
				'''
				for j4 in range(len(tempR3)):
					print str(tempR3[j4])
				'''
				self.getWaitTime(self.IM.getJobNum(),tempR,i2)
				self.getResponseTime(self.IM.getJobNum(),tempR,i2)
				self.getBSD(self.IM.getJobNum(),tempR,i2)
				self.getUtiRatio(tempR3,self.IM.getNodeStruc(),i2)
				self.getSysFraRatio(tempR3,self.IM.getNodeStruc(),i2)
				self.getHappyNum(self.IM.getJobNum(),self.simulator.getHappyNum(),i2)
				self.getSysUti(tempR3,0,600,i2)
				
		
	def showResUtiG(self):
		tempR4=self.simulator.getResult()
		self.showIt.resetPara(self.sim_Num,self.algNames)
		
		self.showIt.graphA(1,self.graphData1,self.graphColor,"Overall Average Waiting Time(sec)")
		self.showIt.graphA(2,self.graphData2,self.graphColor,"Overall Average Response Time(sec)")
		self.showIt.graphA(3,self.graphData3,self.graphColor,"Overall Average Slowdown")
		self.showIt.graphA(4,self.graphData4,self.graphColor,"Happy Job Number")
		self.showIt.graphB(5,self.graphData4,self.IM.getJobNum(),self.graphColor,"Happy Job Ratio")
		self.showIt.graphB(6,self.graphData5,self.IM.getNodeStruc(),self.graphColor,"System Utilization")
		self.showIt.graphB(7,self.graphData8,self.IM.getNodeStruc(),self.graphColor,"Loss Of Capacity")

		for i4 in range(self.sim_Num):
			#self.showIt.graphC(8+i4,self.graphData6[i4]['time'], self.graphData6[i4]['uti'],self.IM.getNodeStruc(), self.graphData7[i4]['min'], self.graphData7[i4]['max'], 10, "System Utilization\n("+str(self.taskParameter[i4]['algs'])+"   BF:"+str(self.taskParameter[i4]['BFmode'])+"   WIN:"+str(self.taskParameter[i4]['winSize'])+")")
			self.showIt.graphD(8+i4,self.graphData6_a[i4]['time'], self.graphData6_a[i4]['uti'],self.IM.getNodeStruc(), self.graphData7[i4]['min'], self.graphData7[i4]['max'], 10, "System Utilization\n("+str(self.taskParameter[i4]['algs'])+"   BF:"+str(self.taskParameter[i4]['BFmode'])+"   WIN:"+str(self.taskParameter[i4]['winSize'])+")")
		
		
		self.showIt.showPlt()
		self.showIt.savePlt()
		
	def getWaitTime(self,inJobNum,inResUtis,indexNum):
		tempWT = 0.0
		tempNum=0.0
		for i3 in range(inJobNum):
			tempNum=(inResUtis[i3]['start'] - inResUtis[i3]['submit'])
			tempWT += tempNum
				
		self.graphData1[indexNum] = tempWT/inJobNum
		
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
		for i3 in range(inJobNum):
			tempRT += (inResUtis[i3]['end'] - inResUtis[i3]['submit'])
		self.graphData2[indexNum2] = tempRT*1.0/inJobNum
		
	def getBSD(self,inJobNum,inResUtis,indexNum3):
		tempRT = 0.0
		tempRT3 = 0.0
		tempRT4 = 0.0	
		tempRT5 = 0.0	
		for i3 in range(inJobNum):
			tempRT = (inResUtis[i3]['end'] - inResUtis[i3]['submit'])
			tempRT4 = inResUtis[i3]['run'] 
			if (tempRT4<10):
				tempRT4 = 10
			tempRT5 = tempRT*1.0/tempRT4 
			tempRT3 += tempRT5
				
		self.graphData3[indexNum3] = (tempRT3*1.0/inJobNum)*1.0
		
	def getHappyNum(self,inJobNum,inResUtis,indexNum4):
		self.graphData4[indexNum4] = inResUtis
		
	def getSysUti(self,inSysUti,timeMode,timeIn,indexNum4):
		temp_time=[]
		temp_Uti=[]
		temp_dis=0
		sep_num=0
		temp_len=len(inSysUti)
		for items in inSysUti:
			self.graphData6[indexNum4]['time'].append(items['time'])
			self.graphData6[indexNum4]['uti'].append(items['uti'])
			self.graphData6[indexNum4]['time'].append(items['time']+items['inter'])
			self.graphData6[indexNum4]['uti'].append(items['uti'])
		x=self.graphData6[indexNum4]['time'].pop()
		self.graphData6[indexNum4]['uti'].pop()
		self.graphData7[indexNum4]={'min':inSysUti[0]['time'],'max':inSysUti[len(inSysUti)-1]['time']}
		#print self.graphData6[indexNum4]
		
		# timeMode: 0.time_dis  1.sep_num
		if (timeMode==0):
			temp_dis=timeIn
			sep_num=(self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])/timeIn
		else:
			temp_dis=(self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])/timeIn
			sep_num=timeIn
		#if ((sep_num*timeIn)<(self.graphData7[indexNum4]['max']-self.graphData7[indexNum4]['min'])):
			#sep_num += 1
		
		temp_index=0
		temp_i=0
		temp_i2=0
		temp_i3=0
		while (temp_i<sep_num) :
			self.graphData6_a[indexNum4]['time'].append(temp_i*temp_dis+self.graphData7[indexNum4]['min'])
			while (temp_i2<temp_len):
				if (inSysUti[temp_i2]['time']+inSysUti[temp_i2]['inter']>self.graphData6_a[indexNum4]['time'][temp_i]):
					break
				temp_i2 += 1
			self.graphData6_a[indexNum4]['uti'].append(inSysUti[temp_i2]['uti'])
			temp_i += 1
		if (self.graphData6_a[indexNum4]['time'][sep_num-1]==self.graphData7[indexNum4]['max']):
			self.graphData6_a[indexNum4]['uti'][sep_num-1]=inSysUti[temp_len-2]['uti']
		else:
			self.graphData6_a[indexNum4]['time'].append(self.graphData7[indexNum4]['max'])
			self.graphData6_a[indexNum4]['uti'].append(inSysUti[temp_len-2]['uti'])
			
				
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
		

a = MainProgram()
a.init([3600,36000,86400])
'''
a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",5,'0',"1\n0","JS_W5_B0_A100","darkblue")
a.addTask("0.65*(w*100.0/z)+0.35*(l*100/t)",5,'0',"0.65\n0.35","JS_W5_B0_A065","darkblue")
a.addTask("0.35*(w*100.0/z)+0.65*(l*100/t)",5,'0',"0.35\n0.65","JS_W5_B0_A035","darkblue")
a.addTask("0*(w*100.0/z)+1.0*(l*100/t)",5,'0',"0\n1","JS_W5_B0_A000","darkblue")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",5,'k',"1\n0\n*","JS_W5_Bk_A100","orange")
a.addTask("0.65*(w*100.0/z)+0.35*(l*100/t)",5,'k',"0.65\n0.35\n*","JS_W5_Bk_A065","orange")
a.addTask("0.35*(w*100.0/z)+0.65*(l*100/t)",5,'k',"0.35\n0.65\n*","JS_W5_Bk_A035","orange")
a.addTask("0*(w*100.0/z)+1.0*(l*100/t)",5,'k',"0\n1\n*","JS_W5_Bk_A000","orange")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",5,'c',"1\n0\n**","JS_W5_Bc_A100","darkgreen")
a.addTask("0.65*(w*100.0/z)+0.35*(l*100/t)",5,'c',"0.65\n0.35\n**","JS_W5_Bc_A065","darkgreen")
a.addTask("0.35*(w*100.0/z)+0.65*(l*100/t)",5,'c',"0.35\n0.65\n**","JS_W5_Bc_A035","darkgreen")
a.addTask("0*(w*100.0/z)+1.0*(l*100/t)",5,'c',"0\n1\n**","JS_W5_Bc_A000","darkgreen")
'''
a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",1,'k',"1\n0\n*","JS_W1_Bk_A100","darkred")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",2,'k',"1\n0\n**","JS_W2_Bk_A100","darkblue")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",3,'k',"1\n0\n***","JS_W3_Bk_A100","orange")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",4,'k',"1\n0\n****","JS_W4_Bk_A100","darkgreen")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",5,'k',"1\n0\n****","JS_W5_Bk_A100","yellow")


a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",1,'0',"1\n0\n*","JS_W1_Bk_A100","darkred")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",2,'0',"1\n0\n**","JS_W2_Bk_A100","darkblue")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",3,'0',"1\n0\n***","JS_W3_Bk_A100","orange")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",4,'0',"1\n0\n****","JS_W4_Bk_A100","darkgreen")

a.addTask("1.0*(w*100.0/z)+0*(l*100/t)",5,'0',"1\n0\n****","JS_W5_Bk_A100","yellow")



a.startSImulation("test6.swf")
a.showResUtiG()
from copy import deepcopy
__metaclass__ = type
class SimulatorProc:
	def init(self):
		self.jobList_s = []
		self.sysInfo_s = {'jobNum':0, 'nodeNum':0, 'prioFunc':"w", 'BFMode':0, 'BFModeStr':'0','winSize':1}
		self.winSize_s=1
	
	# Data Input/Set Method
	def parameterIn(self, jobNumInB,nodeNumInB):
		self.jobNum_s = jobNumInB
		self.nodeNum_s = nodeNumInB
		self.sysInfo_s['jobNum'] = jobNumInB
		self.sysInfo_s['nodeNum'] = nodeNumInB
		
	def prioFuncIn(self,prioFuncInB,inBFStr):
		self.prioFunc_s = prioFuncInB
		self.BFModeStr=inBFStr
		try:
			k=self.waitNum_s
			c=self.winSize_s
			self.BFMode = eval(self.BFModeStr)
		except:
			self.BFMode = 0
		self.sysInfo_s['prioFunc'] = prioFuncInB
		self.sysInfo_s['BFMode'] = self.BFMode
		self.sysInfo_s['BFModeStr'] = self.BFModeStr
	
	def dataIn(self,jobListInB,sysInfoInB):
		self.jobList_s = jobListInB
		self.sysInfo_s = sysInfoInB
		for item in self.jobList_s:
			item['state'] = 0
			item['score'] = 0
			item['start'] = -1
			item['end'] = -1
			item['happy'] = -1
				
	def winSizeIn(self,winIn):
		self.winSize_s=winIn
		if (self.winSize_s<1):
			self.winSize_s=1
		self.sysInfo_s['winSize'] = self.winSize_s
				
	def paraReset(self):
		self.idleNode_s = self.nodeNum_s
		self.jobIndex_s = 0
		self.waitNum_s = 0
		self.runNum_s = 0
		self.jobDoneNum_s = 0
		self.jobStartNum_s = 0
		self.nextEventTime_s = 0
		self.nextJob_s = 0
		self.restIndex_s = 0
		self.startControl = 0
		self.currentTime_s = int(self.jobList_s[0]['submit'])
		self.startTime_s = int(self.jobList_s[0]['submit'])
		self.waitList_s = []
		self.activeJobTrack_s = []
		self.runList_s = []
		self.forecast_s = []
		# time: finish time     index: job index     node: req node
		self.fcNum_s = 0
		self.nextFinishJob = 0
		self.happyNum=0
		self.happyNum2= 0
		self.happyList = []
		self.total_waitTime = 0
		self.total_BSD = 0
		self.total_respTime = 0
		self.ave_waitTime = 0
		self.ave_BSD = 0
		self.ave_respTime = 0
		self.systemUti=[]
		self.ave_uti=0
		self.pre_uti=-1
		self.backCollect=[]
		self.winCount_s=0
				
	# Simulation Method
	def beginSimulation(self):
		while (self.jobDoneNum_s < self.jobNum_s):
			self.currentTime_s += self.nextEventTime_s
			print "--------------------------"+str(self.currentTime_s) + "  (+"+str(self.nextEventTime_s)+")"
			print str(self.jobIndex_s)+"  " + str(self.jobStartNum_s)+"  " + str(self.jobDoneNum_s) +"  " + str(self.jobNum_s)
			print str(self.waitNum_s)+"  " + str(self.runNum_s)+"  [Next Job: " + str(self.nextJob_s) +"  " + str(self.idleNode_s) +"   "+str(self.jobList_s[self.nextJob_s ]['state'])+"]"

			if (self.jobList_s[self.nextJob_s ]['state'] == 2 and self.runNum_s>0):
				self.jobFinish(self.nextJob_s,self.nextFinishJob,self.currentTime_s)
				#print "Wait:"+str(self.ave_waitTime)+"  BSD:" + str(self.ave_BSD)+"  Response:"+ str(self.ave_respTime)
				
			if (self.jobList_s[self.nextJob_s ]['state'] == 0 and self.jobIndex_s<self.jobNum_s):
				self.jobSubmit(self.jobIndex_s)
				
			#print "<w>  "+str(self.waitList_s)
			#print "<r>  "+str(self.runList_s)
			#print "  [idle: " +"  " + str(self.idleNode_s) +"]"
			if (self.waitNum_s > 0):
				self.jobStartScan()
				
			self.nextFinishJob = self.findNext()
			self.collectSysUti()
			#print "Ave Sys Uti: "+str(self.ave_uti)
		print  self.backCollect
	
	def prioCalcu(self):
		self.nextState_s = 0
		i = 0
		tempResult=-1
		if (self.waitNum_s<=0):
			return -1
		else:
			i=0
			z=self.currentTime_s-self.jobList_s [self.waitList_s[0]]['submit']
			l=self.jobList_s [self.waitList_s[0]]['reqTime']
			while (i<self.waitNum_s):
				temp_w=self.currentTime_s-self.jobList_s [self.waitList_s[i]]['submit']
				if (temp_w>z):
					z=temp_w
				if (self.jobList_s [self.waitList_s[i]]['reqTime']<l):
					l=self.jobList_s [self.waitList_s[i]]['reqTime']
				i+=1
			i=0
			if (z == 0):
				z = 1
			while (i<self.waitNum_s):
				s = int(self.jobList_s [self.waitList_s[i]]['submit'])
				t = int(self.jobList_s [self.waitList_s[i]]['reqTime'])
				n = int(self.jobList_s [self.waitList_s[i]]['reqNode'])
				w = int(self.currentTime_s - s)
				m = int(self.idleNode_s)
				self.jobList_s[self.waitList_s[i]]['score'] = eval(self.prioFunc_s)
				i += 1
			tempResult=i
		self.waitList_s.sort(self.scoreCmp)
		#self.winSche()
		return tempResult
		
	def winSche(self):	
		maxWinSize = 5
		self.winCount_s=0
		waitJobWin=[]
		winIndex=[1,1,1,1,1]
		tempI=[0,0,0,0,0]
		tempNumList=[-1,-1,-1,-1,-1]
		jobIndexList=[]
		tempJobList=[]
		tempWinSize=self.winSize_s
		if (self.winSize_s>self.waitNum_s):
			tempWinSize=self.waitNum_s
		
		tempWinSize2 = 1
		t1 = 1
		while (t1<= tempWinSize):
			tempWinSize2=tempWinSize2*t1
			winIndex[maxWinSize-t1]=t1
			tempJobList.append(self.waitList_s[t1-1])
			t1 += 1
		t1 = 0
		while (t1< maxWinSize):
			jobIndexList.append(tempJobList)
			t1 += 1
		t1 = 0
		while (t1< tempWinSize2):
			waitJobWin.append([])
			t1 += 1
			
		#print "ccc  "+str(self.waitNum_s)+"    "+ str(winIndex)
		tpemp_countA=0
		while (tempI[0]<winIndex[0]):
			jobIndexList[1]=jobIndexList[0][:]
			if (winIndex[0]>1):
				tempNumList[0]=jobIndexList[1].pop(tempI[0])
			tempI[1]=0
			
			while (tempI[1]<winIndex[1]):
				jobIndexList[2]=jobIndexList[1][:]
				if (winIndex[1]>1):
					tempNumList[1]=jobIndexList[2].pop(tempI[1])
				tempI[2]=0
					
				while (tempI[2]<winIndex[2]):	
					jobIndexList[3]=jobIndexList[2][:]
					if (winIndex[2]>1):
						tempNumList[2]=jobIndexList[3].pop(tempI[2])
					tempI[3]=0
			
					while (tempI[3]<winIndex[3]):	
						jobIndexList[4]=jobIndexList[3][:]
						if (winIndex[3]>1):
							tempNumList[3]=jobIndexList[4].pop(tempI[3])
						tempNumList[4]=jobIndexList[4].pop()
							
						temp_countB=0
						while (temp_countB<maxWinSize):
							if (tempNumList[temp_countB]!=-1):
								waitJobWin[tpemp_countA].append(tempNumList[temp_countB])
							temp_countB+=1
						tpemp_countA += 1
						
						tempI[3] += 1
					tempI[2] += 1
				tempI[1] += 1
			tempI[0] += 1
		'''	
		print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		t1 = 0
		while (t1< tempWinSize2):
			print str(waitJobWin[t1])
			t1 += 1
		print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		'''
		i2 = 0
		j2 = 0
		scheList3=[]
		scheList3.append({'time':self.currentTime_s, 'node':self.idleNode_s})
		temp_max2=1
		#print scheList3
		#print self.forecast_s
		#print "xxx   "+str(tempWinSize)+"   "+str(tempWinSize2)+"   "+str(self.waitNum_s) +"   "+str(self.winSize_s)
		while (j2 < self.runNum_s):
			#print "xxx   "+str(j2)+"   "+str(i2)
			if (self.forecast_s[j2]['time']!=scheList3[i2]['time']):
				scheList3.append({'time':self.forecast_s[j2]['time'], 'node':scheList3[i2]['node']+self.forecast_s[j2]['node']})
				i2+= 1
				temp_max2 += 1
			else:
				scheList3[i2]['node']=scheList3[i2]['node']+self.forecast_s[j2]['node']
			j2+= 1
		
		j2 = 0
		while (j2 < temp_max2):
			#print scheList3[j2]
			j2 += 1
		temp_max2_store = temp_max2
		minValue=-1
		minValue_start=-1
		selectedOrder=[]
		
		
		for jobTry in waitJobWin:
			scheList2=[]
			i2 = 0
			temp_max2 = temp_max2_store
			while (i2 < temp_max2):
				scheList2.append({'time':scheList3[i2]['time'], 'node':scheList3[i2]['node']})
				i2 += 1
				
			temp_point2=0
			i2=0
			#print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
			#print scheList2
			while (i2<tempWinSize):
				i3 = temp_point2
				temp_time3=0
				while (i3 < temp_max2):
					#print str(jobTry)+"   "+str(temp_max2)
					if (self.jobList_s[jobTry[i2]]['reqNode']<=scheList2[i3]['node']):
						scheList2[i3]['node'] -= self.jobList_s[jobTry[i2]]['reqNode']
						temp_time3=self.jobList_s[jobTry[i2]]['reqTime']+scheList2[i3]['time']
						break
					else:
						temp_point2 += 1
					i3 += 1
				i3=temp_point2+1
				temp_add2=0
				while (i3<temp_max2):
					if (temp_time3<scheList2[i3]['time']):
						scheList2.insert(i3,{'time':temp_time3, 'node':scheList2[i3-1]['node']+self.jobList_s[jobTry[i2]]['reqNode']})
						temp_max2 += 1
						temp_add2=1
						break
					elif (temp_time3==scheList2[i3]['time']):
						temp_add2=1
						break
					else:
						scheList2[i3]['node'] -= self.jobList_s[jobTry[i2]]['reqNode']
					i3 += 1
				if (temp_add2==0):
					scheList2.append({'time':temp_time3, 'node':scheList2[temp_max2-1]['node']+self.jobList_s[jobTry[i2]]['reqNode']})
					temp_max2 += 1
				#print "      ID:"+ str(jobTry[i2])+"   Node:"+ str(self.jobList_s[jobTry[i2]]['reqNode'])+"   Time:"+ str(self.jobList_s[jobTry[i2]]['reqTime'])
				#print scheList2
				i2+=1
			#print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
			
			#print "[jobTry]   "+ str(jobTry)
			#print "[scheList2]   "+ str(scheList2)
			#print "[info]  "+str(minValue)+"   "+str(scheList2[temp_max2-1]['time'])
			if (minValue<0 or minValue>scheList2[temp_max2-1]['time']):
				#if (minValue<0):
					#print "[--------]  " + str(jobTry)+"    \t"+str(scheList2[temp_max2-1]['time'])+"    \t"+str(scheList2[temp_point2]['time'])
				minValue=scheList2[temp_max2-1]['time']
				minValue_start=scheList2[temp_point2]['time']
				#print "[info222]  "+str(minValue)+"   "+str(scheList2[temp_max2-1]['time'])
				selectedOrder=jobTry
			elif (minValue==scheList2[temp_max2-1]['time'] and minValue_start>scheList2[temp_point2]['time']):
				minValue=scheList2[temp_max2-1]['time']
				minValue_start=scheList2[temp_point2]['time']
				#print "[info222]  "+str(minValue)+"   "+str(scheList2[temp_max2-1]['time'])
				selectedOrder=jobTry
				
		#print "[#-------]  " + str(selectedOrder)+"    \t"+str(minValue)+"    \t"+str(minValue_start)
		i2 = 0
		#print "zzzzzzzzzzzz          "+str(tempWinSize2)
		while (i2<tempWinSize):
			#print "xxxxxxxxxxxx    "+str(selectedOrder[i2])
			self.waitList_s[i2]=selectedOrder[i2]
			i2 += 1

		
	def findNext(self):
		self.nextEventTime_s = 0
		jobResult = 0
		if (self.runNum_s>0):
			self.nextEventTime_s=int(self.jobList_s [self.runList_s[0]]['run'])+int(self.jobList_s[self.runList_s[0]]['start'])-self.currentTime_s
			self.nextJob_s=self.runList_s [0]
			for i in  range(self.runNum_s):
				self.tempA=int(self.jobList_s [self.runList_s[i]]['run'])+int(self.jobList_s[self.runList_s[i]]['start'])-self.currentTime_s
				if (self.tempA<self.nextEventTime_s):
					self.nextEventTime_s=self.tempA
					self.nextJob_s=self.runList_s [i]
					jobResult=i
		if (self.jobIndex_s<self.jobNum_s):
			if ((int(self.jobList_s[self.jobIndex_s]['submit'])-self.currentTime_s)<self.nextEventTime_s) or (self.runNum_s <= 0):
				self.nextEventTime_s=int(self.jobList_s[self.jobIndex_s]['submit'])-self.currentTime_s
				self.nextJob_s=self.jobIndex_s
		return jobResult
		
	def scoreCmp(self,jobIndex_c1,jobIndex_c2):
		return -cmp(self.jobList_s[jobIndex_c1]['score'],self.jobList_s[jobIndex_c2]['score'])
		
	#Job Action Method
			
	def jobStartScan(self):	
			tempA=0
			tempB=0
			tempTime=0
			tempSpace=0
			tempRestNode=0
			tempNode=0
			temp_wait=0
			temp_point=0
			temp_max=0
			self.startControl = 0
			checkedNum = 0
			self.winCount_s=self.winSize_s
			scheList=[]
			if (self.jobStartNum_s<self.jobNum_s):
							
				while (tempA <self.waitNum_s):
					#print "[????????????]   "+str(tempA)+"   "+str(self.jobList_s[self.waitList_s[tempA]]['state'] )+"   "+str(self.startControl)
					if (self.winCount_s>=self.winSize_s):
						self.winSche()
					if (int(self.idleNode_s)<int(self.jobList_s[self.waitList_s[tempA]]['reqNode']) or self.startControl==1):
						try:
							k=self.waitNum_s
							c=self.winSize_s-self.winCount_s
							self.BFMode = eval(self.BFModeStr)
						except:
							self.BFMode = 0
							
						if (self.BFMode == 0):
							# no backfilling
							#print "[BackFillMode XXX]  "+str(self.BFMode) +"        "+str(self.winSize_s) +"        "+str(self.winCount_s) +"        "
							break
						else :
							if (self.idleNode_s<=0):
								#print "[BackFillMode XXX]  "+str(self.BFMode)+"        "+str(self.winSize_s) +"        "+str(self.winCount_s) +"        "+"        "+str(self.idleNode_s) 
								break
							else:
								if (self.startControl==0):
									#print "[BackFillMode]  "+str(self.BFMode)
									self.startControl = 1
									scheList.append({'time':self.currentTime_s, 'node':self.idleNode_s, 'min':self.idleNode_s})
									i = 0
									j = 0
									temp_max=1
									
									while (j < self.runNum_s):
										if (self.forecast_s[j]['time']!=scheList[i]['time']):
											scheList.append({'time':self.forecast_s[j]['time'], 'node':scheList[i]['node']+self.forecast_s[j]['node'], 'min':scheList[0]['node']})
											i+= 1
											temp_max += 1
										else:
											scheList[i]['node']=scheList[i]['node']+self.forecast_s[j]['node']
										j+= 1
								#print "[checkNum] "+str(checkedNum)+ "    "+str(self.waitList_s[tempA]) + "    "+str(self.jobList_s[self.waitList_s[tempA]]) 
								if (self.jobList_s[self.waitList_s[tempA]]['reqNode']<=self.idleNode_s):
									i = 0
									temp_time2=self.jobList_s[self.waitList_s[tempA]]['reqTime']+self.currentTime_s
									#print "[compareB "+str(self.waitList_s[tempA])+" ]  "+str(temp_time2)+"   "+str(scheList[temp_max-1]['time'])+"   "+str(self.jobList_s[self.waitList_s[tempA]]['reqNode'])+"   "+str(scheList[temp_max-1]['min'])
									
									if (temp_time2>scheList[temp_max-1]['time']):
										#print "[*compareB "+str(self.waitList_s[tempA])+" ]  "+str(self.jobList_s[self.waitList_s[tempA]]['reqNode'])+"   "+str(scheList[temp_max-1]['min'])
										if (self.jobList_s[self.waitList_s[tempA]]['reqNode']<=scheList[temp_max-1]['min']):
											# Back fill the job
											j=0
											while (j<temp_max):
												scheList[j]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
												j += 1
											scheList.append({'time':temp_time2, 'node':scheList[temp_max-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode'], 'min':scheList[temp_max-1]['min']})
											temp_max += 1
											temp_min=scheList[0]['node']
											j=0
											while (j<temp_max):
												if (temp_min>scheList[j]['node']):
													temp_min = scheList[j]['node']
												scheList[j]['min'] = temp_min
												j += 1
											self.backCollect.append(self.waitList_s[tempA])
											print "[Back] "+str(self.waitList_s[tempA]) + "  " +str(self.jobList_s[self.waitList_s[tempA]]['id']) + "  "+ str(tempA)+"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
											self.jobStart(self.waitList_s[tempA],tempA,self.currentTime_s)
											tempA -= 1
									else:
										while (i<temp_max):
											if (temp_time2<=scheList[i]['time']):
												if (self.jobList_s[self.waitList_s[tempA]]['reqNode']<=scheList[i-1]['min']):
													# Back fill the job
													j=0
													while (j<i):
														scheList[j]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
														j += 1
													if (temp_time2==scheList[j]['time']):
														scheList[j]['node']=scheList[j]['node']
													else:
														scheList.insert(j,{'time':temp_time2, 'node':scheList[i-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode'], 'min':scheList[i-1]['min']})
														temp_max += 1
													temp_min=scheList[0]['node']
													j=0
													while (j<temp_max):
														if (temp_min>scheList[j]['node']):
															temp_min = scheList[j]['node']
														scheList[j]['min'] = temp_min
														j += 1
													self.backCollect.append(self.waitList_s[tempA])
													print "[Back] "+str(self.waitList_s[tempA]) + "  " + str(tempA)+"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
													self.jobStart(self.waitList_s[tempA],tempA,self.currentTime_s)
													tempA -= 1
												break
											i += 1
								if (self.jobList_s[self.waitList_s[tempA]]['state']==1 and checkedNum<self.BFMode ):
									# not back fill
									i = temp_point
									is_find = 0
									temp_pointB=temp_point
									temp_time2=0
									while (i < temp_max):
										if (is_find == 1):
											if (scheList[i-1]['min']<scheList[i]['min']):
												scheList[i]['min']=scheList[i-1]['min']
										else:
											if (self.jobList_s[self.waitList_s[tempA]]['reqNode']<=scheList[i]['node']):
												scheList[i]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
												temp_time2=self.jobList_s[self.waitList_s[tempA]]['reqTime']+scheList[i]['time']
												is_find = 1
												if (scheList[i]['node']<scheList[i]['min']):
													scheList[i]['min']= scheList[i]['node']
												else:
													break
											else:
												temp_point += 1
										i += 1
									i=temp_point+1
									temp_add=0
									while (i<temp_max):
										if (temp_time2<scheList[i]['time']):
											scheList.insert(i,{'time':temp_time2, 'node':scheList[i-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode'], 'min':scheList[i-1]['min']})
											temp_max += 1
											temp_add=1
											break
										elif (temp_time2==scheList[i]['time']):
											temp_add=1
											break
										else:
											scheList[i]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
										i += 1
									if (temp_add==0):
										scheList.append({'time':temp_time2, 'node':scheList[temp_max-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode'], 'min':scheList[temp_max-1]['min']})
										temp_max += 1
						checkedNum += 1
										
					else:
						if (self.jobList_s[self.waitList_s[tempA]]['state'] == 1 ):
							print "[start]  " + str(self.waitList_s[tempA])  + "  " + str(tempA)
							self.jobStart(self.waitList_s[tempA],tempA,self.currentTime_s)
							tempA -= 1
							self.winCount_s += 1
					tempA += 1
		
	def jobSubmit(self,jobIndex_t):
		#print waitList_s	
		self.waitList_s.append(jobIndex_t)
		self.waitNum_s+=1		
		self.prioCalcu()
		self.jobList_s[jobIndex_t]['state']=1
		self.jobIndex_s+=1
		print "[Submit]  "+str(jobIndex_t)#+"    "+str(self.waitList_s)
		self.collectActiveJob(jobIndex_t)
		self.jobList_s[jobIndex_t]['estStart'] = self.estimateStart(jobIndex_t)
		
		
	def jobStart(self,jobIndex_t2,waitIndex_t,startTime_t):				
		if (self.jobStartNum_s<self.jobNum_s):
			if (int(self.idleNode_s)>=int(self.jobList_s[jobIndex_t2]['reqNode'])):		
				print "   <start id "+str(self.jobList_s[jobIndex_t2]['id']) +"> "				
				self.runList_s.append(jobIndex_t2)
				self.jobList_s[jobIndex_t2]['state']=2
				self.jobList_s[jobIndex_t2]['start']=startTime_t
				self.jobList_s[jobIndex_t2]['end'] = startTime_t+self.jobList_s[jobIndex_t2]['run']
				
				self.waitList_s.pop(waitIndex_t)
				self.waitNum_s -= 1
				self.runNum_s += 1
				self.jobStartNum_s += 1
				self.allocateNode(jobIndex_t2)
				self.jobList_s[jobIndex_t2]['happy']=self.happyAnalysis(jobIndex_t2,startTime_t)
				print "  [idle: " +"  " + str(self.idleNode_s) +"]"
				#if (self.BFModeStr!='0' or self.winSize_s>1):
				self.forcast_start(jobIndex_t2)
		
	def jobFinish(self,jobIndex_t3,finishIndex_t,finishTime_t):
		j = 0
		self.runList_s.pop(finishIndex_t)
		self.runNum_s -= 1
		self.jobDoneNum_s += 1
		self.jobList_s [jobIndex_t3]['state'] = 3
		self.releaseNode(jobIndex_t3)	
		self.prioCalcu()
		print "[Finish]  " + str(jobIndex_t3) 
		self.collectJobInfo(jobIndex_t3)
		#if (self.BFModeStr!='0' or self.winSize_s>1):
		self.forcast_end(jobIndex_t3)
	
	def forcast_start(self, jobIndex_t7):
		i3=self.runNum_s-1
		temp_reqT=int(self.jobList_s [jobIndex_t7]['start'])+int(self.jobList_s [jobIndex_t7]['reqTime'])
		if (i3 == 0):
			self.forecast_s.append({'time':temp_reqT, 'index':jobIndex_t7, 'node':self.jobList_s[jobIndex_t7]['reqNode']})
		else:
			while (i3>0):
				if (self.forecast_s[i3-1]['time']<= temp_reqT):
					break
				i3 -= 1
			self.forecast_s.insert(i3,{'time':temp_reqT, 'index':jobIndex_t7, 'node':self.jobList_s[jobIndex_t7]['reqNode']})
		
	def forcast_end(self, jobIndex_t8):
		i3=0
		while (i3<self.runNum_s+1):
			if (self.forecast_s[i3]['index']== jobIndex_t8):
				self.forecast_s.pop(i3)
				break
			i3 += 1
		
	
	def collectActiveJob(self,jobIndex_t5):
		tempActList=[]
		k=0
		while(k<self.waitNum_s and self.waitList_s[k]!=jobIndex_t5):
			tempActList.append(self.waitList_s[k])
			k += 1
		k=0
		while(k<self.runNum_s):
			tempActList.append(self.runList_s[k])
			k += 1
		self.activeJobTrack_s.append({'index':jobIndex_t5, 'jobList':tempActList})
		
	def happyAnalysis(self,jobIndex_t6,currentTime):
		for job in self.activeJobTrack_s:
			if (job['index']==jobIndex_t6):
				if (len(job['jobList'])==0):
					if (self.jobList_s [jobIndex_t6]['submit'] == self.jobList_s [jobIndex_t6]['start'] ):
						self.happyNum += 1
						self.happyList.append(jobIndex_t6)
						print "[Happy]  "+ str(jobIndex_t6) 
						self.activeJobTrack_s.remove(job)
						return 0
					else:
						print "[Not Happy]  "+ str(jobIndex_t6) 
						self.activeJobTrack_s.remove(job)
						return -1
				
				temp_lastEnd=-1
				for preJob in job['jobList']:
					if (self.jobList_s [preJob]['state'] != 3):
						self.happyNum += 1
						self.happyList.append(jobIndex_t6)
						print "[Happy]  "+ str(jobIndex_t6) + " ("+str(preJob)+")"
						self.activeJobTrack_s.remove(job)
						return 0
					else:
						if (self.jobList_s [preJob]['end'] >= currentTime):
							self.happyNum += 1
							self.happyList.append(jobIndex_t6)
							print "[Happy]  "+ str(jobIndex_t6) + " ("+str(preJob)+")"
							self.activeJobTrack_s.remove(job)
							return 0
						
						if (temp_lastEnd<0 or temp_lastEnd<self.jobList_s [preJob]['end']):
							temp_lastEnd=self.jobList_s [preJob]['end']
				print "[Not Happy]  "+ str(jobIndex_t6)
				self.activeJobTrack_s.remove(job)
				return temp_lastEnd
		return -1
	
	def happyAnalysis2(self,jobIndex_t6,currentTime):
		if (self.jobList_s[jobIndex_t]['estStart']>=currentTime):
			self.happyNum2 += 1
			
		
	def estimateStart(self,jobIndex_t7):
		tempA=0
		temp_point=0
		temp_max=0
		scheList2=[]

		scheList2.append({'time':self.currentTime_s, 'node':self.idleNode_s})
		i = 0
		j = 0
		temp_max=1
		
		while (j < self.runNum_s):
			if (self.forecast_s[j]['time']!=scheList2[i]['time']):
				scheList2.append({'time':self.forecast_s[j]['time'], 'node':scheList2[i]['node']+self.forecast_s[j]['node']})
				i+= 1
				temp_max += 1
			else:
				scheList2[i]['node']=scheList2[i]['node']+self.forecast_s[j]['node']
			j+= 1
					
		while (tempA <self.waitNum_s):
			if (self.jobList_s[self.waitList_s[tempA]]['state']==1):
				i = temp_point
				temp_pointB=temp_point
				temp_time2=0
				while (i < temp_max):
					if (self.jobList_s[self.waitList_s[tempA]]['reqNode']<=scheList2[i]['node']):
						scheList2[i]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
						
						if (self.waitList_s[tempA]==jobIndex_t7):
							return scheList2[i]['time']
							
						temp_time2=self.jobList_s[self.waitList_s[tempA]]['reqTime']+scheList2[i]['time']
						break
					else:
						temp_point += 1
					i += 1
				i=temp_point+1
				temp_add=0
				while (i<temp_max):
					if (temp_time2<scheList2[i]['time']):
						scheList2.insert(i,{'time':temp_time2, 'node':scheList2[i-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode']})
						temp_max += 1
						temp_add=1
						break
					elif (temp_time2==scheList2[i]['time']):
						temp_add=1
						break
					else:
						scheList2[i]['node'] -= self.jobList_s[self.waitList_s[tempA]]['reqNode']
					i += 1
				if (temp_add==0):
					scheList2.append({'time':temp_time2, 'node':scheList2[temp_max-1]['node']+self.jobList_s[self.waitList_s[tempA]]['reqNode']})
					temp_max += 1
			tempA += 1
		return -1		
						
	
	# Node Using Method
	def allocateNode(self,jobIndex_t4):
		self.idleNode_s -= int(self.jobList_s[jobIndex_t4]['reqNode'])
	
	def releaseNode(self,jobIndex_t5):
		self.idleNode_s += int(self.jobList_s[jobIndex_t5]['reqNode'])

	# System Information Collection
	def collectJobInfo(self,jobIndex_t7):
		if (self.jobList_s [jobIndex_t7]['state'] == 3):
			temp_wait = self.jobList_s [jobIndex_t7]['start']-self.jobList_s [jobIndex_t7]['submit']
			temp_run = self.jobList_s [jobIndex_t7]['run']
			temp_resp = self.jobList_s [jobIndex_t7]['end']-self.jobList_s [jobIndex_t7]['submit']
			
			if (temp_run<10):
				temp_run = 10
			tempBSD = (temp_run+temp_wait)*1.0/temp_run 
			
			self.total_waitTime += temp_wait
			self.total_BSD += tempBSD
			self.total_respTime += temp_resp
			
			self.ave_waitTime = self.total_waitTime*1.0/self.jobDoneNum_s
			self.ave_BSD = self.total_BSD*1.0/self.jobDoneNum_s
			self.ave_respTime = self.total_respTime*1.0/self.jobDoneNum_s
	
	def collectSysUti(self):
		self.ave_uti=0
		temUti=0
		if self.nextEventTime_s>0 or self.jobDoneNum_s == self.jobNum_s:
			for item in self.systemUti:
				temUti +=(item['uti']*1.00/self.nodeNum_s)*item['inter']
			try:
				self.ave_uti=temUti*100.00/(self.currentTime_s-self.startTime_s)
			except:
				self.ave_uti=0
			tempDelta=0
			if (self.waitNum_s>0):
				tempDelta=1
			temp_size=0
			for waitJob in self.waitList_s:
				temp_size += self.jobList_s [waitJob]['reqNode']
			self.systemUti.append({'time':self.currentTime_s-self.startTime_s, 'inter':self.nextEventTime_s, 'uti':self.nodeNum_s-self.idleNode_s, 'delta':tempDelta, 'waitNum':self.waitNum_s, 'waitSize':temp_size})
			#self.systemUti.append({'time':1.0*(self.currentTime_s-self.startTime_s), 'inter':1.0*self.nextEventTime_s, 'uti':1.0*(self.nodeNum_s-self.idleNode_s), 'delta':1.0*tempDelta, 'waitNum':self.waitNum_s, 'waitSize':1.0*temp_size})
			self.pre_uti=self.nodeNum_s-self.idleNode_s
			
	# Result Output Method
	def exportResult(self,outputName,outputName2):
		f2=open(outputName,"w")
		f2.write("; jr_alg = '"+str(self.sysInfo_s['prioFunc'])+"'")
		f2.write("  \n")
		f2.write("; jr_bf = '"+str(self.sysInfo_s['BFModeStr'])+"'")
		f2.write("  \n")
		f2.write("; jr_winsize = "+str(self.sysInfo_s['winSize']))
		f2.write("  \n")
		f2.write("; jr_nodeNum = "+str(self.sysInfo_s['nodeNum']))
		f2.write("  \n")
		
		for jobResult_o in self.jobList_s:
			f2.write(str(jobResult_o['id']))
			f2.write("  \t")
			f2.write(str(jobResult_o['start']))
			f2.write("  \t")
			f2.write(str(jobResult_o['end']))
			f2.write("  \t")
			f2.write(str(jobResult_o['run']))
			f2.write("  \t")
			f2.write(str(jobResult_o['submit']))
			f2.write("  \t")
			f2.write(str(jobResult_o['reqTime']))
			f2.write("  \t")
			f2.write(str(jobResult_o['reqNode']))
			f2.write("  \t")
			f2.write(str(jobResult_o['user']))
			f2.write("  \t")
			f2.write(str(jobResult_o['group']))
			f2.write("  \t")
			f2.write(str(jobResult_o['state']))
			f2.write("  \t")
			f2.write(str(jobResult_o['happy']))
			f2.write("  \t")
			f2.write(str(jobResult_o['estStart']))
			f2.write("\n")
		f2.close()
		
		f2=open(outputName2,"w")
		f2.write("; jr_alg="+str(self.sysInfo_s['prioFunc']))
		f2.write("  \t")
		f2.write("; jr_bf="+str(self.sysInfo_s['BFModeStr']))
		f2.write("  \t")
		f2.write("; jr_winsize="+str(self.sysInfo_s['winSize']))
		f2.write("  \n")
		
		for utiResult_o in self.systemUti:
			f2.write(str(utiResult_o['time']))
			f2.write("  \t")
			f2.write(str(utiResult_o['inter']))
			f2.write("  \t")
			f2.write(str(utiResult_o['uti']))
			f2.write("  \t")
			f2.write(str(utiResult_o['delta']))
			f2.write("  \t")
			f2.write(str(utiResult_o['waitNum']))
			f2.write("  \t")
			f2.write(str(utiResult_o['waitSize']))
			f2.write("\n")
		f2.close()
		
	
	def getResult(self):
		return self.jobList_s
	
	def getHappyNum(self):
		return self.happyNum
		
	def getHappyNum2(self):
		return self.happyNum2
		
	def getSysUti(self):
		return self.systemUti	

	
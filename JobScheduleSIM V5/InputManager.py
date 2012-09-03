__metaclass__ = type
class InputManager:
	def init(self,readNum_in):
		self.jobList = []
		self.jobNum = 0
		self.nodeNum = 0
		self.winSize = 1
		self.subModify = 1
		self.prioFunc = "w"
		self.readNum = readNum_in
		self.sysInfo = {'jobNum':0, 'nodeNum':0, 'prioFunc':"w" ,'BFMode':0}
	
	# Data Input Method
	def nodeStrucIn(self,inNum):
		self.nodeNum = inNum
		self.sysInfo['nodeNum'] = self.nodeNum
		
	def setBackFilling(self,inBF):
		self.BFStr = inBF
		self.sysInfo['BFMode'] = self.BFStr
		
	def setWinSize(self,inWinSize):
		self.winSize = inWinSize
		self.sysInfo['winSize'] = self.winSize
	
	def setSubmitPara(self,inSubPara):
		self.subModify = inSubPara
		if (self.subModify<0):
			self.subModify = 1
		
	def SWFReader(self,fileNameIn):
		#try:
		self.SWFFileName = fileNameIn
		swfFile = open(fileNameIn,'r')
		j = 0
		temp_readNum=0
		while (temp_readNum<self.readNum or self.readNum==0):
			#print temp_readNum
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
				reqNodesB = ""
				userID = ""
				groupID = ""
				min_sub=-1
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
							submit=submit+ tempStr[i] 
						elif k == 3:
							runTime=runTime+ tempStr[i] 
						elif k == 5:
							reqNodesB=reqNodesB+ tempStr[i] 
						elif k == 7:
							reqNodes=reqNodes+ tempStr[i] 
						elif k == 8:
							reqTime=reqTime+ tempStr[i] 
						elif k == 11:
							userID=userID+ tempStr[i] 
						elif k == 12:
							groupID=groupID+ tempStr[i] 
							
				if (min_sub<0):
					min_sub=eval(submit)
				if (eval(reqNodes)<0):
					reqNodes=reqNodesB
				tempInfo = {'id':int(ID), 'submit':self.subModify*(float(submit)-min_sub)+min_sub, 'run':float(runTime), 'reqTime':float(reqTime), 'reqNode':float(reqNodes), 'user':int(userID), 'group':int(groupID), 'start':-1, 'end':-1, 'score':0, 'state':0, 'happy':-1, 'estStart':-1}
				# state: 0: not submit  1: waiting  2: running  3: done
					
				if (self.jobCheck(tempInfo)>=0):
					self.jobList.append(tempInfo)
					print str(temp_readNum)+"    "+str(tempInfo)
					temp_readNum+=1
				j = j + 1
			else:
				strNum = len(tempStr)
				tempStart = 0
				for i in range(strNum):
					if tempStr[i] != " " and tempStr[i] != ";":
						tempStart = i
						break
				if (tempStart+9<strNum):
					if (tempStr[tempStart:tempStart+8]=="MaxProcs"):
						print tempStr[tempStart:tempStart+8]
						tempProcs =""
						for j in range(strNum-tempStart-8):
							if tempStr[j+tempStart+8] != " " and tempStr[j+tempStart+8] != ":":
								tempProcs = tempProcs +  tempStr[j+tempStart+8] 
						print tempProcs
						self.nodeStrucIn(int(tempProcs))
			#self.jobList = tuple(self.jobList_t)
		swfFile.close()
		self.jobNum = len(self.jobList)
		self.sysInfo['jobNum'] = self.jobNum
		#except:
			#print "SWF File Error!"

	def scheAlgorithmIn(self,prioFuncIn):
		self.prioFunc = prioFuncIn
		self.sysInfo['prioFunc'] = self.prioFunc
	
	# Data Examineing Method
	def algorithmCheck(self):
		try:
			s = 1000
			t = 2000
			n = 30
			w = 4000
			m = 50
			z = 100
			l = 0.2
			result = eval(self.prioFunc)
			#print result
		except:
			return 0
		return 1
	
	def nodeCheck(self):
		if self.nodeNum>0:
			return 1
		else:
			return 0
	
	def jobCheck(self,jobInfo):
		if (int(jobInfo['run'])>int(jobInfo['reqTime'])):
			jobInfo['run']=jobInfo['reqTime']
			#return 2
			
		if (int(jobInfo['reqNode'])>int(self.nodeNum)):
			return -1
		
		if (int(jobInfo['id'])<=0):
			return -2
			
		if (int(jobInfo['submit'])<0):
			return -3
			
		if (int(jobInfo['run'])<=0):
			return -4
			
		if (int(jobInfo['reqTime'])<=0):
			return -5
			
		if (int(jobInfo['reqNode'])<=0):
			return -6
			
		return 1
	
	# Data Output Method
	def getJobNum(self):
		return self.jobNum
	
	def getNodeStruc(self):
		return self.nodeNum
	
	def getPrioFunc(self):
		return self.prioFunc
	
	def getSWFData(self):
		return self.jobList

	def getBFStr(self):
		return self.BFStr
		
	def getWinSize(self):
		return self.winSize

	def getSysInfo(self):
		return self.sysInfo
		

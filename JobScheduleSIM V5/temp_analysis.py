__metaclass__ = type
class ResultAnalysis:
	def init(self):
		self.jobList_All = []
		self.jobList = []
		self.jobNum =0
		self.SWFFileName=""
	
	def ResultReader(self,fileNameIn):
		self.SWFFileName = fileNameIn
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
				for i in range(strNum):
					if tempStr[i] == " " or tempStr[i] == "\t":
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
				tempInfo = {'id':int(ID), 'submit':int(submit), 'run':int(runTime), 'reqTime':int(reqTime), 'reqNode':int(reqNodes), 'user':int(userID), 'group':int(groupID), 'start':int(start), 'end':int(end), 'score':0, 'state':int(state)}
				# state: 0: not submit  1: waiting  2: running  3: done
				
				self.jobList.append(tempInfo)
				j = j + 1
		#self.jobList = tuple(self.jobList_t)
		swfFile.close()
		self.jobNum = len(self.jobList)
		self.jobList_All.append(self.jobList)
		self.jobList=[]
			
	def jobCheck(self):
		i=0
		while i<self.jobNum:
			tempResult=self.jobList_All[0][i]['start']-self.jobList_All[1][i]['start']
			if (self.jobList_All[1][i]['start']!=self.jobList_All[0][i]['start']):
				print "[ "+str(self.jobList_All[1][i]['id'])+"  "+str(i)+" ]  "+str(self.jobList_All[0][i]['start'])+"   "+str(self.jobList_All[1][i]['start'])+"   "+str(tempResult)
			i += 1
	
checkA=ResultAnalysis()
checkA.init()
checkA.ResultReader("JS_B1.rst")
checkA.ResultReader("JS_B1.rst2")
checkA.jobCheck()
print "OK"

checkA.init()
checkA.ResultReader("JS_B2.rst")
checkA.ResultReader("JS_B2.rst2")
checkA.jobCheck()
print "OK"

checkA.init()
checkA.ResultReader("JS_B3.rst")
checkA.ResultReader("JS_B3.rst2")
checkA.jobCheck()
print "OK"

checkA.init()
checkA.ResultReader("JS_B4.rst")
checkA.ResultReader("JS_B4.rst2")
checkA.jobCheck()
print "OK"

checkA.init()
checkA.ResultReader("JS_B5.rst")
checkA.ResultReader("JS_B5.rst2")
checkA.jobCheck()
print "OK"

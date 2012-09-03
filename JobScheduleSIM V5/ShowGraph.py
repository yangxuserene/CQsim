from matplotlib.ticker import FuncFormatter
from pylab import *

__metaclass__ = type
class ShowGraph:
	def init(self):
		self.colorPool=['darkred','blue','green','orange','purple']
		self.linePool=['--',' ',' ',' ',' ']
	
	def resetPara(self,labelNum_in,labels_in):
		self.labelNum_g=labelNum_in
		self.xlabels_g=tuple(labels_in)
		
	def graphA(self,figNum0,val,barColor,myTitle, saveGraph=None):
		import numpy as np
		import matplotlib.pyplot as plt
		myTitle+='\n\n\n'
		pos = arange(self.labelNum_g)+.5
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		ax = fig.add_subplot(111)
		ax.yaxis.grid(True)
		width = 0.5
		rects1 = ax.bar(pos,val, width,align='center',color=barColor)
		ax.set_title(myTitle)
		ax.set_xticks(pos)
		ax.set_xticklabels(self.xlabels_g)
		self.autolabel(rects1,ax)		
		if (saveGraph != None):
			plt.savefig(saveGraph+".png")
		
	def graphB(self,figNum0,val,totalNum_in,barColor,myTitle, saveGraph):
		import numpy as np
		import matplotlib.pyplot as plt
		myTitle+='\n\n\n'
		pos = arange(self.labelNum_g)+.5
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		ax = fig.add_subplot(111)
		ax.yaxis.grid(True)
		width = 0.5
		val2=[]
		for iterms in val:
			val2.append(iterms*100.0/totalNum_in)
		
		rects1 = ax.bar(pos,val2, width,align='center',color=barColor)
		ax.set_title(myTitle)
		ax.set_xticks(pos)
		ax.set_xticklabels(self.xlabels_g)
		formatter = FuncFormatter(self.percent)
		ax.yaxis.set_major_formatter(formatter)
		self.autolabel2(rects1,ax)
		if (saveGraph != None):
			plt.savefig(saveGraph+".png")
		
	def graphC(self,figNum0, timePoint_in, val, totalNum_in, min_start, max_end, partNum_in, myTitle, saveGraph=None):
		import numpy as np
		import matplotlib.pyplot as plt
		myTitle+='\n'
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		fig .subplots_adjust(bottom = 0.12)
		ax = fig.add_subplot(111) 
		ax.yaxis.grid(True)
		ax.plot(timePoint_in, val, color = "red")
		ax.set_title(myTitle)
		formatter = FuncFormatter(self.percent)
		ax.yaxis.set_major_formatter(formatter)
		ax.set_ylim(0, 110.0, color = "red")
		ax.set_xlim(min_start, max_end)
		if (partNum_in>len(val)):
			partNum_in=len(val)
		'''
		print  timePoint_in
		print  val
		'''
		time_total = max_end - min_start
		inteval = time_total / partNum_in
		timelist = []
		labels = []
		temptime = min_start
		for i in range(0, partNum_in+1):
			timelist.append(temptime)
			labels.append(str(temptime))
			temptime = temptime + inteval

		ax.set_xticks(timelist)
		ax.set_xticklabels(labels, rotation = 25, fontsize = 11)
		ax.set_xlabel('Time')
		if (saveGraph != None):
			plt.savefig(saveGraph+".png")
		
	def graphD(self,figNum0, timePoint_in, val, totalNum_in, min_start, max_end, partNum_in, myTitle, saveGraph=None):
		import numpy as np
		import matplotlib.pyplot as plt
		myTitle+='\n'
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		fig .subplots_adjust(bottom = 0.15)
		ax = fig.add_subplot(111) 
		ax.yaxis.grid(True)
		ax.plot(timePoint_in, val, color = "red")
		ax.set_title(myTitle)
		formatter = FuncFormatter(self.percent)
		ax.yaxis.set_major_formatter(formatter)
		ax.set_ylim(0, 110.0, color = "red")
		ax.set_xlim(min_start, max_end)
		if (partNum_in>len(val)):
			partNum_in=len(val)
		'''
		print  timePoint_in
		print  val
		'''
		time_total = int(max_end) - int(min_start)
		inteval = int(time_total) / partNum_in
		timelist = []
		labels = []
		temptime = int(min_start)
		temptime2= int(temptime)
		
		temp_y=0
		temp_w=0
		temp_d=0
		temp_h=0
		temp_m=0
		temp_s=0
		temp_op=60*60*24*7
		temp_op2=60*60*24*365
		
		for i in range(0, partNum_in+1):
			timelist.append(int(temptime))
			temptime2=int(temptime)
			temp_op=60*60*24*7
			
			temp_y=temptime2/temp_op2
			temptime2-=temp_y*temp_op2
			
			temp_w=temptime2/temp_op
			temptime2-=temp_w*temp_op
			temp_op=temp_op/7
			
			temp_d=temptime2/temp_op
			temptime2-=temp_d*temp_op
			temp_op=temp_op/24
			
			temp_h=temptime2/temp_op
			temptime2-=temp_h*temp_op
			temp_op=temp_op/60
			
			temp_m=temptime2/temp_op
			temptime2-=temp_m*temp_op
			
			temp_s=int(temptime2)
			
			labels.append(str(temp_y)+"y-"+str(temp_w)+"w-"+str(temp_d)+"d-"+str(temp_h)+"h-"+str(temp_m)+"m-"+str(temp_s)+"s")
			temptime = temptime + inteval

		ax.set_xticks(timelist)
		ax.set_xticklabels(labels, rotation = 25, fontsize = 10)
		ax.set_xlabel('Time')
		if (saveGraph != None):
			plt.savefig(saveGraph+".png")
		
		
	def graphE(self,figNum0, dataNum_in, timePoint_in, val, timeGroup, totalNum_in, min_start, max_end, partNum_in, myTitle, sepName_in, saveGraph=None,shadowX=None,shadowY=None, shadowMax=None, shadowName=None):
		import numpy as np
		import matplotlib.pyplot as plt
		myTitle+='\n\n\n'
		graphPara= []
		temp_shadowY=[]
		#graphPara={'xdata':[],'ydata':[],'linestyle':[],'color':[],}
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.75)
		fig .subplots_adjust(bottom = 0.15)
		fig .subplots_adjust(right = 0.88)
		ax = fig.add_subplot(111) 
		ax.yaxis.grid(True)
		
		if (shadowX!=None and shadowY!=None):
			ax2 = ax.twinx()
			'''
			print shadowX
			print shadowY
			print "======================="
			print shadowX[timeGroup[0]:timeGroup[1]]
			print shadowY[timeGroup[0]:timeGroup[1]]
			print "======================="
			print timeGroup
			print "======================="
			
			print "======================="
			'''
			temp_s_x=shadowX[timeGroup[0]:timeGroup[1]]
			temp_s_y=shadowY[timeGroup[0]:timeGroup[1]]
			ax2.fill(shadowX,shadowY,color='gray',alpha=0.4)
			temp_name=shadowName
			ax2.set_ylabel(temp_name,color="darkgray")
			tempNum = shadowMax*1.0/10.0
			if tempNum<1:
				tempNum=1
			ax2.set_ylim(0, shadowMax+tempNum)
			tempNum=shadowMax/5
			if tempNum<1:
				tempNum=1
			ax2.set_yticks([shadowMax,shadowMax*4/5,shadowMax*3/5,shadowMax*2/5,shadowMax*1/5,0])
			#for tl in ax2.get_yticklabels():
				#tl.set_color('darkgray')

		
		i = 0
		while i < dataNum_in:
			graphPara.append(timePoint_in[i][timeGroup[0]:timeGroup[1]])
			graphPara.append(val[i][timeGroup[0]:timeGroup[1]])
			#graphPara.append(self.linePool[i])
			graphPara.append(self.colorPool[i])
			
			i += 1
		ax.plot(*graphPara)
		ax.set_title(myTitle)
		formatter = FuncFormatter(self.percent)
		ax.yaxis.set_major_formatter(formatter)
		ax.set_ylim(0, 110.0, color = "red")
		ax.set_xlim(min_start, max_end)
		#print len(val)
		#print partNum_in
		#print val
		if (partNum_in>len(val[0][timeGroup[0]:timeGroup[1]])):
			partNum_in=len(val[0][timeGroup[0]:timeGroup[1]])
		
		time_total = int(max_end) - int(min_start)
		inteval = int(time_total) / partNum_in
		timelist = []
		labels = []
		temptime = int(min_start)
		temptime2= int(temptime)
		
		temp_y=0
		temp_w=0
		temp_d=0
		temp_h=0
		temp_m=0
		temp_s=0
		temp_op=60*60*24*7
		temp_op2=60*60*24*365
		
		for i in range(0, partNum_in+1):
			timelist.append(int(temptime))
			temptime2=int(temptime)
			temp_op=60*60*24*7
			
			temp_y=temptime2/temp_op2
			temptime2-=temp_y*temp_op2
			
			temp_w=temptime2/temp_op
			temptime2-=temp_w*temp_op
			temp_op=temp_op/7
			
			temp_d=temptime2/temp_op
			temptime2-=temp_d*temp_op
			temp_op=temp_op/24
			
			temp_h=temptime2/temp_op
			temptime2-=temp_h*temp_op
			temp_op=temp_op/60
			
			temp_m=temptime2/temp_op
			temptime2-=temp_m*temp_op
			
			temp_s=int(temptime2)
			
			labels.append(str(temp_y)+"y-"+str(temp_w)+"w-"+str(temp_d)+"d-"+str(temp_h)+"h-"+str(temp_m)+"m-"+str(temp_s)+"s")
			temptime = temptime + inteval

		ld = ax.legend(sepName_in,loc=9, bbox_to_anchor=[0.5, 1.13],ncol=4,prop={'size':10}) 
		ld.draw_frame(False)
		ax.set_xticks(timelist)
		ax.set_xticklabels(labels, rotation = 25, fontsize = 10)
		ax.set_xlabel('Time')
		if (saveGraph != None):
			plt.savefig(saveGraph+".png")
				
	def autolabel(self,rects,tar):
		# attach some text labels
		for rect in rects:
			height = rect.get_height()
			tar.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')
		
	def autolabel2(self,rects,tar):
		# attach some text labels
		for rect in rects:
			height = rect.get_height()
			tar.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height)+'%', ha='center', va='bottom')
		
	def percent(self,x2, pos2):
		return str(x2)+'%'
		
	def showPlt(self):
		import numpy as np
		import matplotlib.pyplot as plt
		plt.show()

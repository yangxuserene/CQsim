from matplotlib.ticker import FuncFormatter
from pylab import *

__metaclass__ = type
class ShowGraph:
	def init(self):
		import numpy as np
		import matplotlib.pyplot as plt
	
	def resetPara(self,labelNum_in,labels_in):
		self.labelNum_g=labelNum_in
		self.xlabels_g=tuple(labels_in)
		
	def graphA(self,figNum0,val,myTitle):
		myTitle+='\n\n\n'
		pos = arange(self.labelNum_g)+.5
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		ax = fig.add_subplot(111)
		ax.yaxis.grid(True)
		width = 0.5
		rects1 = ax.bar(pos,val, width,align='center',color='darkblue')
		ax.set_title(myTitle)
		ax.set_xticks(pos)
		ax.set_xticklabels(self.xlabels_g)
		self.autolabel(rects1,ax)
		
	def graphA(self,figNum0,val,barColor,myTitle):
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
		
	def graphB(self,figNum0,val,totalNum_in,barColor,myTitle):
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
		
	def graphC(self,figNum0, timePoint_in, val, totalNum_in, min_start, max_end, partNum_in, myTitle):
		myTitle+='\n'
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		fig .subplots_adjust(bottom = 0.12)
		ax = fig.add_subplot(111) 
		ax.yaxis.grid(True)
		ax.plot(timePoint_in, val, color = "red")
		ax.set_title(myTitle)
		ax.set_ylim(0, totalNum_in + totalNum_in*0.1, color = "red")
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
		
	def graphD(self,figNum0, timePoint_in, val, totalNum_in, min_start, max_end, partNum_in, myTitle):
		myTitle+='\n'
		fig = plt.figure(figNum0,facecolor='white')
		fig .subplots_adjust(top = 0.8)
		fig .subplots_adjust(bottom = 0.15)
		ax = fig.add_subplot(111) 
		ax.yaxis.grid(True)
		ax.plot(timePoint_in, val, color = "red")
		ax.set_title(myTitle)
		ax.set_ylim(0, totalNum_in + totalNum_in*0.1, color = "red")
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
		temptime2=temptime
		
		temp_y=0
		temp_w=0
		temp_d=0
		temp_h=0
		temp_m=0
		temp_s=0
		temp_op=60*60*24*7
		temp_op2=60*60*24*365
		
		for i in range(0, partNum_in+1):
			timelist.append(temptime)
			temptime2=temptime
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
			
			temp_s=temptime2
			
			labels.append(str(temp_y)+"y-"+str(temp_w)+"w-"+str(temp_d)+"d-"+str(temp_h)+"h-"+str(temp_m)+"m-"+str(temp_s)+"s")
			temptime = temptime + inteval

		ax.set_xticks(timelist)
		ax.set_xticklabels(labels, rotation = 25, fontsize = 10)
		ax.set_xlabel('Time')
		
	def showPlt(self):
		plt.show()
		
	def savePlt(self):
		plt.savefig("test_graph.png")
		
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

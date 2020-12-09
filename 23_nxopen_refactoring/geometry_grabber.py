import math
import NXOpen
import NXOpen.UF
import re
import os
import collections
import itertools
import threading
import multiprocessing
import time as tt
import sys

class namelessModule:
	def __init__(self):
		self.theSession = NXOpen.Session.GetSession()
		self.theUF = NXOpen.UF.UFSession.GetUFSession()
		self.thePDM = self.theSession.PdmSession
		self.workPart = self.theSession.Parts.Work
		self.displayPart = self.theSession.Parts.Display
		self.rtComp = self.workPart.ComponentAssembly.RootComponent 
		self.lw = self.theSession.ListingWindow
		self.bodies = [] #self.cycleObjects()
		self.fileCache = [] #self.getCacheFile()
		self.lw.Open()
	
	def writeCacheFile(self,body,values):
		with multiprocessing.Lock():
			with open(self.fileCache,'a') as cachedGeometry: 
				cachedGeometry.write('-------\n')
				# try:cachedGeometry.write('%s\n'%body.OwningComponent.Name)
				# except:cachedGeometry.write('%s\n'%body.OwningPart.Name)
				cachedGeometry.write('%s-%s\n'%(body,values))
				cachedGeometry.close()

	def getCacheFile(self):
		try:
			dirName = '%s\\teamcenter\\NX_DMCache' %os.environ['APPDATA']
			fileName = '%s\\teamcenter\\NX_DMCache\\cachedGeometry.txt' %os.environ['APPDATA']
			if os.path.isdir(dirName): pass
			else: os.mkdir(dirName)
			if os.path.isfile(fileName):
				self.fileCache = fileName 
				#return fileName 
			else: 
				with open(fileName,'a') as cache: 
					cache.close()
				self.fileCache = fileName
				#return fileName
		except Exception as ex:
			#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'getCacheFile failed with %s' %ex)
			raise ex
		pass

	def grabGeometry(self,bodies,vertices = [],points = []):
		with multiprocessing.Lock():
			for body in bodies:
				edges = []
				[edges.append(edge) for edge in body.GetEdges()]
				vertices = []
				for edge in edges:
					[vertices.append(vert) for vert in edge.GetVertices()]
				points = []
				for point in vertices:
					points.append((point.X,point.Y,point.Z))
				#self.writeCacheFile(body,points)

	def chunkIt(self,num,out = [],last = 0.0):
		avg = len(self.bodies) / float(num)
		while last < len(self.bodies):
			out.append(self.bodies[int(last):int(last + avg)])
			last += avg
		return out

	def cycleObjects(self,bodies = [], tmpBodyTag = 0):
		while True:
			tmpBodyTag = self.theUF.Obj.CycleObjsInPart(self.workPart.Tag, NXOpen.UF.UFConstants.UF_solid_type ,tmpBodyTag)
			if tmpBodyTag == 0: break 
			else:
				theType, theSubType = self.theUF.Obj.AskTypeAndSubtype(tmpBodyTag)
				if theSubType == NXOpen.UF.UFConstants.UF_solid_body_subtype:
					bodies.append(NXOpen.TaggedObjectManager.GetTaggedObject(tmpBodyTag))
		self.bodies = bodies
		#return bodies

def main(num = 4):
	app = namelessModule()
	app.cycleObjects()
	app.getCacheFile()
	chunks = app.chunkIt(num)
	#multithreading section
	if len(app.bodies)>1:
		vts = []
		pts = []
		threadList = []
		time1 = tt.time()
		for index in range(num):
			set_ = chunks[index]
			vts.insert(index,[])
			pts.insert(index,[])
			threadList.insert(index,threading.Thread(target = app.grabGeometry, args = (set_,vts[index],pts[index])))
			threadList[index].start()
		for thread in threadList:
			thread.join()
		time2 = tt.time() - time1
	#single thread section
	elif len(app.bodies) == 1: 
		time1 = tt.time()
		v1,p1 = [],[]
		t1 = threading.Thread(target = app.grabGeometry, args = (app.bodies,v1,p1))
		t1.start()
		t1.join()
		time2 = tt.time() - time2
	else: pass 
	#report section
	app.lw.WriteLine(str(len(app.bodies)))
	app.lw.WriteLine(str(time2))
	app.lw.WriteLine('Completed')
	return None
	
if __name__ == '__main__':
	main()

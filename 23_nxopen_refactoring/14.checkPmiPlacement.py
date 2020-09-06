from math import *
import NXOpen
import NXOpen.UF
import re

def detectBorders(segmentPoles,lw):
	polesX = []
	polesY = []
	polesZ = []
	result = {}
	
	kostil = [polesX.append(pole.X) for pole in segmentPoles]
	kostil = [polesY.append(pole.Y) for pole in segmentPoles]
	kostil = [polesZ.append(pole.Z) for pole in segmentPoles]
	
	sortFunction = [item.sort() for item in (polesX,polesY,polesZ)]
	
	result['minX'] = polesX[0]
	result['maxX'] = polesX[-1]
	result['minY'] = polesY[0]
	result['maxY'] = polesY[-1]
	result['minZ'] = polesZ[0]
	result['maxZ'] = polesZ[-1]
	
	#fn = [lw.WriteLine('%s -- %s'%(key,result[key])) for key in result]
	
	'''
	for i, pole in enumerate(segmentPoles):
		if i == 0:
			coordX = [pole.X,pole.X] #[minValue,maxvalue]
			coordY = [pole.Y,pole.Y] #[minValue,maxvalue]
			coordZ = [pole.Z,pole.Z] #[minValue,maxvalue]
		else:
				coordX[0] = pole.X if coordX[0]>pole.X else pass
				coordX[1] = pole.X if coordX[0]<pole.X else pass
				coordY[0] = pole.Y if coordX[0]>pole.Y else pass
				coordY[1] = pole.Y if coordX[0]<pole.Y else pass
				coordZ[0] = pole.Z if coordX[0]>pole.Z else pass
				coordZ[1] = pole.Z if coordX[0]<pole.Z else pass
	
	#господа бога ради перепиши потом на нормальный поиск краевых значений, а не вот это вот все
	#это ужасно
	'''
	return result

def pointCoordDiff(p1,p2):
	return (abs(p1)-abs(p2)) < 200
	
def detectNotePlacement(borders,noteOrigin):
	flag = ''
	if noteOrigin.X < borders['maxX']:
		flag += 'за рамками X: minx %s maxx %s planex %s' %(borders['minX'],borders['maxX'],noteOrigin.X)#test
	elif pointCoordDiff(noteOrigin.Y,borders['minY']) or pointCoordDiff(noteOrigin.Y,borders['maxY']):   #test
		flag += 'за рамками Y: miny %s maxy %s planey %s' %(borders['minY'],borders['maxY'],noteOrigin.Y)#test
	elif pointCoordDiff(noteOrigin.Z,borders['minZ']) or pointCoordDiff(noteOrigin.Z,borders['maxZ'])::  #test
		flag += 'за рамками Z: minz %s maxz %s planez %s' %(borders['minZ'],borders['maxZ'],noteOrigin.Z)#test
	else:
		pass
	return flag
	
	#work###############if noteOrigin.X < borders['maxX']:
	#work###############	flag += 'за рамками X: minx %s maxx %s planex %s' %(borders['minX'],borders['maxX'],noteOrigin.X)
	#work###############elif noteOrigin.Y < borders['minY'] or noteOrigin.Y > borders['maxY']:
	#work###############	flag += 'за рамками Y: miny %s maxy %s planey %s' %(borders['minY'],borders['maxY'],noteOrigin.Y)
	#work###############elif noteOrigin.Z < borders['minZ'] or noteOrigin.Z > borders['maxZ']:
	#work###############	flag += 'за рамками Z: minz %s maxz %s planez %s' %(borders['minZ'],borders['maxZ'],noteOrigin.Z)
	#work###############else:
	#work###############	pass
	#work###############return flag
	
def pointDistance(pCoord):
	return sqrt(pow(pCoord.X,2) + pow(pCoord.Y,2) + pow(pCoord.Z,2))
	
def main() :
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	lw = theSession.ListingWindow
	#viewsSTD_lib = ['Top', 'Front', 'Right',
	#					'Back', 'Bottom', 'Left', 
	#					'Isometric', 'Trimetric'] #sys prop of who was creator of view
	#viewsEXT = []
	lw.Open()
	#for item in workPart.ModelingViews:
	#	if not(item.Name in viewsSTD_lib):
	#		viewsEXT.append(item.Name)
	#	else:
	#		pass
	orientNote = {}
	orientView = []
	modelPoles = [] #узлы жг если быть точным
	pointCollection = workPart.Points
	splineCollection = workPart.Splines
	borderPoles =[]
	lw.WriteLine('-------------------')
	#fn = [lw.WriteLine('%s -- %s -- distance %s'%(point.JournalIdentifier,point.Coordinates,pointDistance(point.Coordinates))) for point in workPart.Points]
	lw.WriteLine('-------------------')

	for note in workPart.Notes:
		for view in note.GetViews():
			lw.WriteLine(str(view.Name))
			#lw.WriteLine('note origin: %s -- distance to note %s' %(note.AnnotationOrigin,pointDistance(note.AnnotationOrigin)))
			np = note.AnnotationPlane
			#lw.WriteLine('%s' %np.Origin)
			for splineSegment in splineCollection:
				[modelPoles.append(pole) for pole in splineSegment.GetPoles()]
			borderPoles = detectBorders(modelPoles,lw)
			lw.WriteLine('%s' %(detectNotePlacement(borderPoles,note.AnnotationOrigin)))
			
				#lw.WriteLine('spline: %s -- %s' %(splineSegment.JournalIdentifier,splineSegment))
				#[lw.WriteLine('pole: %s -- distance: %s' %(pole, pointDistance(pole))) for pole in splineSegment.GetPoles()] #get coordinates of knot-points and disabled fracture-point
			
			#############check visibility of Notes
			#orientationNote = note.AnnotationPlane.Orientation
			#orientationView = view.Matrix #если ориентация ТТ и вида не совпадают в пределах допуска , то считаю ТТ неверной сориентированной. Оценка допуска - х
			#lw.WriteLine('xx %s note----view %s delta(%s)' %(orientationNote.Xx,orientationView.Xx,abs(orientationNote.Xx)-abs(orientationView.Xx)))	 
			#lw.WriteLine('xy %s note----view %s delta(%s)' %(orientationNote.Xy,orientationView.Xy,abs(orientationNote.Xy)-abs(orientationView.Xy)))	 
			#lw.WriteLine('xz %s note----view %s delta(%s)' %(orientationNote.Xz,orientationView.Xz,abs(orientationNote.Xz)-abs(orientationView.Xz)))	 
			#lw.WriteLine('yx %s note----view %s delta(%s)' %(orientationNote.Yx,orientationView.Yx,abs(orientationNote.Yx)-abs(orientationView.Yx)))	 
			#lw.WriteLine('yy %s note----view %s delta(%s)' %(orientationNote.Yy,orientationView.Yy,abs(orientationNote.Yy)-abs(orientationView.Yy)))	 
			#lw.WriteLine('yz %s note----view %s delta(%s)' %(orientationNote.Yz,orientationView.Yz,abs(orientationNote.Yz)-abs(orientationView.Yz)))	 
			#lw.WriteLine('zx %s note----view %s delta(%s)' %(orientationNote.Zx,orientationView.Zx,abs(orientationNote.Zx)-abs(orientationView.Zx)))	 
			#lw.WriteLine('zy %s note----view %s delta(%s)' %(orientationNote.Zy,orientationView.Zy,abs(orientationNote.Zy)-abs(orientationView.Zy)))	 
			#lw.WriteLine('zz %s note----view %s delta(%s)' %(orientationNote.Zz,orientationView.Zz,abs(orientationNote.Zz)-abs(orientationView.Zz)))
			#########
			
			at = workPart.Annotations.CreateAssociativeText()
			cd = workPart.Annotations.CreateComponentData(note)
						
			#techReqProps = {'Вид расположения ТТ' : view.Name,
			#				'ИД ТТ' : note.JournalIdentifier,
			#				'Расположение ТТ' : note.AnnotationOrigin,
			#				'Плоскость ТТ' : note.AnnotationPlane.Origin,
			#				'Ориентация ТТ' : note.AnnotationPlane.Orientation,
			#				'Цвет шрифта ТТ' : note.Color,
			#				'Шрифт ТТ' : note.LineFont,
			#				'Толщина линии ТТ' : note.LineWidth}
				
			#noteBuilder = workPart.Annotations.CreatePmiNoteBuilder(note)
			
			#fn = [lw.WriteLine('%s -- %s'%(key,val)) for key,val in techReqProps.items()]
			#for tc in cd.GetTextComponents():
			#	for line in tc.GetText():
			#		lw.WriteLine('%s'%(at.GetEvaluatedText(note, line)))
			lw.WriteLine('--------------------------------')			
if __name__ == '__main__':
	main()

'''
import math
import NXOpen
import NXOpen.Annotations
import NXOpen.Drawings
def main() : 

	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	viewsSTD_lib = ['Top', 'Front', 'Right', 'Back', 'Bottom', 'Left', 'Isometric', 'Trimetric'] #sys prop of who was creator of view
	viewsEXT = []
	lw = theSession.ListingWindow
	lw.Open()
	
	for item in workPart.ModelingViews:
		if not(item.Name in viewsSTD_lib):
			viewsEXT.append(item.Name)
		else:
			pass
	func = [lw.WriteLine(str(type(item))) for item in workPart.Notes]
	func = [lw.WriteLine(str(type(item))) for item in workPart.Labels]
	
	lw.WriteLine(str(type(pmiNote1)))
	lw.WriteLine(str(pmiNote1.GetText()))
	func = [lw.WriteLine(item.Name) for item in pmiNote1.GetViews()]
	
	
if __name__ == '__main__':
	main()
'''

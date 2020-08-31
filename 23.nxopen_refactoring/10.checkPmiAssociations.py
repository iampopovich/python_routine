import NXOpen
import NXOpen.UF
import NXOpen.Assemblies
import time as tt
import datetime as dt

def main():
	theSession  = NXOpen.Session.GetSession()
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work #<class 'NXOpen.Part'>
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	tStart = dt.datetime.now()
	lw.WriteLine(findRetainedPMI(workPart))
	lw.WriteLine(findEmptyPMI(workPart))
	lw.WriteLine('%s' %(dt.datetime.now() - tStart))

def findRetainedPMI(workPart):
	try:
		frp_string = ''
		frp_pmiCollection = workPart.PmiManager.Pmis
		associativeText = workPart.Annotations.CreateAssociativeText()
		frp_retainedList = []
		for pmiItem in frp_pmiCollection:
			frp_pmiItemGdi = pmiItem.GetDisplayInstances()[0]
			frp_PMIMatrix = [
								round(frp_pmiItemGdi.AnnotationOrigin.X),
								round(frp_pmiItemGdi.AnnotationOrigin.Y),
								round(frp_pmiItemGdi.AnnotationOrigin.Z)
							]
			if frp_pmiItemGdi.IsRetained:
					frp_retainedList.append(frp_PMIMatrix)
		if len(frp_retainedList) == 0: frp_string = 'PMI связи не нарушены\n'
		elif len(frp_retainedList) == 1: frp_string = 'Ассоциативная связь нарушена в точке \n%s' %('\n'.join(map(str,frp_retainedList)))
		else: frp_string = 'Ассоциативная связь нарушена в точках \n%s' %('\n'.join(map(str,frp_retainedList)))
		return frp_string
	except Exception as ex:
		return('findRetainedPMI failed with %s' %ex)
	

def findEmptyPMI(workPart):
	try:
		fep_string = ''
		fep_pmiCollection = workPart.PmiManager.Pmis
		associativeText = workPart.Annotations.CreateAssociativeText()
		fep_emptyList = []
		for pmiItem in fep_pmiCollection:
			fep_pmiItemGdi = pmiItem.GetDisplayInstances()[0]
			fep_PMIMatrix = [
								round(fep_pmiItemGdi.AnnotationOrigin.X),
								round(fep_pmiItemGdi.AnnotationOrigin.Y),
								round(fep_pmiItemGdi.AnnotationOrigin.Z)
							]
			if isinstance(fep_pmiItemGdi, NXOpen.Annotations.BalloonNote):
				pmiBuilder = workPart.Annotations.CreateBalloonNoteBuilder(fep_pmiItemGdi)
			elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.PmiLineWeld):
				pmiBuilder = workPart.Annotations.Welds.CreatePmiLineWeldBuilder(fep_pmiItemGdi)	
				continue #заглушка
			elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.SurfaceFinish):
				pmiBuilder = workPart.PmiManager.PmiAttributes.CreateSurfaceFinishBuilder(fep_pmiItemGdi)
				continue #заглушка
			elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.PmiCustomSymbol):
				pmiBuilder = workPart.Annotations.CreatePmiCustomSymbolBuilder(fep_pmiItemGdi)
			else: pmiBuilder = workPart.Annotations.CreatePmiNoteBuilder(fep_pmiItemGdi)
			try:	
				text = ''.join(map(str,pmiBuilder.Text.GetEditorText()))
				fep_pmiText = associativeText.GetEvaluatedText(fep_pmiItemGdi,text)
				#fep_pmiText = ''.join(map(str,fep_pmiItemGdi.GetText()))
				if len(fep_pmiText) == 0:
					fep_emptyList.append(fep_PMIMatrix)
			except Exception as ex: 
				lw.WriteLine('%s' %ex)
				continue
		if len(fep_emptyList) == 0: fep_string = 'Все аннотации подписаны\n'
		elif len(fep_emptyList) == 1: fep_string = 'Отсутствует текст в точке \n%s' %('\n'.join(map(str,fep_emptyList)))
		else: fep_string = 'Отсутствует текст в точках \n%s' %('\n'.join(map(str,fep_emptyList)))
		return fep_string
	except Exception as ex:
		return ('findEmptyPMI failed with %s' %ex)
	'''
	HANDLE R-26099916 -- ['2470.A1-J8'] -- [6929, -691, 1209]
	HANDLE R-26146648 -- ['B.9100.XB11'] -- [10672, 1608, -1269]
	0:00:06.685800
	===============
	HANDLE R-26099916 -- ['2470.A1-J8'] -- [6929, -691, 1209]
	HANDLE R-26146648 -- ['B.9100.XB11'] -- [10672, 1608, -1269]
	0:00:00.015600
	############technical requaries
	NXOpen.Annotations.PmiCenterMark
	NXOpen.Annotations.PmiDiameterDimension
	NXOpen.Annotations.PmiNote
	NXOpen.Annotations.PmiHorizontalDimension
	NXOpen.Annotations.Region
	NXOpen.Annotations.Fcf
	NXOpen.Annotations.PointTarget
	NXOpen.Annotations.PmiCenterline3d
	NXOpen.Annotations.PmiPerpendicularDimension
	NXOpen.Annotations.BalloonNote
	NXOpen.Annotations.PmiLineWeld
	NXOpen.Annotations.SurfaceFinish
	NXOpen.Annotations.Datum
	NXOpen.Annotations.PmiMinorAngularDimension
	NXOpen.Annotations.PmiConcentricCircleDimension
	NXOpen.Annotations.PmiOrdinateOriginDimension
	NXOpen.Annotations.PmiVerticalOrdinateDimension
	NXOpen.Annotations.PmiChamferDimension
	NXOpen.Annotations.PmiLabel
	NXOpen.Annotations.CustomSymbol
	
	'''

if __name__ == '__main__':
	main()

from math import *
import NXOpen
import NXOpen.UF
import re
#очень плохо
#https://docs.plm.automation.siemens.com/data_services/resources/nx/10/nx_api/en_US/custom/nxopen_python_ref/NXOpen.Annotations.ArrowheadType.html?highlight=arrowheadtype%20enumeration

def checkPointDistance(pCoord):
	try:
		return sqrt(pow(pCoord.X,2) + pow(pCoord.Y,2) + pow(pCoord.Z,2))
	except Exception as ex:
		return('checkPointDistance failed with %s' %ex)

def main() :
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	checkAnnotationsStyle(workPart)

def checkAnnotationsStyle(workPart):
	try:
		cas_pmiCollection = workPart.PmiManager.Pmis
		associativeText = workPart.Annotations.CreateAssociativeText()
		cas_pmiListAlarm = []
		for pmiItem in cas_pmiCollection:
			cas_pmiItemGdi = GetDisplayInstances()[0]
			if  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiCenterMark): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiDiameterDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiNote): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiHorizontalDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.Region): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.Fcf): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PointTarget): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiCenterline3d): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiPerpendicularDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.BalloonNote): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiLineWeld): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.SurfaceFinish): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.Datum): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiMinorAngularDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiConcentricCircleDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiOrdinateOriginDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiVerticalOrdinateDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiChamferDimension): continue
			elif  isinstance(cas_pmiItemGdi ,NXOpen.Annotations.PmiLabel): #выноски с полкой, ТУ
				cas_pmiBuilder = workPart.Annotations.CreatePmiNoteBuilder(cas_pmiItemGdi)
				cas_pmiLetteringStyle = cas_pmiBuilder.Style.LetteringStyle
				cas_associatedObject = cas_pmiItemGdi.GetAssociatedObject()
				cas_pmiPrefs = cas_pmiItemGdi.GetLineAndArrowPreferences()
				text = ''.join(map(str,cas_pmiBuilder.Text.GetEditorText()))
				cas_pmiText = associativeText.GetEvaluatedText(cas_pmiItemGdi,text)
				if NXOpen.Annotations.ArrowheadType.FilledDot != pmiPrefs.FirstArrowType:
					cas_pmiListAlarm.append('Несоответствущий тип 1 стрелки выноски %s'%(cas_pmiText)) 
				elif NXOpen.Annotations.ArrowheadType.FilledDot != pmiPrefs.SecondArrowType:
					cas_pmiListAlarm.append('Несоответствущий тип 2 стрелки выноски %s'%(cas_pmiText))
				elif pmiLetteringStyle.GeneralTextFont != 1:
					cas_pmiListAlarm.append('Текст замечания %s не кириллический' %(cas_pmiText))  
				else: pass
				#lw.WriteLine('Color %s :%s' %(pmi_labelText,pmiLetteringStyle.GeneralTextColor.Label))
			elif cas_pmiItemGdi == NXOpen.Annotations.CustomSymbol: pass#как правило - клеймение
	except Exception as ex:
		return('checkAnnotationsStyle failed with %s' %ex)
		
'''
			#lw.WriteLine('%s' %associativeText.GetEvaluatedText(label,str(pmiBuilder.Text.GetEditorText())))
			lw.WriteLine('%s' %associatedObject.GetObjects())
			#lw.WriteLine('AnnotationOrigin:%s' %label.AnnotationOrigin)
			lw.WriteLine('Color:%s' %label.Color)
			lw.WriteLine('Layer:%s' %label.Layer)
			lw.WriteLine('LineWidth:%s' %label.LineWidth)
			lw.WriteLine('LineFont:%s' %label.LineFont)
			#lw.WriteLine('NumberOfAssociativities):%s' %label.NumberOfAssociativities)
			#lw.WriteLine('Tag:%s' %label.Tag)
'''
			

if __name__ == '__main__':
	main()


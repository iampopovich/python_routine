import NXOpen
import NXOpen.UF
import NXOpen.Assemblies
import math
import time as tt
import datetime as dt

def main():
	theSession = NXOpen.Session.GetSession()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	theUI = NXOpen.UI.GetUI()
	workPart = theSession.Parts.Work
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	try:
		rtComp = workPart.ComponentAssembly.RootComponent
		if (rtComp != 0): lw.WriteLine('%s' %checkWeightStatement(rtComp,theUF))
		else: pass
	except Exception as e:
		lw.WriteLine('main failed with %s' %e)

	
def checkWeightStatement(component,theUF):
	try: #для сб достаточно проверить только первый рут компонент
		cws_string = ''
		workPart = component.OwningPart
		cws_componentObjects = []
		cws_componentObjects.append(component)
		reportComponentChildren(component,cws_componentObjects)
		cws_list = []
		for item in cws_componentObjects:
			cws_massProps = theUF.Weight.AskProps(item.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM)
			if cws_massProps.CacheState == NXOpen.UF.Weight.StateType.CACHED: 
				cws_list.append('Состояние массы %s: Расчет массы актуальный' %item.Name)
			elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.NO_CACHE:
				cws_list.append('Состояние массы %s: Расчет массы не актуальный' %item.Name)
			elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.ASSERTED:
				cws_list.append('Состояние массы %s: Масса назначена вручную' %item.Name)
			elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.IMPLIED: pass
			elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.INHERITED: pass 
			elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.UNKNOWN: pass
		cws_string = '\n'.join(cws_list)
		return cws_string
	except Exception as ex:
		return('checkWeightStatement failed with %s' %ex) 
	
	
def reportComponentChildren(rcc_comp,rcc_compList):
	try: rcc_componentChildren = rcc_comp.GetChildren()
	except: return rcc_compList
	if len(rcc_componentChildren) != 0:
		for item in rcc_componentChildren:
			try:
				if item.IsSuppressed: rcc_compList.append(item)#pass
				elif len(item.GetChildren()) != 0:
					rcc_compList.append(item)
					reportComponentChildren(item,rcc_compList)
				else: rcc_compList.append(item)
			except Exception as ex:
				return ('reportComponentChildren failed with %s ' %ex)#debug output
		return rcc_compList	
	else: return rcc_compList
	
if __name__ == '__main__':
	main()

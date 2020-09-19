import NXOpen
import NXOpen.Assemblies
import NXOpen.UF
import math
########original code here http://nxjournaling.com/content/creating-subroutine-process-all-components-assembly
def main():
	theSession = NXOpen.Session.GetSession()
	theUF = NXOpen.UI.GetUI()
	theUI = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	try:
		rtComp = workPart.ComponentAssembly.RootComponent
		if rtComp != 0:
			lw.WriteLine(checkSuppressedObjects(theSession,rtComp))
		else: pass
	except Exception as ex:
		lw.WriteLine('Failed with %s' %ex)
		
def checkSuppressedObjects(theSession,component, compObjcts = None):
	cso_componentObjects = [] #рутина - выполнить один раз для сборок и передавать в качестве листа компонентов.
	cso_list = []
	workPart = component.OwningPart
	cso_componentObjects.append(component)
	reportComponentChildren(component,cso_componentObjects)
	try:
		for item in cso_componentObjects:
			if item.IsSuppressed:
				cso_attributesList = []
				[cso_attributesList.append(item.Title) for item in item.GetAttributeTitlesByType(NXOpen.NXObjectAttributeType.String)]
				if 'REFERENCE_COMPONENT' in cso_attributesList:	continue
				else:
					parent = item.Parent
					cso_list.append('%s (%s)' %(item.DisplayName, parent.DisplayName))
					continue
			else: pass
		cso_list = set(cso_list)
		if len(cso_list) == 0: cso_string = 'ЭМ не содержит подавленные объекты'
		if len(cso_list) == 1: cso_string = 'ЭМ содержит подавленный объект %s' %('\n'.join(map(str,cso_list)))
		elif len(cso_list) > 1:	cso_string = 'ЭМ содержит подавленные объекты:\n%s' %('\n'.join(map(str,cso_list)))
		else: pass
		return cso_string
	except Exception as ex:
		return ('checkSuppressedObjects failed with: %s' %ex)
	
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


import NXOpen
import NXOpen.UF


def main():
	theSession = NXOpen.Session.GetSession()
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine(checkUnparameterizedBodies(workPart))

def checkUnparameterizedBodies(workPart):
	cub_list = []
	#cub_list = [feature.Name if feature.FeatureType == NXOpen.Features.Brep for feature in workPart.Features  ]
	if len(workPart.Features.GetFeatures()) != 0:
		for feature in workPart.Features:
			if isinstance(feature,NXOpen.Features.Brep):
				cub_list.append('%s - %s' %(feature.Name, feature.JournalIdentifier))
		if len(cub_list) == 0: cub_string = 'ЭМ не содержит непараметризованных тел'
		elif len(cub_list) == 1: cub_string = 'ЭМ содержит непараметризованное тело: %s' %('\n'.join(map(str,cub_list)))
		elif len(cub_list) > 1: cub_string = "ЭМ содержит непараметризованные тела:\n%s" %('\n'.join(map(str,cub_list)))
		else: pass
	else: cub_string = 'ЭМ не содержит непараметризованных тел' 
	return (cub_string)

if __name__ == '__main__':
	main()

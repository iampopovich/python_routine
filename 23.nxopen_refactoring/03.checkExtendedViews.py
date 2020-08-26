import math
import NXOpen
import NXOpen.UF


def main() :
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine('%s' %checkExtendedViews(workPart))

def checkExtendedViews(workPart):
	try:
		vs_STD_lib = ['Top','Front','Right',
						'Back','Bottom','Left',
						'Isometric','Trimetric'] #sys prop of who was creator of view
		vs_listSTD = []
		vs_listEXT = []
		for item in workPart.ModelingViews:
			if item.Name in vs_STD_lib:
				vs_listSTD.append(item.Name)
			else:
				vs_listEXT.append(item.Name)
		#rewrite output info , combine it into one row vs_string
		if len(vs_listEXT) == 0: vs_string = 'ЭМ не содержит доп. виды'
		if len(vs_listEXT) == 1: vs_string = 'ЭМ содержит доп. вид %s' %('\n'.join(map(str,vs_listEXT)))
		elif len(vs_listEXT) > 1: vs_string = "ЭМ содержит доп. виды:\n%s" %('\n'.join(map(str,vs_listEXT)))
		return vs_string
	except Exception as ex:
		return ('checkExtendedViews failed with %s' %ex)

if __name__ == '__main__':
	main()


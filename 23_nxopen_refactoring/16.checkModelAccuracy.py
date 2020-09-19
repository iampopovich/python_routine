import math
import NXOpen
import datetime as dt

def main() :
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine('%s' %checkModelAccuracy(workPart))

def checkModelAccuracy(workPart):
	try:
		cma_dist = workPart.Preferences.Modeling.DistanceToleranceData
		cma_angle = workPart.Preferences.Modeling.AngleToleranceData
		cma_dict = {'Линейный допуск ЭМ': cma_dist,'Угловой допуск ЭМ': cma_angle}
		cma_string = '\n'.join(['%s: %s' %(key,cma_dict[key]) for key in cma_dict])
		return cma_string
	except Exception as ex:
		return ('checkModelAccuracy failed with %s' %ex)
		
if __name__ == '__main__':
	main()

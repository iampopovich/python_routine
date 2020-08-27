import math
import NXOpen

def main() :

	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine(findPMIs(workPart))

def findPMIs(workPart):
	try:
		if len(list(workPart.PmiManager.Pmis))!=0:
			fp_pmiList = [item.JournalIdentifier for item in workPart.PmiManager.Pmis]
			fp_string = 'Модель содержит объекты PMI \n%s' %('\n'.join(map(str,fp_pmiList)))
		else: fp_string = 'Модель соответствует требованиям'
		return(fp_string)
	except Exception as ex:
		return('findPMIs failed with %s' %ex)

if __name__ == '__main__':
	main()

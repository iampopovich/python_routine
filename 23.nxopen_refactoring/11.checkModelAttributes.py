import NXOpen
import NXOpen.UI
import NXOpen.Assemblies
import math
import re

def main():
	theSession = NXOpen.Session.GetSession()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine(checkModeAttributes(workPart))


def checkModelAttributes(workPart):
	cma_attribList = []
	[cma_attribList.append(item.Title) for item in item.GetAttributeTitlesByType(NXOpen.NXObjectAttributeType.String)]
	if "REFERENCE_COMPONENT" in cma_attribList:
		continue
	else:
		parent = item.Parent
		cam_list.append('%s (%s)' %(item.DisplayName, parent.DisplayName))
					continue
			else: pass
		cam_list = set(cam_list)
		if len(cam_list) == 0: su_string = ''
		if len(cam_list) == 1: su_string = ' %s' %('\n'.join(map(str,cam_list)))
		elif len(cam_list) > 1:	su_string = '\n%s' %('\n'.join(map(str,cam_list)))
		else: pass
		return su_string
	except Exception as ex:
		return ('checkModelAttributes failed with: %s' %ex)
	pass


if __name__ =='__main__':
	main()

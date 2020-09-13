import math
import NXOpen

def main() :
	global theSession
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	theUI = NXOpen.UI.GetUI()
	lw = theSession.ListingWindow

def checkModelSections(workPart):
	isDrawing = 'DRAFTING' in theSession.ApplicationName
	isModeling = 'MODEL' in theSession.ApplicationName
	#надо задефить обнаружение режима моделирования или драфта. - готово в чек2д
	#а так же зафлаговать произвольное переключение между режимами пользователем
	#sect_listSections = []
	try:
		if len(workPart.DynamicSections) != 0: 
			cms_string = 'ЭМ содержит сечения:%s' %('\n'.join([item.Name for item in workPart.DynamicSections]))
		else: cms_string = 'ЭМ не содержит сечений' 
		return cms_string	
		#[listSections.append(item.Name) for item in workPart.DynamicSections]			
	except Exception as ex:
		return ex
	
	

if __name__ == '__main__':
	main()

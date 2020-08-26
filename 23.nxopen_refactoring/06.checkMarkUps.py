from math import *
import NXOpen
import NXOpen.UF
import re

#если строка техтребований начинается с \s, то, скорее всего, это неоконченная строка пункта
#это может быть и пропуск пункта, тогда нужно собрать все первые элементы строк и сортировать
#если же это буква , то выставить замечание по смещению текста в ТТ - upd 1897 нет такого требования, смотрит норма


################################Пункт проверки в проверку 2D#################################
def checkItemOrder(note,text): #не работает
	try:
		cio_firstItemInLine = []
		cio_checkItemOrderPass = True
		for cio_line in text:
			cio_firstItemInLine.append(associativeText.GetEvaluatedText(note, line)) #не первый элемент строки , а первые цифры в строке
		fn = [item for item in cio_firstItemInLine if isinstance(item, int)]
		if len(firstItemInLine) > 2:
			for item in firstItemInLine[1:]:
				if item < firstItemInLine[item.index - 1]:
					checkItemOrder = False
					break
				else:
					pass
		return checkItemOrderPass
	except Exception as ex:
		return('checkItemOrder failed with %s' %ex)
#############################################################################################

def checkSpecMarks(workPart): #добавить проверку текста "на бирке"
	try:
		csm_pmiLabelCollection = workPart.Labels
		csm_pmiNoteCollection = workPart.Notes
		csm_pmiCusotmCollection = workPart.Annotations.CustomSymbols
		csm_pmiBalloonnNotes = workPart.Annotations.BalloonNotes
		csm_associativeText = workPart.Annotations.CreateAssociativeText()
		list_marks = []
		list_stgm = []
		dict_marks = {}
		dict_stgm = {}
		for item in csm_pmiCusotmCollection:
			if 'triangle' in str(item.SymbolName).lower(): list_stgm.append(item)
			else: continue
		for item in csm_pmiBalloonnNotes:
			
			#data = item.GetSymbolData()
			#data_text = [''.join(item.GetText()) for item in data.GetTextData()] #list -> string
				#dict_stgm[item.JournalIdentifier] = data_text
				#lw.WriteLine('%s' %(dict_stgm))
			lw.WriteLine('%s -- %s -- %s' %(item.JournalIdentifier,item.SymbolName,data_text))
		#for note in noteCollection:		
		#	cd = workPart.Annotations.CreateComponentData(note)
		#	for textComponent in cd.GetTextComponents():
		
		#checkSpecMarksPass = True
		#markUps = {}
		#for line in text:  
		#	if 'клеймить' in line.lower:
		#		numLine = ''
		#		for ch in line:
		#			numLine+=ch if re.match(r'[0123456789]',ch) else break
		#		markUps[numLine] = 'клеймение'
		#	elif 'маркировать' in line.lower:
		#		numLine = ''
		#		for ch in line:
		#			numLine+=ch if re.match(r'[0123456789]',ch) else break
		#		markUps[numLine] = 'маркировка'	
		return markUps
	except Exception as ex:
		return('checkSpecMarks failed with %s' %ex)
	
def main() :
	theSession  = NXOpen.Session.GetSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	checkSpecMarks(workPart)
	#for note in noteCollection:		
	#	cd = workPart.Annotations.CreateComponentData(note)
	#	for textComponent in cd.GetTextComponents():
			#lw.WriteLine('Не соблюден порядок пунктов ТТ') if checkItemOrder(note,textComponent.GetText()) else pass
			#lw.WriteLine('ошибка в указании пунктов клеймения и маркировки') if checkSpecMarks(note,textComponent.GetText()) else pass
			
if __name__ == '__main__':
	main()

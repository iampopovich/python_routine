# Preview saving options - 	workPart.PartPreviewMode return a value of PreviewMode
#	0 - None	No preview image is stored for the part.
#	1 - OnSave	Create a preview image when the part is saved.
#	2 - OnDemand	Create a preview image on demand.
import math
import NXOpen

class NXJournal:
	def __init__(self):
		self.theSession  = NXOpen.Session.GetSession()
		self.workPart = self.theSession.Parts.Work
		self.lw = self.theSession.ListingWindow

	def checkPreviewMode(self):
		try:
			preview = self.workPart.PartPreviewMode
			if  preview is None: cpm_string = 'отключен'
			elif preview == NXOpen.BasePartPartPreview.OnSave: 
				cpm_string = 'по сохранению'
			elif preview == NXOpen.BasePartPartPreview.OnDemand:
				cpm_string = 'по требованию'
			return ('Режим предварительного просмотра: {0}'.format(cpm_string))
		except Exception as ex:
			return ('checkPreviewMode failed qwith %s' %ex)

	def setPreviewMode(self):	
		try:
			preview = self.workPart.PartPreviewMode
			if preview != NXOpen.BasePartPartPreview.OnDemand:
				preview = NXOpen.BasePartPartPreview.OnDemand
				return ('Режим предварительного просмотра изменен на \'по требованию\'')
			else: pass
		except Exception as ex:
			return ('setPreviewMode failed with %s' %ex)

def main() :
	app = NXJournal()
	app.lw.Open()
	app.lw.WriteLine(app.checkPreviewMode())

if __name__ == '__main__':
	main()

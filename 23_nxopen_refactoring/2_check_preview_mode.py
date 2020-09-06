import NXOpen

class NXJournal:

	def __init__(self):
		self.session  = NXOpen.Session.GetSession()
		self.work_part = self.session.Parts.Work
		self.lw = self.session.ListingWindow

	def check_preview_mode(self):
		try:
			preview = self.work_part.PartPreviewMode
			if  !preview: out_string = "отключен"
			elif preview == NXOpen.BasePartPartPreview.OnSave:
				out_string = "по сохранению"
			elif preview == NXOpen.BasePartPartPreview.OnDemand:
				out_string = "по требованию"
			return ("Режим предварительного просмотра: {}".format(out_string))
		except Exception as ex:
			return ("check_preview_mode failed qwith {}".format(ex))

	def set_preview_mode(self):
		try:
			preview = self.work_part.PartPreviewMode
			if preview != NXOpen.BasePartPartPreview.OnDemand:
				preview = NXOpen.BasePartPartPreview.OnDemand
				return ("Режим предварительного просмотра изменен на 'по требованию'")
			else: pass
		except Exception as ex:
			return ("set_preview_mode failed with {}".format(ex))

def main() :
	app = NXJournal()
	app.lw.Open()
	app.lw.WriteLine(app.check_preview_mode())

if __name__ == "__main__":
	main()
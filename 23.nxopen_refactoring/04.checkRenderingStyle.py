import math
import NXOpen

class NXJournal:
	def __init__(self):
		self.theSession  = NXOpen.Session.GetSession()
		self.workPart = self.theSession.Parts.Work
		self.displayPart = self.theSession.Parts.Display
		self.workView = self.workPart.Views.WorkView
		self.lw = self.theSession.ListingWindow

	def checkRenderingStyle(self):
		try:
			crs_list = []
			for view in self.workPart.ModelingViews:
				if view.RenderingStyle != NXOpen.View.RenderingStyleType.StaticWireframe:
					crs_list.append(view.Name)
			if len(crs_list) == 0: crs_string = 'Закраска видов соответствует требованиям'
			elif len(crs_list) == 1: crs_string = 'Закраска вида %s не соответствует требованиям' %('\n'.join(crs_list))
			elif len(crs_list) > 1: crs_string = 'Закраска видов не соответствует требованиям:\n%s' %('\n'.join(crs_list))
			else: pass
			return (crs_string)
		except Exception as ex:
			return ('checkRenderingStyle failed with %s' %ex)

	def setRenderingStyle(self,style):
		try:
			for view in self.workPart.ModelingViews:
				if view.RenderingStyle != style:
					view.RenderingStyle = style
			self.workView.RenderingStyle = NXOpen.View.RenderingStyleType.StaticWireframe
		except Exception as ex:
			return ('setRenderingStyle failed with %s' %ex)

def main() : 
	app = NXJournal()
	app.lw.Open()
	app.lw.WriteLine(app.checkRenderingStyle())
	
if __name__ == '__main__':
	main()

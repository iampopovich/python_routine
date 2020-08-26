import NXOpen

class NXJournal:

	def __init__(self):
		self.session  = NXOpen.Session.GetSession()
		self.work_part = self.session.Parts.Work
		self.work_view = self.work_part.Views.WorkView
		self.lw = self.session.ListingWindow

	def check_rendering_style(self):
		try:
			nx_style = NXOpen.View.RenderingStyleType.StaticWireframe
			views = self.work_part.ModelingViews
			out_list = list(filter(view.RenderingStyle != nx_style, views))
			if len(out_list) == 0:
				out_string = "Закраска видов соответствует требованиям"
			elif len(out_list) == 1:
				out_string = "Закраска вида {} не соответствует требованиям".format(
					"\n".join(out_list)
					)
			elif len(out_list) > 1:
				out_string = "Закраска видов не соответствует требованиям:\n{}".format(
					"\n".join(out_list)
					)
			else: pass
			return (out_string)
		except Exception as ex:
			return ("check_rendering_style failed with {}".format(ex))

	def set_rendering_style(self, style):
		try:
			for view in self.work_part.ModelingViews:
				if view.RenderingStyle != style:
					view.RenderingStyle = style
			self.work_view.RenderingStyle = NXOpen.View.RenderingStyleType.StaticWireframe
		except Exception as ex:
			return ("set_rendering_style failed with {}".format(ex))

def main() :
	app = NXJournal()
	app.lw.Open()
	app.lw.WriteLine(app.check_rendering_style())

if __name__ == "__main__":
	main()

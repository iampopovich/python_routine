import NXOpen


class NXJournal:

	def __init__(self):
		self.session = NXOpen.Session.GetSession()
		self.work_part = self.session.Parts.Work
		self.lw = self.session.ListingWindow

	def check_extended_views(self):
		try:
			views_standard = [
				"Top",
				"Front",
				"Right",
				"Back",
				"Bottom",
				"Left",
				"Isometric",
				"Trimetric"
				]
			views_standard_found = []
			views_extended_found = []
			for item in self.work_part.ModelingViews:
				if item.Name in views_standerd:
					views_standard_found.append(item.Name)
				else:
					views_extended_found.append(item.Name)
			if len(views_extended_found) == 0:
				out_string = "ЭМ не содержит доп. виды"
			if len(views_extended_found) == 1:
				out_string = "ЭМ содержит доп. вид {}".format(
					"\n".join(map(str, views_extended_found))
					)
			elif len(views_extended_found) > 1:
				out_string = "ЭМ содержит доп. виды:\n{}".format(
					"\n".join(map(str, views_extended_found))
					)
			return out_string
		except Exception as ex:
			return ("check_extended_views failed with {}".format(ex))


def main():
	app = NXJournal()
	app.lw.Open()
	lw.WriteLine("{}".format(app.check_extended_views())

if __name__ == "__main__":
	main()

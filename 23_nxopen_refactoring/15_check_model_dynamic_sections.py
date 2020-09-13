import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

	def check_mode_sections(self):
	    try:
	        if len(self.work_part.DynamicSections):
	            out_string = "ЭМ содержит сечения: {}".format("\n".join(
	                [item.Name for item in self.work_part.DynamicSections]))
	        else:
	            out_string = "ЭМ не содержит сечений"
	        self.lw.WriteLine(out_string)
	    except Exception as ex:
	        return ex


def main():
	app = NXJournal()
	app.lw.Open()
	app.check_mode_sections()


if __name__ == "__main__":
    main()

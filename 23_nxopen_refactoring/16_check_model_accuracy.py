import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

    def check_module_accuracy(self):
        try:
            distance = self.work_part.Preferences.Modeling.DistanceToleranceData
            angle = self.work_part.Preferences.Modeling.AngleToleranceData
            summary = {
                "Линейный допуск ЭМ": distance,
                "Угловой допуск ЭМ": angle}
            out_string = "\n".join(
                ["{}: {}".format(key, summary[key]) for key in summary])
            return out_string
        except Exception as ex:
            return ("check_module_accuracy failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine(app.check_module_accuracy())


if __name__ == "__main__":
    main()

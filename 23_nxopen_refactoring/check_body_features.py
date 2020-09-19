import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

    def check_unparameterized_bodies(self):
        out_list = []
        if self.work_part.Features.GetFeatures():
            for feature in self.work_part.Features:
                if isinstance(feature, NXOpen.Features.Brep):
                    out_list.append("{} - {}".format(
                        feature.Name, feature.JournalIdentifier))
            if len(out_list) == 0:
                return "ЭМ не содержит непараметризованных тел"
            elif len(out_list) == 1:
                return "ЭМ содержит непараметризованное тело: {}".format(
                    "\n".join(out_list))
            elif len(out_list) > 1:
                return "ЭМ содержит непараметризованные тела:\n{}".format(
                    "\n".join(out_list))
            else:
                pass
        else:
            return "ЭМ не содержит непараметризованных тел"


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine(app.check_unparameterized_bodies())


if __name__ == "__main__":
    main()

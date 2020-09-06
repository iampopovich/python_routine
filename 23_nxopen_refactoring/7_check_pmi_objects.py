import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.PMIs = self.work_part.PmiManager.Pmis

    def find_pmi_objects(self):
        try:
            if self.PMIs:
                pmi_list = [item.JournalIdentifier for item in self.PMIs]
                out_string = "Модель содержит объекты PMI \n{}".format(
                    "\n".join(map(str, pmi_list))
                )
            else:
                out_string = "Модель соответствует требованиям"
            return out_string
        except Exception as ex:
            return("find_pmi_objects failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.WriteLine(app.find_pmi_objects())


if __name__ == "__main__":
    main()

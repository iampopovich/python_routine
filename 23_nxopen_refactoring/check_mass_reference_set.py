import NXOpen
import NXOpen.UF
import NXOpen.Assemblies
from report_component_children import report_component_children


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.work_view = self.work_part.Views.WorkView
        self.lw = self.session.ListingWindow
        self.uf_session = NXOpen.UF.UFSession.GetUFSession()

    def cehck_mass_reference_set(self, reference_set = ""):
        try:
            model_mass_reference_set = self.uf_session.Weight.AskPartRefSet(
                self.workPart.Tag)
            if model_mass_reference_set == reference_set:
                return True
            else:
                self.lw.WriteLine("Проверка ссылочного набора расчета массы: СН\
                не соответствует требованиям")
                return False
        except Exception as ex:
            return ("cehck_mass_reference_set failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.cehck_mass_reference_set()


if __name__ == "__main__":
    main()

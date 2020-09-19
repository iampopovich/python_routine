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
        self.root_comopnent = self.work_part.ComponentAssembly.RootComponent

    def check_weight_statement(self):
        if not self.root_component:
            print("Root component is empty...")
            return
        component_objects = []
        component_objects.append(self.root_component)
        report_component_children(self.root_component, component_objects)
        out_list = []
        for item in component_objects:
            mass_props = self.uf_session.Weight.AskProps(
                item.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM)
            if mass_props.CacheState == NXOpen.UF.Weight.StateType.CACHED:
                out_list.append(
                    "Состояние массы {}: Расчет актуальный".format(item.Name))
            elif mass_props.CacheState == NXOpen.UF.Weight.StateType.NO_CACHE:
                out_list.append(
                    "Состояние массы {}: Расчет не актуальный".format(item.Name))
            elif mass_props.CacheState == NXOpen.UF.Weight.StateType.ASSERTED:
                out_list.append(
                    "Состояние массы {}: Назначена вручную".format(item.Name))
            elif mass_props.CacheState == NXOpen.UF.Weight.StateType.IMPLIED:
                pass
            elif mass_props.CacheState == NXOpen.UF.Weight.StateType.INHERITED:
                pass
            elif mass_props.CacheState == NXOpen.UF.Weight.StateType.UNKNOWN:
                pass
        return "\n".join(out_list)


def main():
    app = NXJournal()
    app.lw.Open()
    app.check_weight_statement()


if __name__ == "__main__":
    main()

import NXOpen
import NXOpen.Assemblies
from report_component_children import report_component_children


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

    def get_root_component(self):
        try:
            root_component = self.work_part.ComponentAssembly.RootComponent
            if root_component != 0:
                return root_component
            else:
                return None
        except Exception as ex:
            self.lw.WriteLine("Failed with {}".format(ex))

    def check_suppressed_objects(self, component, comp_object=None):
        component_objects = []
        suppressed_objects = []
        component_objects.append(component)
        reportComponentChildren(component, component_objects)
        try:
            for item in component_objects:
                if item.IsSuppressed:
                    attributes = []
                    items = tem.GetAttributeTitlesByType(
                        NXOpen.NXObjectAttributeType.String)
                    for item in items:
                        attributes.append(item.Title)
                    if "REFERENCE_COMPONENT" in attributes:
                        continue
                    else:
                        parent = item.Parent
                        suppressed_objects.append("{} ({})".format(
                            item.DisplayName, parent.DisplayName))
                        continue
                else:
                    pass
            suppressed_objects = set(suppressed_objects)
            if len(suppressed_objects) == 0:
                out_string = "ЭМ не содержит подавленные объекты"
            if len(suppressed_objects) == 1:
                out_string = "ЭМ содержит подавленный объект {}".format(
                    "\n".join(suppressed_objects))
            elif len(suppressed_objects) > 1:
                out_string = "ЭМ содержит подавленные объекты:\n{}".format(
                    "\n".join(suppressed_objects))
            else:
                pass
            return out_string
        except Exception as ex:
            return ("check_suppressed_objects failed with: {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    root_component = app.get_root_component()
    if root_component:
        lw.WriteLine(check_suppressed_objects(theSession, root_component))


if __name__ == "__main__":
    main()

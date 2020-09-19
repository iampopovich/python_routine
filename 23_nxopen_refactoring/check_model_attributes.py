import NXOpen
import NXOpen.UI
import NXOpen.Assemblies
import math
import re


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

    def check_model_attributes(self):
        attributes = [item.Title for item in item.GetAttributeTitlesByType(
            NXOpen.NXObjectAttributeType.String)]
        if "REFERENCE_COMPONENT" in attributes:
            continue
        else:
            parent = item.Parent
            non_reference_list.append("{} ({})".format(
                item.DisplayName,
                parent.DisplayName))
            non_reference_list = set(non_reference_list)
            if len(non_reference_list) == 0:
                su_string = ""
            if len(non_reference_list) == 1:
                su_string = "\s{}".format("\n".join(non_reference_list))
            elif len(non_reference_list) > 1:
                su_string = "\n{}".format("\n".join(non_reference_list))
            else:
                pass
            return su_string
        except Exception as ex:
            return ("check_model_attributes failed with: {}".format(ex))
        pass


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine(app.check_model_attributes())


if __name__ == "__main__":
    main()

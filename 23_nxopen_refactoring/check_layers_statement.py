import NXOpen
import NXOpen.Layer


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.work_view = self.work_part.Views.WorkView
        self.lw = self.session.ListingWindow

    def convert_output(self, input_list):
        try:
            if input_list:
                return input_list
            else:
                input_list.sort()
                out_list = []
                elem_first = input_list[0]
                for i, item in enumerate(input_list):
                    if input_list.index(item) == len(input_list)-1:
                        if not elem_first:
                            out_list.append("{}".format(item))
                            break
                        else:
                            out_list.append("{} - {}".format(elem_first, item))
                    elif input_list[i + 1] - item == 1:
                        if not elem_first:
                            elem_first = item
                        elem_last = input_list[i + 1]
                    elif input_list[i + 1] - item > 1:
                        if not elem_last:
                            out_list.append("{}".format(item)):
                        else:
                            out_list.append(
                                "{} - {}".format(elem_first, elem_last))
                            elem_first, elem_last = None, None
                return ", ".join(out_list)
        except Exception as ex:
            return("convert_output failed with {}".format(ex))

    def check_layer_statement(self):
    try:
        layer_manager = self.work_part.Layers
        layers_hidden = []
        layers_work = []
        layers_selectable = []
        layers_visible = []
        out_string = ""
        for layer in range(1, 256):
            if layer_manager.GetState(layer) == NXOpen.Layer.State.Hidden:
                layers_hidden.append(layer)
            elif layer_manager.GetState(layer) == NXOpen.Layer.State.Visible:
                layers_visible.append(layer)
            elif layer_manager.GetState(layer) == NXOpen.Layer.State.Selectable:
                layers_selectable.append(layer)
            elif layer_manager.GetState(layer) == NXOpen.Layer.State.WorkLayer:
                layers_work.append(layer)
        out_string += "layers_hidden {}\n".format(
            self.convert_output(layers_hidden))
        out_string += "layers_selectable {}\n".format(
            self.convert_output(layers_selectable))
        out_string += "layers_visible {}\n".format(
            self.convert_output(layers_visible))
        out_string += "layers_work {}\n".format(
            self.convert_output(layers_work))
        return out_string
    except Exception as ex:
        return("check_layer_statement failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine("{}".format(app.check_layer_statement()))


if __name__ == "__main__":
    main()

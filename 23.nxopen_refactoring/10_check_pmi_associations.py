import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.uf_session = NXOpen.UF.UFSession.GetUFSession()

    def find_retained_pmi(self):
        try:
            out_string = ""
            pmi_collection = self.work_part.PmiManager.Pmis
            associative_text = self.work_part.Annotations.CreateAssociativeText()
            retained_list = []
            for pmi_item in pmi_collection:
                pmi_item_gdi = pmi_item.GetDisplayInstances()[0]
                pmi_matrix = [
                    round(pmi_item_gdi.AnnotationOrigin.X),
                    round(pmi_item_gdi.AnnotationOrigin.Y),
                    round(pmi_item_gdi.AnnotationOrigin.Z)
                ]
                if pmi_item_gdi.IsRetained:
                    retained_list.append(pmi_matrix)
            if len(retained_list) == 0:
                out_string = "PMI связи не нарушены\n"
            elif len(retained_list) == 1:
                out_string = "Ассоциативная связь нарушена в точке \n{}".format(
                    "\n".join(map(str, retained_list)))
            else:
                out_string = "Ассоциативная связь нарушена в точках \n{}".format(
                    "\n".join(map(str, retained_list)))
            return out_string
        except Exception as ex:
            return("find_retained_pmi failed with {}"format(ex))

    def find _empty_pmi(self):
        try:
            out_string = ""
            pmi_collection = self.work_part.PmiManager.Pmis
            associative_text = self.work_part.Annotations.CreateAssociativeText()
            fep_emptyList = []
            for pmi_item in pmi_collection:
                fep_pmiItemGdi = pmi_item.GetDisplayInstances()[0]
                fep_PMIMatrix = [
                    round(fep_pmiItemGdi.AnnotationOrigin.X),
                    round(fep_pmiItemGdi.AnnotationOrigin.Y),
                    round(fep_pmiItemGdi.AnnotationOrigin.Z)
                ]
                if isinstance(fep_pmiItemGdi, NXOpen.Annotations.BalloonNote):
                    pmiBuilder = self.work_part.Annotations.CreateBalloonNoteBuilder(
                        fep_pmiItemGdi)
                elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.PmiLineWeld):
                    pmiBuilder = self.work_part.Annotations.Welds.CreatePmiLineWeldBuilder(
                        fep_pmiItemGdi)
                    continue  # заглушка
                elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.SurfaceFinish):
                    pmiBuilder = self.work_part.PmiManager.PmiAttributes.CreateSurfaceFinishBuilder(
                        fep_pmiItemGdi)
                    continue  # заглушка
                elif isinstance(fep_pmiItemGdi, NXOpen.Annotations.PmiCustomSymbol):
                    pmiBuilder = self.work_part.Annotations.CreatePmiCustomSymbolBuilder(
                        fep_pmiItemGdi)
                else:
                    pmiBuilder = self.work_part.Annotations.CreatePmiNoteBuilder(
                        fep_pmiItemGdi)
                try:
                    text = "".join(map(str, pmiBuilder.Text.GetEditorText()))
                    fep_pmiText = associative_text.GetEvaluatedText(
                        fep_pmiItemGdi, text)
                    if len(fep_pmiText) == 0:
                        fep_emptyList.append(fep_PMIMatrix)
                except Exception as ex:
                    lw.WriteLine("%s" % ex)
                    continue
            if len(fep_emptyList) == 0:
                out_string = "Все аннотации подписаны\n"
            elif len(fep_emptyList) == 1:
                out_string = "Отсутствует текст в точке \n{}".format(
                    "\n".join(map(str, fep_emptyList)))
            else:
                out_string = "Отсутствует текст в точках \n{}".format(
                    "\n".join(map(str, fep_emptyList)))
            return out_string
        except Exception as ex:
            return ("find_empty_pmi failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine(app.find_retained_pmi())
    app.lw.WriteLine(app.find_empty_pmi())


if __name__ == "__main__":
    main()

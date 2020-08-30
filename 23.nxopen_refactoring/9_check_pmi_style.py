import NXOpen


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.uf_session = NXOpen.UF.UFSession.GetUFSession()

    def check_distance_to_point(pCoord):
        try:
            return sqrt(pow(pCoord.X, 2) + pow(pCoord.Y, 2) + pow(pCoord.Z, 2))
        except Exception as ex:
            return("check_distance_to_point failed with %s" % ex)

    def check_annotation_style(self):
        try:
            cas_pmiCollection = self.work_part.PmiManager.Pmis
            associativeText = self.work_part.Annotations.CreateAssociativeText()
            cas_pmiListAlarm = []
            for pmi_item in cas_pmiCollection:
                pmi_item_gdi = pmi_item.GetDisplayInstances()[0]
                if isinstance(pmi_item_gdi, NXOpen.Annotations.PmiCenterMark):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiDiameterDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiNote):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiHorizontalDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.Region):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.Fcf):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PointTarget):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiCenterline3d):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiPerpendicularDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.BalloonNote):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiLineWeld):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.SurfaceFinish):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.Datum):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiMinorAngularDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiConcentricCircleDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiOrdinateOriginDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiVerticalOrdinateDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiChamferDimension):
                    continue
                elif isinstance(pmi_item_gdi, NXOpen.Annotations.PmiLabel):
                    pmi_builder = self.work_part.Annotations.CreatePmiNoteBuilder(
                        pmi_item_gdi)
                    pmi_lettering_style = pmi_builder.Style.LetteringStyle
                    pmi_prefs = pmi_item_gdi.GetLineAndArrowPreferences()
                    text = "".join(
                        map(str, pmi_builder.Text.GetEditorText()))
                    cas_pmiText = associativeText.GetEvaluatedText(
                        pmi_item_gdi, text)
                    if NXOpen.Annotations.ArrowheadType.FilledDot != pmi_prefs.FirstArrowType:
                        cas_pmiListAlarm.append(
                            "Несоответствущий тип 1 стрелки выноски {}".format(
                                cas_pmiText
                            )
                        )
                    elif NXOpen.Annotations.ArrowheadType.FilledDot != pmi_prefs.SecondArrowType:
                        cas_pmiListAlarm.append(
                            "Несоответствущий тип 2 стрелки выноски {}".format(
                                cas_pmiText
                            )
                        )
                    elif pmi_lettering_style.GeneralTextFont != 1:
                        cas_pmiListAlarm.append(
                            "Текст замечания {} не кириллический".format(
                                cas_pmiText
                            )
                        )
                    else:
                        pass
                elif pmi_item == NXOpen.Annotations.CustomSymbol:
                    pass
        except Exception as ex:
            return("check_annotation_style failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.check_annotation_style()


if __name__ == "__main__":
    main()

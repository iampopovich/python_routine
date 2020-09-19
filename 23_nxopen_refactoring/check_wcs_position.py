import NXOpen
import NXOpen.UF
import datetime as dt


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow

    def check_wcs_position(self):
        try:
            wcs_origin = self.work_part.WCS.CoordinateSystem.Origin
            for item in [wcs_origin.X, wcs_origin.Y, wcs_origin.Z]:
                if item == 0:
                    continue
                else:
                    return "РСК смещена по позиции"
            return "РСК в АСК"
        except Exception as ex:
            return ("check_wcs_position failed with {}".format(ex))

    def check_wcs_orientation(self):
        try:
            wcs_rotation_matrix = self.work_part.WCS.CoordinateSystem.Orientation
            for item in [
                    wcs_rotation_matrix.Element.Xx,
                    wcs_rotation_matrix.Element.Yy,
                    wcs_rotation_matrix.Element.Zz
            ]:
                if item == 1:
                    continue
                else:
                    return "ОШИБКА! РСК была перемещена!"
            return "РСК в АСК"
        except Exception as ex:
            return ("check_wcs_orientation failed with {}".format(ex))

    def set_wcs_orientation(self):
        try:
            wcs_origin = NXOpen.Point3d(0.0, 0.0, 0.0)
            wcs_matrix = NXOpen.Matrix3x3()
            wcs_matrix.Xx, wcs_matrix.Xy, wcs_matrix.Xz = 1.0, 0.0, 0.0
            wcs_matrix.Yx, wcs_matrix.Yy, wcs_matrix.Yz = 0.0, 1.0, 0.0
            wcs_matrix.Zx, wcs_matrix.Zy, wcs_matrix.Zz = 0.0, 0.0, 1.0
            self.work_part.WCS.SetOriginAndMatrix(wcs_origin, wcs_matrix)
        except Exception as ex:
            return ("set_wcs_orientation failed with {}".format(ex))


def main():
    app = NXJournal()
    app.lw.Open()
    app.lw.WriteLine("{}".format(app.check_wcs_orientation()))
    app.lw.WriteLine("{}".format(app.check_wcs_position()))


if __name__ == "__main__":
    main()

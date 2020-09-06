from math import *
import NXOpen
import NXOpen.UF
import re


class NXJournal:

    def __init__(self):
        self.session = NXOpen.Session.GetSession()
        self.work_part = self.session.Parts.Work
        self.lw = self.session.ListingWindow
        self.pointCollection = self.work_part.Points
        self.splineCollection = self.work_part.Splines
        self.orient_note = {}
        self.orient_view = []
        self.model_poles = []
        self.border_poles = []
        self.notes = self.work_part.Notes

    def detect_borders(self, segmentPoles, lw):
        polesX = []
        polesY = []
        polesZ = []
        result = {}
        [polesX.append(pole.X) for pole in segmentPoles]
        [polesY.append(pole.Y) for pole in segmentPoles]
        [polesZ.append(pole.Z) for pole in segmentPoles]
        [item.sort() for item in (polesX, polesY, polesZ)]
        result["minX"] = polesX[0]
        result["maxX"] = polesX[-1]
        result["minY"] = polesY[0]
        result["maxY"] = polesY[-1]
        result["minZ"] = polesZ[0]
        result["maxZ"] = polesZ[-1]
        return result

    def get_point_distance_on_view(self, point1, point2, distance=200):
        return (abs(point1)-abs(point2)) < distance

    def check_pmi_placement(self):
    	for note in self.notes:
        	for view in note.GetViews():
            	self.lw.WriteLine(str(view.Name))
            	np = note.AnnotationPlane
            for splineSegment in splineCollection:
                [modelPoles.append(pole) for pole in splineSegment.GetPoles()]
            borderPoles = self.detect_borders(modelPoles, lw)
            self.lw.WriteLine("{}".format(get_note_placement(
                borderPoles, note.AnnotationOrigin)))
            at = self.work_part.Annotations.CreateAssociativeText()
            cd = self.work_part.Annotations.CreateComponentData(note)


    def get_note_placement(self, borders, note_origin):
        flag = ""
        statement_y = [
            self.get_point_distance_on_view(note_origin.Y, borders["minY"]),
            self.get_point_distance_on_view(note_origin.Y, borders["maxY"])
        ]
        statement_z = [
            self.get_point_distance_on_view(note_origin.Z, borders["minZ"]),
            self.get_point_distance_on_view(note_origin.Z, borders["maxZ"])
        ]
        if note_origin.X < borders["maxX"]:
            flag += "за рамками X: min_x {} max_x {} planex {}".format(
                borders["minX"], borders["maxX"], note_origin.X)
        elif any(statement_y):
            flag += "за рамками Y: min_y {} max_y {} planey {}".format(
                borders["minY"], borders["maxY"], note_origin.Y)
        elif any(statement_z):
            flag += "за рамками Z: min_z {} max_z {} planez {}".format(
                borders["minZ"], borders["maxZ"], note_origin.Z)
        else:
            pass
        return flag

    def get_point_distance(self, coord):
        return sqrt(pow(coord.X, 2) + pow(coord.Y, 2) + pow(coord.Z, 2))


def main():
    app = NXJournal()
    app.lw.Open()
    app.check_pmi_placement()


if __name__ == "__main__":
    main()

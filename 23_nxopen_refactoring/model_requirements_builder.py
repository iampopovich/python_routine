# -*- coding: utf-8 -*-

import NXOpen
import NXOpen.BlockStyler
import NXOpen.UF
import NXOpen.Features
import subprocess
import re
import math
import collections
import itertools


class ColoredBlock:
    SnapPointTypesEnabled_UserDefined = 1
    SnapPointTypesEnabled_Inferred = 2
    SnapPointTypesEnabled_ScreenPosition = 4
    SnapPointTypesEnabled_EndPoint = 8
    SnapPointTypesEnabled_MidPoint = 16
    SnapPointTypesEnabled_ControlPoint = 32
    SnapPointTypesEnabled_Intersection = 64
    SnapPointTypesEnabled_ArcCenter = 128
    SnapPointTypesEnabled_QuadrantPoint = 256
    SnapPointTypesEnabled_ExistingPoint = 512
    SnapPointTypesEnabled_PointonCurve = 1024
    SnapPointTypesEnabled_PointonSurface = 2048
    SnapPointTypesEnabled_PointConstructor = 4096
    SnapPointTypesEnabled_TwocurveIntersection = 8192
    SnapPointTypesEnabled_TangentPoint = 16384
    SnapPointTypesEnabled_Poles = 32768

    SnapPointTypesOnByDefault_UserDefined = 1
    SnapPointTypesOnByDefault_Inferred = 2
    SnapPointTypesOnByDefault_ScreenPosition = 4
    SnapPointTypesOnByDefault_EndPoint = 8
    SnapPointTypesOnByDefault_MidPoint = 16
    SnapPointTypesOnByDefault_ControlPoint = 32
    SnapPointTypesOnByDefault_Intersection = 64
    SnapPointTypesOnByDefault_ArcCenter = 128
    SnapPointTypesOnByDefault_QuadrantPoint = 256
    SnapPointTypesOnByDefault_ExistingPoint = 512
    SnapPointTypesOnByDefault_PointonCurve = 1024
    SnapPointTypesOnByDefault_PointonSurface = 2048
    SnapPointTypesOnByDefault_PointConstructor = 4096
    SnapPointTypesOnByDefault_TwocurveIntersection = 8192
    SnapPointTypesOnByDefault_TangentPoint = 16384
    SnapPointTypesOnByDefault_Poles = 32768
    enum0 = NXOpen.BlockStyler.UIBlock

    def __init__(self):
        # class members
        self.group0 = None  # Block type: Group
        self.blockHeight = None  # Block type: Double
        self.blockWidth = None  # Block type: Double
        self.blockLength = None  # Block type: Double
        self.blockOrigin = None  # Block type: Specify Point
        self.blockColor = None  # Block type: Color Picker
        try:
            self.session = NXOpen.Session.GetSession()
            self.session_ui = NXOpen.UI.GetUI()
            self.session_uf = NXOpen.UF.UFSession.GetUFSession()
            self.work_part = self.session.Parts.Work
            self.session_path = self.session.ExecutingJournal
            self.work_file_name = re.search(
                r'[a-zA-Zа-яА-Я]{1,}\.py', self.session_path).group(0)
            self.dialog_path = self.session_path.replace('.py', '.dlx')
            self.executable_path = ''
            self.dialog = self.session_ui.CreateDialog(self.dialog_path)
            self.dialog.AddApplyHandler(self.apply_cb)
            self.dialog.AddInitializeHandler(self.initialize_cb)
            self.dialog.AddDialogShownHandler(self.dialogShown_cb)
            self.is_drafting = 'DRAFTING' in self.session.ApplicationName
            self.lw = self.session.ListingWindow
        except Exception as ex:
            raise ex

    def Show(self):
        try:
            self.dialog.Show()
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(
                'Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))

    def Dispose(self):
        if self.dialog != None:
            self.dialog.Dispose()
            self.dialog = None

    def initialize_cb(self):
        try:
            self.group0 = self.dialog.TopBlock.FindBlock('group0')
            self.blockHeight = self.dialog.TopBlock.FindBlock('blockHeight')
            self.blockWidth = self.dialog.TopBlock.FindBlock('blockWidth')
            self.blockLength = self.dialog.TopBlock.FindBlock('blockLength')
            self.blockOrigin = self.dialog.TopBlock.FindBlock('blockOrigin')
            self.blockColor = self.dialog.TopBlock.FindBlock('blockColor')
            self.enum0 = self.dialog.TopBlock.FindBlock('enum0')
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(
                'Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))

    def dialogShown_cb(self):
        try:
            pass
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(
                'Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))

    def apply_cb(self):
        errorCode = 0
        blockFeatureBuilder1 = None
        try:
            if self.enum0.GetProperties().GetEnum('Value') == 0:
                self.createTechRequirements(self)
            elif self.enum0.GetProperties().GetEnum('Value') == 1:
                self.rebuildTechRequirements(self)
            elif self.enum0.GetProperties().GetEnum('Value') == 2:
                self.editTechRequirements(self)
            elif self.enum0.GetProperties().GetEnum('Value') == 3:
                self.removeTechRequirements(self)
            else:
                pass
        except Exception as ex:
            errorCode = 1
            self.session_ui.NXMessageBox.Show(
                'Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))
        finally:
            if not blockFeatureBuilder1 == None:
                blockFeatureBuilder1.Destroy()
        return errorCode

        def scaleGrabber(self, parent):  # debug function
        self.lw.Open()
        for view in self.work_part.ModelingViews:
            layout = self.work_part.Layouts.FindObject('L1')
            layout.ReplaceView(
                self.work_part.ModelingViews.WorkView, view, True)
            view.Fit()
            self.lw.WriteLine('{} -- {}'.format(view.Name, view.Scale))

    def cycleObjects(self, parent, bodies=[], temp_body_tag=0):
        while True:
            temp_body_tag = self.session_uf.Obj.CycleObjsInPart(
                self.work_part.Tag, NXOpen.UF.UFConstants.UF_solid_type, temp_body_tag)
            if temp_body_tag == 0:
                break
            else:
                the_type, the_subtype = self.session_uf.Obj.AskTypeAndSubtype(
                    temp_body_tag)
                if the_subtype == NXOpen.UF.UFConstants.UF_solid_body_subtype:
                    bodies.append(
                        NXOpen.TaggedObjectManager.GetTaggedObject(temp_body_tag))
        return bodies

    def calculateScalePoint(self, parent, view, text, scale=1.000):
        self.lw.Open()
        bodies = self.cycleObjects(self)
        points = [self.session_uf.ModlGeneral.AskBoundingBox(
            item.Tag) for item in bodies]
        x_points, y_points, z_points = [], [], []
        [x_points.extend([point[0], point[3]]) for point in points]
        [y_points.extend([point[1], point[4]]) for point in points]
        [z_points.extend([point[2], point[5]]) for point in points]
        x_max, y_max, z_max = max(x_points), max(y_points), max(z_points)
        x_min, y_min, z_min = min(x_points), min(y_points), min(z_points)
        line1 = self.work_part.Curves.CreateLine(NXOpen.Point3d(
            x_max, y_max, z_max), NXOpen.Point3d(x_min, y_min, z_min))
        line2 = self.work_part.Curves.CreateLine(NXOpen.Point3d(
            x_max, y_max, z_min), NXOpen.Point3d(x_min, y_min, z_max))
        pointIntersect = self.session_uf.Curve.Intersect(
            line1.Tag, line2.Tag, [line1.StartPoint.X, line1.StartPoint.Y, line1.StartPoint.Z])
        pointPlane = NXOpen.Point3d(x_max, y_max, pointIntersect.CurvePoint[2])
        pointText = NXOpen.Point3d(x_max, y_max, pointIntersect.CurvePoint[2])
        builder_pmi_note = self.work_part.Annotations.CreatePmiNoteBuilder(
            NXOpen.Annotations.SimpleDraftingAid.Null)
        builder_pmi_note.Origin.Plane.PlaneMethod = NXOpen.Annotations.PlaneBuilder.PlaneMethodType.ModelView
        builder_pmi_note.Origin.Origin.SetValue(
            NXOpen.TaggedObject.Null, NXOpen.View.Null, pointText)
        builder_pmi_note.Origin.Anchor = NXOpen.Annotations.OriginBuilder.AlignmentPosition.MidLeft
        builder_pmi_note.Style.LetteringStyle.GeneralTextSize = 5.0
        builder_pmi_note.Style.LetteringStyle.GeneralTextFont = self.work_part.Fonts.AddFont(
            "cyrillic", NXOpen.FontCollection.Type.Nx)
        builder_pmi_note.Style.LetteringStyle.GeneralTextColor = self.work_part.Colors.Find(
            'Yellow')
        builder_pmi_note.Text.TextBlock.SetText(text)
        object_pmi = builder_pmi_note.Commit()
        plane = object_pmi.AnnotationPlane
        plane.SetOrigin(pointPlane)
        cd = self.work_part.Annotations.CreateComponentData(object_pmi)
        scale = (z_max - z_min)/(cd.GetTextComponents()[0]).Height
        self.session.UpdateManager.AddToDeleteList([line1, line2])
        builder_pmi_note.Text.TextBlock.SetText(['<C{}>'.format(scale)]+text+['<C>'])
        builder_pmi_note.ShowResults()
        builder_pmi_note.Commit()
        builder_pmi_note.Destroy()
        return object_pmi

    def createTechRequirements(self, parent):
        ctr_subprocess = subprocess.Popen(
            [self.executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = ctr_subprocess.communicate()[0]
        text = text.decode('utf-8')
        if self.is_drafting:
            scale = 1.000
            for index, part in enumerate(parts):
            builder_drafting_note = self.work_part.Annotations.CreateDraftingNoteBuilder(
                NXOpen.Annotations.SimpleDraftingAid.Null)
            text = ['<C{}>{}<C>'.format(scale, item) for item in part]
            builder_drafting_note.Text.TextBlock.SetText(text)
            s = child.stdout.readline().decode('cp866')
            except Exception as ex:
                self.lw.Open()
                self.lw.WriteLine(str(ex))
        else:
            if self.checkView(self) is None:
                layout = self.work_part.Layouts.FindObject('L1')
                view_modelling = self.work_part.ModelingViews.FindObject(
                    'Isometric')
                layout.ReplaceView(
                    self.work_part.ModelingViews.WorkView, view_modelling, True)
                view_modelling = self.work_part.Views.SaveAsPreservingCase(
                    view_modelling, 'ИЗОМЕТРИЧЕСКИЙ', True, False)
                layout.ReplaceView(
                    self.work_part.ModelingViews.WorkView, view_modelling, True)
            else:
                view_modelling = self.checkView(self)
            text = text.split('\r\n')
            object_pmi = self.calculateScalePoint(self, view_modelling, text)
            builder_general_properties = self.work_part.PropertiesManager.CreateObjectGeneralPropertiesBuilder([object_pmi])
            # 'ТЕХНИЧЕСКИЕ_ТРЕБОВАНИЯ_%i' %index
            builder_general_properties.Name = 'ТЕХНИЧЕСКИЕ_ТРЕБОВАНИЯ'
            builder_general_properties.Commit()
            builder_general_properties.Destroy()
            display_modification = self.session.DisplayManager.NewDisplayModification()
            display_modification.NewLayer = 9
            display_modification.Apply([object_pmi])
            display_modification.Dispose()
            view_modelling.Fit()

    def editTechRequirements(self, parent):
        try:
            view_modelling = self.checkView(self)
            note_tag = self.checkNote(self, view_modelling)
            if view_modelling is None:
                self.session_ui.NXMessageBox.Show(
                    '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'Вид отсутствует')
                return None
            if note_tag is None:
                self.session_ui.NXMessageBox.Show(
                    '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'ТТ отсутствуют')
                return None
            note_tagged = NXOpen.TaggedObjectManager.GetTaggedObject(note_tag)
            builder_pmi_note = self.work_part.Annotations.CreatePmiNoteBuilder(
                note_tagged)
            text = builder_pmi_note.Text.TextBlock.GetText()
            scale = [text[0], text[-1]]
            text = '\n'.join(text[1:-1])
            etr_subprocess = subprocess.Popen(
                [self.executable_path, text], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            text = etr_subprocess.communicate()[0]
            text = text.decode('cp1251')
            if len(text) != 0:
                text = text.split('\r\n')
                builder_pmi_note.Text.TextBlock.SetText(
                    [scale[0]]+text+[scale[1]])
                builder_pmi_note.ShowResults()
            builder_pmi_note.Commit()
            builder_pmi_note.Destroy()
            view_modelling.Fit()
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(
                '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'editTechReqs failed with {}'.format(ex))

    def rebuildTechRequirements(self, parent):
        try:
            view_modelling = self.checkView(self)
            note_tag = self.checkNote(self, view_modelling)
            if view_modelling is None:
                self.session_ui.NXMessageBox.Show(
                    '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'Вид отсутствует')
                return None
            if note_tag is None:
                self.session_ui.NXMessageBox.Show(
                    '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'ТТ отсутствуют')
                return None
            builder_pmi_note = self.work_part.Annotations.CreatePmiNoteBuilder(
                note_tagged)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(
                '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'Вид отсутствует')

    def checkView(self, parent):
        try:
            layout = self.work_part.Layouts.FindObject('L1')
            view_modelling = self.work_part.ModelingViews.FindObject(
                'ИЗОМЕТРИЧЕСКИЙ')
            layout.ReplaceView(
                self.work_part.ModelingViews.WorkView, view_modelling, True)
            return view_modelling
        except:
            return None

    def checkNote(self, parent, view=None, note_tag=None):
        pmiNotes = [item for item in view.AskVisibleObjects(
        ) if isinstance(item, NXOpen.Annotations.PmiNote)]
        note_tag = [item.Tag for item in pmiNotes if item.Name in [
            'ТЕХНИЧЕСКИЕ_ТРЕБОВАНИЯ']]
        return note_tag[0]

    def removeTechRequirements(self, parent):
        note_tag = self.checkNote(self)
        if note_tag is None:
            self.session_ui.NXMessageBox.Show(
                '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'ТТ отсутствуют.')
            return None
        else:
            note_tagged = NXOpen.TaggedObjectManager.GetTaggedObject(note_tag)

            self.session.UpdateManager.AddToDeleteList([note_tagged])
            self.session_ui.NXMessageBox.Show(
                '__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'ТТ удалены.')


def main():
    try:
        theColoredBlock = ColoredBlock()
        theColoredBlock.Show()
    except Exception as ex:
        NXOpen.UI.GetUI().NXMessageBox.Show(
            'Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))
    finally:
        theColoredBlock.Dispose()


if __name__ == '__main__':
    main()

'''
'See the APPLICATION_BUTTON's defined in the ug_main.men file
        'UG_APP_GATEWAY
        'UG_APP_MODELING
        'UG_APP_STUDIO
        'UG_APP_DRAFTING
        'UG_APP_MANUFACTURING
        'UG_APP_SFEM
        'UG_APP_DESFEM
        'UG_APP_MECHANISMS
        'UG_APP_MECHATRONICS
        'UG_APP_SHEETMETAL
        'UG_APP_PCB_DESIGN
        'UG_APP_ROUTING
        'etc.
'''

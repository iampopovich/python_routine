# -*-coding: utf-8-*-
import NXOpen
import NXOpen.UF
import NXOpen.Layer
import NXOpen.BlockStyler
import NXOpen.Drawings
import collections
import sqlite3
import inspect
import string
import math
import json
import re
import os


class Formats:
    # class static collections

    enumerated_drawing_sheets = {}

    standard_scales = {
        0: [1.0, 100.0], 1: [1.0, 75.0], 2: [1.0, 50.0],
        3: [1.0, 40.0], 4: [1.0, 25.0], 5: [1.0, 20.0],
        6: [1.0, 15.0], 7: [1.0, 10.0], 8: [1.0, 5.0],
        9: [1.0, 4.0], 10: [1.0, 2.5], 11: [1.0, 2.0],
        12: [1.0, 1.0], 13: [2.0, 1.0], 14: [2.5, 1.0],
        15: [4.0, 1.0], 16: [5.0, 1.0], 17: [10.0, 1.0],
        18: [20.0, 1.0], 19: [40.0, 1.0], 20: [50.0, 1.0],
        21: [100.0, 1.0]}

    # system"s functions

    def __init__(self):
        try:
            self.version = "v0.12.2_a"
            self.session = NXOpen.Session.GetSession()
            self.work_part = self.session.Parts.Work
            self.session_ui = NXOpen.UI.GetUI()
            self.session_uf = NXOpen.UF.UFSession.GetUFSession()
            self.session_path = self.session.ExecutingJournal
            self.dlx_file_name = self.session_path.replace(".py", ".dlx")
            self.dialog = self.session_ui.CreateDialog(self.dlx_file_name)
            self.dialog.AddCloseHandler(self.close_cb)
            self.dialog.AddUpdateHandler(self.update_cb)
            self.dialog.AddInitializeHandler(self.initialize_cb)
            self.dialog.AddDialogShownHandler(self.dialogShown_cb)
            self.isDrawing = "DRAFTING" in self.session.ApplicationName
            self.rtComp = self.work_part.ComponentAssembly.RootComponent
            self.errorTemplate = string.Template("$function failed with $ex")
            ###задефил системные типы и имена###
            self.MSG_Error = NXOpen.NXMessageBox.DialogType.Error
            self.MSG_Info = NXOpen.NXMessageBox.DialogType.Information
            self.MSG_Question = NXOpen.NXMessageBox.DialogType.Question
            self.MSG_Warning = NXOpen.NXMessageBox.DialogType.Warning
            self.moduleName = "Редактор чертежных форматов {0}".format(
                self.version)
            ###end section###
            self.workPartGroups = []
            self.cacheFile = self.getCacheFile()
            self.templates_database = self.session_path.replace(
                os.path.basename(__file__), "templates.sqlite")
            self.is_valid_template_database = self.validTemplatesDataBase()
            self.isVertical = False
            self.moreThanOneSheet = None
        except Exception as ex:
            raise ex

    def Show(self):
        try:
            self.dialog.Show()
        except Exception as ex:
            raise ex

    def Dispose(self):
        if self.dialog != None:
            self.dialog.Dispose()
            self.dialog = None

    def initialize_cb(self):
        try:
            self.tabControl = self.dialog.TopBlock.FindBlock("tabControl")
            self.tabPage = self.dialog.TopBlock.FindBlock(
                "tabPage")  # атрибуты
            self.tabPage1 = self.dialog.TopBlock.FindBlock(
                "tabPage1")  # формат
            self.button0 = self.dialog.TopBlock.FindBlock(
                "button0")  # удалить текущий лист
            self.button01 = self.dialog.TopBlock.FindBlock(
                "button01")  # применить изменение для атрибутов
            self.button02 = self.dialog.TopBlock.FindBlock(
                "button02")  # применить изменение для листов
            self.string0 = self.dialog.TopBlock.FindBlock(
                "string0")  # текущий размер листа
            self.string01 = self.dialog.TopBlock.FindBlock(
                "string01")  # free
            self.string02 = self.dialog.TopBlock.FindBlock(
                "string02")  # free
            self.string03 = self.dialog.TopBlock.FindBlock(
                "string03")  # free
            self.string04 = self.dialog.TopBlock.FindBlock(
                "string04")  # Наименование изделия
            self.string06 = self.dialog.TopBlock.FindBlock(
                "string06")  # Наименование документа
            self.string07 = self.dialog.TopBlock.FindBlock(
                "string07")  # Нормоконтроль
            self.string08 = self.dialog.TopBlock.FindBlock(
                "string08")  # Первичная применяемость
            self.string09 = self.dialog.TopBlock.FindBlock(
                "string09")  # Будущий размер листа
            self.string10 = self.dialog.TopBlock.FindBlock(
                "string10")  # Утвердил
            self.string11 = self.dialog.TopBlock.FindBlock(
                "string11")  # Руководитель
            self.string12 = self.dialog.TopBlock.FindBlock(
                "string12")  # Должность руководителя
            self.string13 = self.dialog.TopBlock.FindBlock(
                "string13")  # Технологический контроль
            self.string14 = self.dialog.TopBlock.FindBlock(
                "string14")  # Проверил
            self.string15 = self.dialog.TopBlock.FindBlock(
                "string15")  # Разработал
            self.string16 = self.dialog.TopBlock.FindBlock(
                "string16")  # Номер ДД
            self.string17 = self.dialog.TopBlock.FindBlock(
                "string17")  # free
            self.string18 = self.dialog.TopBlock.FindBlock(
                "string18")  # масштаб
            self.string20 = self.dialog.TopBlock.FindBlock(
                "string20")  # Масса изделия
            self.string21 = self.dialog.TopBlock.FindBlock(
                "string21")  # Материал детали
            self.string22 = self.dialog.TopBlock.FindBlock(
                "string22")  # free
            self.string23 = self.dialog.TopBlock.FindBlock(
                "string23")  # free
            self.string24 = self.dialog.TopBlock.FindBlock(
                "string24")  # free
            self.group = self.dialog.TopBlock.FindBlock(
                "group")  # новый формат
            self.group1 = self.dialog.TopBlock.FindBlock("group1")  # литера
            self.group2 = self.dialog.TopBlock.FindBlock(
                "group2")  # добавление нового листа
            self.group3 = self.dialog.TopBlock.FindBlock(
                "group3")  # ответственные лица
            self.group4 = self.dialog.TopBlock.FindBlock(
                "group4")  # справочные атрибуты
            self.group5 = self.dialog.TopBlock.FindBlock(
                "group5")  # ориентация листа
            self.enum0 = self.dialog.TopBlock.FindBlock(
                "enum0")  # выбор формата
            self.enum01 = self.dialog.TopBlock.FindBlock("enum01")  # литера
            self.enum02 = self.dialog.TopBlock.FindBlock("enum02")
            self.enum03 = self.dialog.TopBlock.FindBlock(
                "enum03")  # выбор ориентации листа
            self.enum04 = self.dialog.TopBlock.FindBlock(
                "enum04")  # Индекс литеры
            self.enum05 = self.dialog.TopBlock.FindBlock(
                "enum05")  # выбор_Масштаба
            self.toggle0 = self.dialog.TopBlock.FindBlock("toggle0")
            self.toggle01 = self.dialog.TopBlock.FindBlock("toggle01")
            self.toggle02 = self.dialog.TopBlock.FindBlock("toggle02")
            self.toggle03 = self.dialog.TopBlock.FindBlock(
                "toggle03")  # добавить на новый лист
        except Exception as ex:
            raise ex

    def dialogShown_cb(self):
        try:
            self.clearEmptyGroups()
            if self.checkSheetCollectionSize():
                pass
            else:
                self.recalculateSheetsAndGroupsNames()
            self.setDefaultProps()
        except Exception as ex:
            raise ex

    def close_cb(self):
        errorCode = 0
        try:
            return errorCode
        except Exception as ex:
            errorCode = 1
            raise ex

    def update_cb(self, block):
        try:
            if block == self.button0:
                self.commitSheetChanges(block)
            elif block == self.button01:
                self.commitAttributeChanges(block)
            elif block == self.toggle03:
                self.checkIsValidTemplate()
            elif block == self.enum0:
                self.checkIsValidTemplate()
                self.string09.Value = self.resolveNewSizes()
            elif block == self.enum03:
                self.isVertical = bool(
                    self.enum03.GetProperties().GetEnum("Value"))
                self.string09.Value = self.resolveNewSizes()
            elif block == self.button02:
                self.commitSheetChanges(block)
            elif block == self.enum01:
                self.enableLetterInserting()
        except Exception as ex:
            raise ex
        return 0

    def GetBlockProperties(self, blockID):
        try:
            return self.dialog.GetBlockProperties(blockID)
        except Exception as ex:
            raise ex
        return None

    # custom functions

    def validTemplatesDataBase(self):
        try:
            if os.path.isfile(self.templates_database):
                pass
            else:
                self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                             "Отсутствует файл базы даных шаблонов")
                return False
            query = """select * from templates_ limit 1"""
            response = self.sendBaseQuery(query)
            if isinstance(response, sqlite3.Error):
                self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                             "Файл базы данных шаблонов поврежден")
                return False
            return True
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def loadCachedInput(self):
        try:
            dictCachedInput = {}
            with open(self.cacheFile) as cache:
                dictCachedInput = json.load(cache)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))
            return False
        try:
            self.string10.Value = dictCachedInput["DRW_approve_user"]
        except:
            return False
        try:
            self.string11.Value = dictCachedInput["DRW_Lider"]
        except:
            return False
        try:
            self.string12.Value = dictCachedInput["DRW_Grafa_10"]
        except:
            return False
        try:
            self.string15.Value = dictCachedInput["DRW_owner"]
        except:
            return False
        return True

    def writeCacheFile(self, values):
        try:
            fileCache = self.cacheFile
            with open(fileCache, "w") as prevInput:
                json.dump(values, prevInput)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def getCacheFile(self):
        try:
            dirName = "{0}\\NX_DMCache".format(os.environ["APPDATA"])
            fileName = "{0}\\NX_DMCache\\cache.json".format(
                os.environ["APPDATA"])
            if os.path.isdir(dirName):
                pass
            else:
                os.mkdir(dirName)
            if os.path.isfile(fileName):
                return fileName
            else:
                with open(fileName, "a") as cache:
                    cache.close()
                return fileName
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def writeLog(self):
        try:
            dirName = "{0}\\NX_DMCache".format(os.environ["APPDATA"])
            fileName = "{0}\\NX_DMCache\\log.txt".format(os.environ["APPDATA"])
            if os.path.isdir(dirName):
                pass
            else:
                os.mkdir(dirName)
            if os.path.isfile(fileName):
                return fileName
            else:
                with open(fileName, "w") as log:
                    log.close()
            with open(fileName, "a") as log:
                log.write("пишем стату по сеансам и падениям")
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def commitSheetChanges(self, block):
        try:
            if block == self.button02:
                if self.toggle03.Value:
                    self.appendNewSheet()
                else:
                    self.editCurrentSheet()
            if block == self.button0:
                self.deleteCurrentSheet()
            self.returnCurrentSizes()
            self.checkSheetCollectionSize()
            self.recalculateZoneMarkUps()
            self.recalculateSheetsAndGroupsNames()
            self.commitAttributeChanges()
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkIsDrafting(self):
        try:
            if self.isDrawing:
                return True
            else:
                self.session.ApplicationSwitchImmediate("UG_APP_DRAFTING")
                alertString = "Вы переключены в режим \"Черчение\"."
                self.session_ui.NXMessageBox.Show(
                    self.moduleName, self.MSG_Info, alertString)
                return True
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def deleteCurrentSheet(self):
        try:
            removeCode = self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Question, "Лист будет удален. Продолжить?")
            if removeCode == 1:
                sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
                self.deleteChainedGroup(sheet)
                markId1 = self.session.SetUndoMark(
                    NXOpen.Session.MarkVisibility.Invisible, "Delete")
                self.session.UpdateManager.ClearErrorList()
                self.session.UpdateManager.AddToDeleteList([sheet])
                self.session.UpdateManager.DoUpdate(markId1)
                self.session.UpdateManager.ClearDeleteList()
            else:
                pass
            return None
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkIsScaleEnable(self):
        try:
            drawingSheetBuilder = None
            sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                sheet)
            if int(drawingSheetBuilder.Number) == 1:
                self.enum05.Enable = True
            else:
                self.enum05.Enable = False
            drawingSheetBuilder.Destroy()
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkIsValidTemplate(self):
        try:
            if not(re.search(r"(A4|А4)\s\(", self.enum0.ValueAsString) is None):
                self.enum03.Enable = False
                self.enum03.GetProperties().SetEnum("Value", 1)
            else:
                self.enum03.GetProperties().SetEnum("Value", 0)
                self.enum03.Enable = True
            self.isVertical = bool(
                self.enum03.GetProperties().GetEnum("Value"))
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def calculateFormatArea(self):
        try:
            if len(list(self.work_part.DrawingSheets)) != 0:
                totalArea = 0.0
                for sheet in self.work_part.DrawingSheets:
                    drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                        sheet)
                    totalArea += drawingSheetBuilder.Height * drawingSheetBuilder.Length
                    drawingSheetBuilder.Destroy()
                totalArea /= (210 * 297)
                return str(math.floor(totalArea))
            else:
                return ""
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))
            return "--Площадь чертежа не посчитана--"

    def clearEmptyGroups(self):
        try:
            self.askWorkPartGroups()
            if self.workPartGroups.__len__() == 0:
                return None
            deleteGroups = []
            for group in self.workPartGroups:
                membersTags = self.session_uf.Group.AskGroupData(group.Tag)[0]
                #nameFlag = not(re.search(r"формат*",group.Name.lower()) is None)
                nameFlag = not(
                    re.search(r"Format", group.GetStringAttribute("DB_PART_MFKID")) is None)
                if len(membersTags) == 0 and nameFlag:
                    deleteGroups.append(group)
                else:
                    continue
            markId1 = self.session.SetUndoMark(
                NXOpen.Session.MarkVisibility.Invisible, "Delete")
            self.session.UpdateManager.ClearErrorList()
            self.session.UpdateManager.AddToDeleteList(deleteGroups)
            self.session.UpdateManager.DoUpdate(markId1)
            self.session.UpdateManager.ClearDeleteList()
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def recalculateSheetsAndGroupsNames(self):
        try:
            drawingSheetBuilder = None
            started_sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            for sheet in self.work_part.DrawingSheets:
                try:
                    shNum = int(
                        re.search(r"Лист \d{1,4}", sheet.Name).group(0).split()[1])
                    drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                        sheet)
                    if int(drawingSheetBuilder.Number) == shNum:
                        pass
                    else:
                        if len(str(len(list(self.work_part.DrawingSheets)))) > 1:
                            drawingSheetBuilder.Name = "Лист {0}".format(
                                int(shNum) - 1)
                        else:
                            drawingSheetBuilder.Name = "Лист 0{0}".format(
                                int(shNum) - 1)
                        drawingSheetBuilder.Commit()
                    drawingSheetBuilder.Destroy()
                    self.editChainedGroupName(sheet)
                except:
                    if not (drawingSheetBuilder is None):
                        drawingSheetBuilder.Destroy()
                    continue
            started_sheet.Open()
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def getLeaderSheetFormat(self):
        try:
            drawingSheetBuilder = None
            formatNameNote = None
            if len(list(self.work_part.DrawingSheets)) == 0:
                return self.enum0.ValueAsString.split()[0]
            started_sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            firstSheet = list(self.work_part.DrawingSheets)[0]
            firstSheet.Open()
            view_drafting = firstSheet.View
            for item in view_drafting.AskVisibleObjects():
                match_type = isinstance(item, NXOpen.Annotations.Note)
                match_name = item.Name == "FORMAT_NAME"
                if match_name and match_type:
                    formatNameNote = item
                else:
                    continue
            if formatNameNote is None:
                return ""
            else:
                builder_drafting_note = self.work_part.Annotations.CreateDraftingNoteBuilder(
                    formatNameNote)
                text = "".join(builder_drafting_note.Text.GetEditorText())
                builder_drafting_note.Destroy()
                started_sheet.Open()
                return text.split()[-1]
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def resolveNewSizes(self):
        try:
            templateName = self.enum0.GetProperties().GetEnum("Value")
            orientation = 'v' if self.isVertical else 'h'
            query = """select height_, width_ from templates_
						where enum_value_ = {0} 
						and orientation_ like \"{1}\"""".format(templateName, orientation)
            response = self.sendBaseQuery(query)[0]
            _h, _w = response[0], response[1]
            string_size = "{0} x {1}".format(int(_h), int(_w))
            return string_size
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def returnCurrentSizes(self):
        try:
            sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            if sheet is None:
                return None
            else:
                size_string = "{0} x {1}".format(
                    int(sheet.Height), int(sheet.Length))
                self.string0.Value = size_string
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def enableLetterInserting(self):
        try:
            if self.enum01.GetProperties().GetEnum("Value") in [0, 2, 3]:
                self.enum04.Enable = False
            else:
                self.enum04.Enable = True
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkSheetCollectionSize(self):
        try:
            drawingSheetBuilder = None
            if len(list(self.work_part.DrawingSheets)) > 1:
                self.moreThanOneSheet = "1"
            else:
                self.moreThanOneSheet = ""
            flag = list(self.work_part.DrawingSheets).__len__() == 0
            self.toggle03.Value = flag
            self.toggle03.Enable = not flag
            if flag:
                self.button0.Enable = not flag
            else:
                sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
                drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                    sheet)
                if int(drawingSheetBuilder.Number) == 1:
                    self.button0.Enable = False
                else:
                    self.button0.Enable = not flag
                drawingSheetBuilder.Destroy()
            return flag
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def setDefaultProps(self):
        self.validateAttributes()
        self.isVertical = bool(self.enum03.GetProperties().GetEnum("Value"))
        if self.checkSheetCollectionSize():
            createCode = self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Question, "Деталь не содержит чертежных листов.\nСоздать сейчас?")
            if createCode == 1:
                self.resolveNewSizes()
                self.appendNewSheet()
                self.recalculateSheetsAndGroupsNames()
                self.checkSheetCollectionSize()
                self.commitAttributeChanges()
            else:
                pass
        else:
            pass
        self.checkIsScaleEnable()
        self.checkIsValidTemplate()
        if self.loadCachedInput():
            pass
        else:
            try:
                self.string10.Value = self.work_part.GetStringAttribute(
                    "DRW_approve_user")
            except:
                self.string10.Value = ""
            try:
                self.string14.Value = self.work_part.GetStringAttribute(
                    "DRW_check_user")
            except:
                self.string14.Value = ""
            try:
                self.string15.Value = self.work_part.GetStringAttribute(
                    "DRW_owner")
            except:
                self.string15.Value = ""
            try:
                self.string11.Value = self.work_part.GetStringAttribute(
                    "DRW_Lider")
            except:
                self.string11.Value = ""
            try:
                self.string12.Value = self.work_part.GetStringAttribute(
                    "DRW_Grafa_10")
            except:
                self.string12.Value = "Нач. отд"
        try:
            letterProp = self.work_part.GetStringAttribute("DRW_litera_letter")
            letterIndex = self.work_part.GetStringAttribute("DRW_litera_index")
            self.enum01.GetProperties().SetEnumAsString("Value", letterProp)
            self.enum04.GetProperties().SetEnumAsString("Value", letterIndex)
        except:
            self.enum01.GetProperties().SetEnum("Value", 0)
            self.enum04.GetProperties().SetEnum("Value", 0)
        try:
            self.returnCurrentSizes()
        except:
            self.string0.Value = ""
        try:
            self.string04.Value = self.checkDocumentName()
        except:
            self.string04.Value = ""
        try:
            self.string06.Value = self.checkDocumentType()
        except:
            self.string06.Value = ""
        try:
            self.string07.Value = self.work_part.GetStringAttribute("DRW_NK")
        except:
            self.string07.Value = ""
        try:
            self.string08.Value = self.work_part.GetStringAttribute(
                "DRW_first_used")
        except:
            self.string08.Value = ""
        try:
            self.string13.Value = self.work_part.GetStringAttribute("DRW_TK")
        except:
            self.string13.Value = ""
        try:
            self.string16.Value = self.work_part.GetStringAttribute(
                "DRW_directive_ref")
        except:
            self.string16.Value = ""
        try:
            self.string20.Value = self.checkBaseModelWeight()
        except:
            self.string20.Value = self.work_part.GetStringAttribute(
                "DRW_prod_weight")
        try:
            self.string21.Value = self.checkBaseModelMaterial()
        except:
            self.string21.Value = self.work_part.GetStringAttribute(
                "DRW_prod_material")
        self.enum05.GetProperties().SetEnum("Value", 12)
        self.enableLetterInserting()
        try:
            self.string09.Value = self.resolveNewSizes()
        except:
            self.string09.Value = ""

    def checkDocumentName(self):
        try:
            nameAttrib = self.work_part.GetStringAttribute("DB_PART_DESC")
            documentName = nameAttrib.split(".")
            if len(documentName) == 1:
                return nameAttrib
            elif len(documentName) > 1:
                return "".join(documentName[:-1:])
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))
            return ""

    def sendBaseQuery(self, query):
        try:
            connection = sqlite3.connect(self.templates_database)
            cursor = connection.cursor()
            response = cursor.execute(query)
            results = response.fetchall()
            connection.close()
            return results
        except sqlite3.Error as sqlerror:
            connection.close()
            return sqlerror
        except Exception as ex:
            connection.close()
            return ex

    def checkDocumentType(self):
        try:
            typeAttrib = self.work_part.GetStringAttribute("DB_PART_TYPE")
            query = "select document_name_translate_ from templates_ where document_name_ like {0}".format(
                typeAttrib)
            try:
                documentType = self.sendBaseQuery(query)
            except:
                documentType = "--Требуется ручной ввод--"
            return documentType
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))
            return ""

    def validateAttributes(self):
        try:
            keys = [
                "DRW_title", "DRW_doc_name", "DRW_prod_material",
                "DRW_litera", "DRW_litera_letter", "DRW_litera_index",
                "DRW_prod_weight", "DRW_scale", "DRW_change_sheet",
                "DRW_directive_ref", "DRW_owner", "DRW_check_user",
                "DRW_TK", "DRW_Grafa_10", "DRW_Lider", "DRW_NK",
                "DRW_approve_user", "DRW_first_used",
                "DRW_format", "DRW_first_page", "DRW_A4_amt"]
            attributePropertiesBuilder = self.session.AttributeManager.CreateAttributePropertiesBuilder(self.work_part,
                                                                                                           [self.work_part],
                                                                                                           NXOpen.AttributePropertiesBuilder.OperationType.NotSet)
            for key in keys:
                try:
                    self.work_part.GetStringAttribute(key)
                except:
                    attributePropertiesBuilder.Title = key
                    attributePropertiesBuilder.DataType = NXOpen.AttributePropertiesBaseBuilder.DataTypeOptions.String
                    attributePropertiesBuilder.StringValue = ""
                    attributePropertiesBuilder.CreateAttribute()
                    continue
            attributePropertiesBuilder.Commit()
            attributePropertiesBuilder.Destroy()
        except Exception as ex:
            if not (attributePropertiesBuilder is None):
                attributePropertiesBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def convertProductMaterial(self):
        try:
            material = self.string21.Value
            if "/" in material:
                try:
                    header = re.search(
                        r"Рельс\s{0,}(двухголовый|тавровый|типа (P5|Р5))", material).group(0)
                except:
                    header = material.split(" ", 1)[0]
                cl_ = material.split(header)[1].split("/")  # replace("/","!")
                convertedMaterial = "{0} <V{1}!{2}>".format(
                    header, cl_[0], cl_[1])
                return convertedMaterial
            else:
                return material
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def commitAttributeChanges(self, sender=None, msg=False):
        try:
            attributePropertiesBuilder = None
            dictToCache = {}
            attributePropertiesBuilder = self.session.AttributeManager.CreateAttributePropertiesBuilder(self.work_part,
                                                                                                           [self.work_part],
                                                                                                           NXOpen.AttributePropertiesBuilder.OperationType.NotSet)
            if sender == self.button01:
                attributes = {
                    "DRW_title": self.string04.Value,
                    "DRW_doc_name": self.string06.Value,
                    "DRW_prod_material": self.convertProductMaterial,
                    "DRW_prod_material_": self.string21.Value,
                    "DRW_litera": "{0}{1}".format(self.enum01.ValueAsString, self.enum04.ValueAsString),
                    "DRW_litera_letter": self.enum01.ValueAsString,
                    "DRW_litera_index": self.enum04.ValueAsString,
                    "DRW_prod_weight": self.string20.Value,
                    "DRW_change_sheet": self.checkPartRevisionChanges,
                    "DRW_directive_ref": self.string16.Value,
                    "DRW_owner": self.string15.Value,
                    "DRW_check_user": self.string14.Value,
                    "DRW_TK": self.string13.Value,
                    "DRW_Grafa_10": self.string12.Value,
                    "DRW_Lider": self.string11.Value,
                    "DRW_NK": self.string07.Value,
                    "DRW_approve_user": self.string10.Value,
                    "DRW_first_used": self.string08.Value,
                    "DRW_format": self.getLeaderSheetFormat,
                    "DRW_first_page": self.moreThanOneSheet,
                    "DRW_A4_amt": self.calculateFormatArea
                }
            else:
                attributes = {
                    "DRW_first_page": self.moreThanOneSheet,
                    "DRW_format": self.getLeaderSheetFormat,
                    "DRW_A4_amt": self.calculateFormatArea,
                    "DRW_change_sheet": self.checkPartRevisionChanges
                }
                sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
                drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                    sheet)
                isFirstSheet = int(drawingSheetBuilder.Number) == 1
                isEditCurrentSheet = not(self.toggle03.Value)
                drawingSheetBuilder.Destroy()
                if isFirstSheet and isEditCurrentSheet:
                    attributes["DRW_scale"] = self.enum05.ValueAsString
                else:
                    pass
            for key, val in attributes.items():
                try:
                    attributePropertiesBuilder.Title = key
                    attributePropertiesBuilder.DataType = NXOpen.AttributePropertiesBaseBuilder.DataTypeOptions.String
                    if isinstance(attributes[key], str):
                        attributePropertiesBuilder.StringValue = attributes[key]
                    else:
                        attributePropertiesBuilder.StringValue = attributes[key](
                        )
                    dictToCache[key] = attributePropertiesBuilder.StringValue
                    attributePropertiesBuilder.CreateAttribute()
                except:
                    continue
            attributePropertiesBuilder.Commit()
            attributePropertiesBuilder.Destroy()
            if sender == self.button01:
                self.writeCacheFile(dictToCache)
                self.session_ui.NXMessageBox.Show(
                    self.moduleName, self.MSG_Info, "Атрибуты успешно обновлены!")
        except Exception as ex:
            if not (attributePropertiesBuilder is None):
                attributePropertiesBuilder.Destroy()
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkPartRevisionChanges(self):
        try:
            attrib = self.work_part.GetStringAttribute("DB_PART_REV")
            try:
                rev = re.match(r"[\d]{1,}", attrib).group(0)
                if int(rev) == 1:
                    return "-"
                else:
                    return "Зам."
            except:
                rev = re.match(r"[a-zA-Zа-яА-Я]{1,}", attrib).group(0)
                if len(rev) > 1:
                    return "-"
                elif rev in ["A", "А"]:
                    return "-"
                else:
                    return "Зам."
            else:
                return "-"
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkBaseModelWeight(self):  # работает только для одного линка
        if self.rtComp == 0:
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Error, "В чертеже отсутствует базовая модель")
            return None
        try:
            componentObjects = self.reportComponentChildren(self.rtComp, [])
            mass = ""
            if componentObjects.__len__() == 0:
                for name in ["NX_Mass"]:
                    try:
                        mass = self.work_part.GetStringAttribute(name)
                        if round(float(mass), 6) != 0.000000:
                            roundMass = self.massPowerRound(mass, 3)
                    except:
                        pass
            else:
                for item in componentObjects:
                    try:
                        massPropertiesBuilder = self.work_part.PropertiesManager.CreateMassPropertiesBuilder([
                                                                                                            item])
                        massPropertiesBuilder.UpdateNow()
                        mass = self.session_uf.Weight.AskProps(
                            item.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM).Mass
                        massPropertiesBuilder.Destroy()
                        if round(float(mass), 6) != 0.000000:
                            roundMass = self.massPowerRound(mass, 3)
                    except:
                        pass
            return str(roundMass)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def massPowerRound(self, mass, precision):
        try:
            mass = float(mass)
            factor = math.pow(10, precision)
            mass = abs(math.floor(-mass * factor) / factor)
            return str(mass)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def checkBaseModelMaterial(self):
        if self.rtComp == 0:
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Error, "В чертеже отсутствует базовая модель")
            return None
        try:
            material = ""
            componentObjects = self.reportComponentChildren(self.rtComp, [])
            if componentObjects.__len__() == 0:
                try:
                    return self.work_part.GetStringAttribute("NX_Material")
                except:
                    return material
            else:
                for item in componentObjects:
                    try:
                        return item.GetStringAttribute("NX_Material")
                    except Exception as ex:
                        return material
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def reportComponentChildren(self, component, rcc_compList):
        try:
            try:
                componentChildren = component.GetChildren()
            except:
                return rcc_compList
            if len(componentChildren) != 0:
                for item in componentChildren:
                    try:
                        if item.IsSuppressed:
                            rcc_compList.append(item)
                        elif len(item.GetChildren()) != 0:
                            rcc_compList.append(item)
                            self.reportComponentChildren(item, rcc_compList)
                        else:
                            rcc_compList.append(item)
                    except Exception as ex:
                        raise ex
                return rcc_compList
            else:
                return rcc_compList
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def resizeCurrentSheet(self, drawingSheetBuilder):
        try:
            templateName = self.enum0.GetProperties().GetEnum("Value")
            serialName = 'second' if self.moreThanOneSheet else 'first'
            orientation = 'v' if self.isVertical else 'h'
            query = """select height_, width_ from templates_
						 where enum_value_ = {0} 
						 and orientation_ like \"{1}\"
						 and serial_name_ like \"{2}\"""".format(templateName, orientation, serialName)
            response = self.sendBaseQuery(query)[0]
            _h, _w = response[0], response[1]
            drawingSheetBuilder.Option = NXOpen.Drawings.DrawingSheetBuilder.SheetOption.CustomSize
            try:
                drawingSheetBuilder.Height = _h
                drawingSheetBuilder.Length = _w
            except Exception as ex:
                drawingSheetBuilder.Height = self.work_part.DrawingSheets.CurrentDrawingSheet.Height
                drawingSheetBuilder.Length = self.work_part.DrawingSheets.CurrentDrawingSheet.Length
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def askWorkPartGroups(self, tmpGrpTag=0):
        try:
            self.workPartGroups = []
            while True:
                tmpGrpTag = self.session_uf.Obj.CycleObjsInPart(
                    self.work_part.Tag, NXOpen.UF.UFConstants.UF_group_type, tmpGrpTag)
                if tmpGrpTag == 0:
                    break
                else:
                    myGroup = NXOpen.TaggedObjectManager.GetTaggedObject(
                        tmpGrpTag)
                    self.workPartGroups.append(myGroup)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def editCurrentSheet(self):
        try:
            drawingSheetBuilder = None
            sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                sheet)
            self.deleteChainedGroup(sheet)
            self.resizeCurrentSheet(drawingSheetBuilder)
            drawingSheetBuilder.Commit()
            drawingSheetBuilder.Destroy()
            self.importTemplate(sheet)
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Info, "Текущий лист успешно изменен")
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def findChainedGroup(self, sheet):
        try:
            chained_groups = []
            sheet.Open()
            view = sheet.View
            view.Fit()
            viewGroups = [item for item in view.AskVisibleObjects(
            ) if isinstance(item, NXOpen.Group)]
            [chained_groups.append(item) for item in viewGroups if not(
                re.search(r"Format", item.GetStringAttribute("DB_PART_MFKID")) is None)]
            if len(chained_groups) == 0:
                return None
            else:
                return chained_groups[0]  # упадет на пустом листе
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def deleteChainedGroup(self, sheet):
        try:
            builder_group = None
            group = self.findChainedGroup(sheet)
            if group is None:
                return None
            else:
                pass
            builder_group = self.work_part.CreateGatewayGroupBuilder(group)
            builder_group.ActionType = 4
            builder_group.Commit()
            builder_group.Destroy()
            markId1 = self.session.SetUndoMark(
                NXOpen.Session.MarkVisibility.Visible, "Delete")
            self.session.UpdateManager.AddToDeleteList([group])
            self.session.Preferences.Modeling.NotifyOnDelete
            self.session.UpdateManager.DoUpdate(markId1)
            self.session.UpdateManager.ClearDeleteList()
        except Exception as ex:
            if not (builder_group is None):
                builder_group.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def editChainedGroupName(self, sheet):
        try:
            builder_group = None
            group = self.findChainedGroup(sheet)
            if group is None:
                return None
            else:
                pass
            builder_group = self.work_part.CreateGatewayGroupBuilder(group)
            builder_group.ActionType = 4
            if re.search(r"_ЛИСТ\s[0]{0,}\d", builder_group.GroupName) is None:
                builder_group.GroupName = "{0}_{1}".format(
                    builder_group.GroupName, sheet.Name)
            else:
                builder_group.GroupName = re.sub(
                    r"_ЛИСТ [0]{0,}\d", "_{0}".format(sheet.Name), builder_group.GroupName)
            builder_group.Commit()
            builder_group.Destroy()
        except Exception as ex:
            if not (builder_group is None):
                builder_group.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def appendNewSheet(self):
        try:
            drawingSheetBuilder = None
            drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                NXOpen.Drawings.DrawingSheet.Null)
            self.resizeCurrentSheet(drawingSheetBuilder)
            sheetNumber = len(list(self.work_part.DrawingSheets)) + 1
            if len(str(sheetNumber)) > 1:
                sheetName = "Лист {0}".format(sheetNumber)
            else:
                sheetName = "Лист 0{0}".format(sheetNumber)
            drawingSheetBuilder.Number = str(sheetNumber)
            drawingSheetBuilder.Name = sheetName
            sheet = drawingSheetBuilder.Commit()
            drawingSheetBuilder.Destroy()
            self.importTemplate(sheet)
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Info, "Добавлен новый лист {0}".format(sheetName))
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def updateNumeratedDrawingSheetCollection(self):
        try:
            drawingSheetBuilder = None
            if len(list(self.work_part.DrawingSheets)) == 0:
                return None
            else:
                self.enumerated_drawing_sheets = {}
                for sheet in self.work_part.DrawingSheets:
                    drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                        sheet)
                    self.enumerated_drawing_sheets[int(
                        drawingSheetBuilder.Number)] = sheet
                    drawingSheetBuilder.Destroy()
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def recalculateZoneMarkUps(self):
        try:
            builder_drafting_note = None
            started_sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            if len(list(self.work_part.DrawingSheets)) == 0 or started_sheet is None:
                return None
            else:
                self.updateNumeratedDrawingSheetCollection()
                zone_number = 1
                sorted_keys = sorted(list(self.enumerated_drawing_sheets))
                for key in sorted_keys:
                    sheet = self.enumerated_drawing_sheets[key]
                    sheet.Open()
                    view_drafting = sheet.View
                    notes = [item for item in view_drafting.AskVisibleObjects(
                    ) if isinstance(item, NXOpen.Annotations.Note)]
                    sortedNotes = sorted(notes, key=lambda note: note.Name)
                    uniqueZoneNames = sorted(
                        set([item.Name for item in sortedNotes if "ZONE_" in item.Name]))
                    for uniqueName in uniqueZoneNames:
                        for note in sortedNotes:
                            if uniqueName in note.Name:
                                builder_drafting_note = self.work_part.Annotations.CreateDraftingNoteBuilder(
                                    note)
                                text = "".join(
                                    builder_drafting_note.Text.GetEditorText())
                                builder_drafting_note.Text.SetEditorText([re.sub(
                                    r"(<F\d{1,}>){0,}\d{1,}(<F>){0,}|<F\d{1,}><F>", "<F8>{0}<F>".format(zone_number), text)])
                                builder_drafting_note.Commit()
                                builder_drafting_note.Destroy()
                            else:
                                pass
                        zone_number += 1
            started_sheet.Open()
        except Exception as ex:
            if not (builder_drafting_note is None):
                builder_drafting_note.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def importTemplate(self, sheet):
        try:
            drawingSheetBuilder = None
            partImporter = None
            orientation = 'v' if self.isVertical else 'h'
            templateName = self.enum0.GetProperties().GetEnum("Value")
            if not(sheet is None):
                drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                    sheet)
                shNum = int(drawingSheetBuilder.Number)
                serialName = 'second' if shNum > 1 else 'first'
                drawingSheetBuilder.Destroy()
            elif len(list(self.work_part.DrawingSheets)) > 1:
                serialName = 'second'
            else:
                serialName = 'first'
            query = """select template_id_ 
						from templates_ where enum_value_ = {0}
						and serial_name_ like \"{1}\"
						and orientation_ like \"{2}\"""".format(templateName, serialName, orientation)
            response = self.sendBaseQuery(query)[0]
            name = response[0]
            partImporter = self.work_part.ImportManager.CreatePartImporter()
            partImporter.FileName = "@DB/{0}/A".format(name)
            partImporter.Scale = 1.0
            partImporter.CreateNamedGroup = True
            partImporter.ImportViews = False
            partImporter.ImportCamObjects = False
            partImporter.LayerOption = NXOpen.PartImporter.LayerOptionType.Original
            partImporter.DestinationCoordinateSystemSpecification = NXOpen.PartImporter.DestinationCoordinateSystemSpecificationType.Work
            matrix = NXOpen.Matrix3x3()
            matrix.Xx, matrix.Xy, matrix.Xz = 1.0, 0.0, 0.0
            matrix.Yx, matrix.Yy, matrix.Yz = 0.0, 1.0, 0.0
            matrix.Zx, matrix.Zy, matrix.Zz = 0.0, 0.0, 1.0
            nXMatrix = self.work_part.NXMatrices.Create(matrix)
            partImporter.DestinationCoordinateSystem = nXMatrix
            destinationPoint = NXOpen.Point3d(0.0, 0.0, 0.0)
            partImporter.DestinationPoint = destinationPoint
            partImporter.Commit()
            partImporter.Destroy()
            stateArray = [None] * 2
            stateArray[0] = NXOpen.Layer.StateInfo(
                256, NXOpen.Layer.State.Selectable)
            stateArray[1] = NXOpen.Layer.StateInfo(
                256, NXOpen.Layer.State.Visible)
            self.work_part.Layers.ChangeStates(stateArray, False)
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            if not (partImporter is None):
                partImporter.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))


def main():
    try:
        formats = None
        formats = Formats()
        if formats.is_valid_template_database:
            pass
        else:
            formats.Dispose()
            return None
        if formats.checkIsDrafting():
            formats.Show()
        else:
            formats.Dispose()
    except Exception as ex:
        NXOpen.UI.GetUI().NXMessageBox.Show("Редактор чертежных форматов",
                                            NXOpen.NXMessageBox.DialogType.Error, str(ex))
    finally:
        formats.Dispose()


if __name__ == "__main__":
    main()
List.append(item)
                            self.reportComponentChildren(item, rcc_compList)
                        else:
                            rcc_compList.append(item)
                    except Exception as ex:
                        raise ex
                return rcc_compList
            else:
                return rcc_compList
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def resizeCurrentSheet(self, drawingSheetBuilder):
        try:
            templateName = self.enum0.GetProperties().GetEnum("Value")
            serialName = 'second' if self.moreThanOneSheet else 'first'
            orientation = 'v' if self.isVertical else 'h'
            query = """select height_, width_ from templates_
						 where enum_value_ = {0} 
						 and orientation_ like \"{1}\"
						 and serial_name_ like \"{2}\"""".format(templateName, orientation, serialName)
            response = self.sendBaseQuery(query)[0]
            _h, _w = response[0], response[1]
            drawingSheetBuilder.Option = NXOpen.Drawings.DrawingSheetBuilder.SheetOption.CustomSize
            try:
                drawingSheetBuilder.Height = _h
                drawingSheetBuilder.Length = _w
            except Exception as ex:
                drawingSheetBuilder.Height = self.work_part.DrawingSheets.CurrentDrawingSheet.Height
                drawingSheetBuilder.Length = self.work_part.DrawingSheets.CurrentDrawingSheet.Length
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def askWorkPartGroups(self, tmpGrpTag=0):
        try:
            self.workPartGroups = []
            while True:
                tmpGrpTag = self.session_uf.Obj.CycleObjsInPart(
                    self.work_part.Tag, NXOpen.UF.UFConstants.UF_group_type, tmpGrpTag)
                if tmpGrpTag == 0:
                    break
                else:
                    myGroup = NXOpen.TaggedObjectManager.GetTaggedObject(
                        tmpGrpTag)
                    self.workPartGroups.append(myGroup)
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def editCurrentSheet(self):
        try:
            drawingSheetBuilder = None
            sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                sheet)
            self.deleteChainedGroup(sheet)
            self.resizeCurrentSheet(drawingSheetBuilder)
            drawingSheetBuilder.Commit()
            drawingSheetBuilder.Destroy()
            self.importTemplate(sheet)
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Info, "Текущий лист успешно изменен")
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def findChainedGroup(self, sheet):
        try:
            chained_groups = []
            sheet.Open()
            view = sheet.View
            view.Fit()
            viewGroups = [item for item in view.AskVisibleObjects(
            ) if isinstance(item, NXOpen.Group)]
            [chained_groups.append(item) for item in viewGroups if not(
                re.search(r"Format", item.GetStringAttribute("DB_PART_MFKID")) is None)]
            if len(chained_groups) == 0:
                return None
            else:
                return chained_groups[0]  # упадет на пустом листе
        except Exception as ex:
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def deleteChainedGroup(self, sheet):
        try:
            builder_group = None
            group = self.findChainedGroup(sheet)
            if group is None:
                return None
            else:
                pass
            builder_group = self.work_part.CreateGatewayGroupBuilder(group)
            builder_group.ActionType = 4
            builder_group.Commit()
            builder_group.Destroy()
            markId1 = self.session.SetUndoMark(
                NXOpen.Session.MarkVisibility.Visible, "Delete")
            self.session.UpdateManager.AddToDeleteList([group])
            self.session.Preferences.Modeling.NotifyOnDelete
            self.session.UpdateManager.DoUpdate(markId1)
            self.session.UpdateManager.ClearDeleteList()
        except Exception as ex:
            if not (builder_group is None):
                builder_group.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def editChainedGroupName(self, sheet):
        try:
            builder_group = None
            group = self.findChainedGroup(sheet)
            if group is None:
                return None
            else:
                pass
            builder_group = self.work_part.CreateGatewayGroupBuilder(group)
            builder_group.ActionType = 4
            if re.search(r"_ЛИСТ\s[0]{0,}\d", builder_group.GroupName) is None:
                builder_group.GroupName = "{0}_{1}".format(
                    builder_group.GroupName, sheet.Name)
            else:
                builder_group.GroupName = re.sub(
                    r"_ЛИСТ [0]{0,}\d", "_{0}".format(sheet.Name), builder_group.GroupName)
            builder_group.Commit()
            builder_group.Destroy()
        except Exception as ex:
            if not (builder_group is None):
                builder_group.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def appendNewSheet(self):
        try:
            drawingSheetBuilder = None
            drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                NXOpen.Drawings.DrawingSheet.Null)
            self.resizeCurrentSheet(drawingSheetBuilder)
            sheetNumber = len(list(self.work_part.DrawingSheets)) + 1
            if len(str(sheetNumber)) > 1:
                sheetName = "Лист {0}".format(sheetNumber)
            else:
                sheetName = "Лист 0{0}".format(sheetNumber)
            drawingSheetBuilder.Number = str(sheetNumber)
            drawingSheetBuilder.Name = sheetName
            sheet = drawingSheetBuilder.Commit()
            drawingSheetBuilder.Destroy()
            self.importTemplate(sheet)
            self.session_ui.NXMessageBox.Show(
                self.moduleName, self.MSG_Info, "Добавлен новый лист {0}".format(sheetName))
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def updateNumeratedDrawingSheetCollection(self):
        try:
            drawingSheetBuilder = None
            if len(list(self.work_part.DrawingSheets)) == 0:
                return None
            else:
                self.enumerated_drawing_sheets = {}
                for sheet in self.work_part.DrawingSheets:
                    drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                        sheet)
                    self.enumerated_drawing_sheets[int(
                        drawingSheetBuilder.Number)] = sheet
                    drawingSheetBuilder.Destroy()
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def recalculateZoneMarkUps(self):
        try:
            builder_drafting_note = None
            started_sheet = self.work_part.DrawingSheets.CurrentDrawingSheet
            if len(list(self.work_part.DrawingSheets)) == 0 or started_sheet is None:
                return None
            else:
                self.updateNumeratedDrawingSheetCollection()
                zone_number = 1
                sorted_keys = sorted(list(self.enumerated_drawing_sheets))
                for key in sorted_keys:
                    sheet = self.enumerated_drawing_sheets[key]
                    sheet.Open()
                    view_drafting = sheet.View
                    notes = [item for item in view_drafting.AskVisibleObjects(
                    ) if isinstance(item, NXOpen.Annotations.Note)]
                    sortedNotes = sorted(notes, key=lambda note: note.Name)
                    uniqueZoneNames = sorted(
                        set([item.Name for item in sortedNotes if "ZONE_" in item.Name]))
                    for uniqueName in uniqueZoneNames:
                        for note in sortedNotes:
                            if uniqueName in note.Name:
                                builder_drafting_note = self.work_part.Annotations.CreateDraftingNoteBuilder(
                                    note)
                                text = "".join(
                                    builder_drafting_note.Text.GetEditorText())
                                builder_drafting_note.Text.SetEditorText([re.sub(
                                    r"(<F\d{1,}>){0,}\d{1,}(<F>){0,}|<F\d{1,}><F>", "<F8>{0}<F>".format(zone_number), text)])
                                builder_drafting_note.Commit()
                                builder_drafting_note.Destroy()
                            else:
                                pass
                        zone_number += 1
            started_sheet.Open()
        except Exception as ex:
            if not (builder_drafting_note is None):
                builder_drafting_note.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))

    def importTemplate(self, sheet):
        try:
            drawingSheetBuilder = None
            partImporter = None
            orientation = 'v' if self.isVertical else 'h'
            templateName = self.enum0.GetProperties().GetEnum("Value")
            if not(sheet is None):
                drawingSheetBuilder = self.work_part.DrawingSheets.DrawingSheetBuilder(
                    sheet)
                shNum = int(drawingSheetBuilder.Number)
                serialName = 'second' if shNum > 1 else 'first'
                drawingSheetBuilder.Destroy()
            elif len(list(self.work_part.DrawingSheets)) > 1:
                serialName = 'second'
            else:
                serialName = 'first'
            query = """select template_id_ 
						from templates_ where enum_value_ = {0}
						and serial_name_ like \"{1}\"
						and orientation_ like \"{2}\"""".format(templateName, serialName, orientation)
            response = self.sendBaseQuery(query)[0]
            name = response[0]
            partImporter = self.work_part.ImportManager.CreatePartImporter()
            partImporter.FileName = "@DB/{0}/A".format(name)
            partImporter.Scale = 1.0
            partImporter.CreateNamedGroup = True
            partImporter.ImportViews = False
            partImporter.ImportCamObjects = False
            partImporter.LayerOption = NXOpen.PartImporter.LayerOptionType.Original
            partImporter.DestinationCoordinateSystemSpecification = NXOpen.PartImporter.DestinationCoordinateSystemSpecificationType.Work
            matrix = NXOpen.Matrix3x3()
            matrix.Xx, matrix.Xy, matrix.Xz = 1.0, 0.0, 0.0
            matrix.Yx, matrix.Yy, matrix.Yz = 0.0, 1.0, 0.0
            matrix.Zx, matrix.Zy, matrix.Zz = 0.0, 0.0, 1.0
            nXMatrix = self.work_part.NXMatrices.Create(matrix)
            partImporter.DestinationCoordinateSystem = nXMatrix
            destinationPoint = NXOpen.Point3d(0.0, 0.0, 0.0)
            partImporter.DestinationPoint = destinationPoint
            partImporter.Commit()
            partImporter.Destroy()
            stateArray = [None] * 2
            stateArray[0] = NXOpen.Layer.StateInfo(
                256, NXOpen.Layer.State.Selectable)
            stateArray[1] = NXOpen.Layer.StateInfo(
                256, NXOpen.Layer.State.Visible)
            self.work_part.Layers.ChangeStates(stateArray, False)
        except Exception as ex:
            if not (drawingSheetBuilder is None):
                drawingSheetBuilder.Destroy()
            if not (partImporter is None):
                partImporter.Destroy()
            self.session_ui.NXMessageBox.Show(self.moduleName, self.MSG_Error,
                                         self.errorTemplate.substitute(function=inspect.stack()[0][3], ex=ex))


def main():
    try:
        formats = None
        formats = Formats()
        if formats.is_valid_template_database:
            pass
        else:
            formats.Dispose()
            return None
        if formats.checkIsDrafting():
            formats.Show()
        else:
            formats.Dispose()
    except Exception as ex:
        NXOpen.UI.GetUI().NXMessageBox.Show("Редактор чертежных форматов",
                                            NXOpen.NXMessageBox.DialogType.Error, str(ex))
    finally:
        formats.Dispose()


if __name__ == "__main__":
    main()

import NXOpen
import NXOpen.UF
import NXOpen.Assemblies
import NXOpen.Features
import NXOpen.GeometricAnalysis
import NXOpen.GeometricUtilities
import NXOpen.Layer
import re, math
import json
import time as tt
import datetime as dt
import codecs
import itertools
import collections
import subprocess
import sys, os

# return statement for simple check
# return joined conclusion for complex check

class AKS_checker_application:
	def __init__(self):
		self.theSession = NXOpen.Session.GetSession()
		self.theUI = NXOpen.UI.GetUI()
		self.theUF = NXOpen.UF.UFSession.GetUFSession()
		self.lw = self.theSession.ListingWindow
		self.workPart = self.theSession.Parts.Work
		self.displayPart = self.theSession.Parts.Display
		self.rtComp = self.workPart.ComponentAssembly.RootComponent
		self.version = "v0.1.7"
		self.theSessionPath = self.theSession.ExecutingJournal
		self.configurationFile = self.theSessionPath.replace(".py",".asb")#.encode("utf-8").decode("cp1251")
		self.configuration = None

	def loadConfig(self, path):
		try:
			with open(path) as config:
				self.configuration = json.load(config)
				return True
		except:
			raise
			return False

	def checkPreviewMode(self, ):
		try:
			preview = self.workPart.PartPreviewMode
			previewMode = eval(self.configuration["samplePreviewMode"])
			if preview == previewMode : return True
			else: return "Проверка режима предварительного просмотра: режим выбран не верно"
		except Exception as ex:
			return ("checkPreviewMode failed qwith {0}".format(ex))
	
	def checkRenderingStyle(self, ):
		try:
			viewList = []
			for view in self.workPart.ModelingViews:
				renderingStyle = eval(self.configuration["sampleRenderingStyle"])
				if view.RenderingStyle == renderingStyle: continue
				else: viewList.append(view.Name)
			if len(viewList) == 0: return True
			else: 
				return "Проверка закраски видов: Закраска видов не соответствует требованиям: {0}".format(" | ".join(viewList))
		except Exception as ex:
			return ("checkRenderingStyle failed with {0}".format(ex))
	
	def checkWCSOrientation(self):
		try:
			conclusion = []
			origin = self.configuration["sampleOrigin"]
			rotation = self.configuration["sampleRotation"]
			cwo_WCSOrigin = self.workPart.WCS.CoordinateSystem.Origin
			cwo_WCSRotationMatrix = self.workPart.WCS.CoordinateSystem.Orientation
			cwo_passOrigin = [cwo_WCSOrigin.X,cwo_WCSOrigin.Y,cwo_WCSOrigin.Z] == origin
			cwo_passRotation = [cwo_WCSRotationMatrix.Element.Xx,
							cwo_WCSRotationMatrix.Element.Yy,
							cwo_WCSRotationMatrix.Element.Zz] == rotation
			if cwo_passOrigin: pass
			else: conclusion.append("Проверка ориентации РСК: РСК была перемещена.")
			if cwo_passRotation: pass
			else: conclusion.append("Проверка ориентации РСК: РСК отклонена от АСК.")
			if len(conclusion) != 0: return "\n".join(conclusion)
			else: return True
		except Exception as ex:
			return ("checkWCSOrientation failed with {0}".format(ex))
	
	def checkWCSVisibility(self):
		try:
			if self.workPart.WCS.Visibility: return "Проверка видимости РСК: Отображение РСК включено"
			else: return True
		except Exception as ex:
			return ("checkWCSVisibility failed with {0}".format(ex))

	def checkNameAndId(self):
		try:
			nameToCheck = self.workPart.GetStringAttribute("DB_PART_NAME")
			idToCheck = self.workPart.GetStringAttribute("DB_PART_NO")
			trName = self.translateName(nameToCheck)
			if trName == idToCheck: return True
			else: return "Проверка имени и идентификатора: Имя и идентификатор не идентичны"
		except Exception as ex:
			return ("checkNameAndId failed with {0}".format(ex))

	def translateName(self, name):
		trName = []
		gost7_79_2000Replacements = {
			"а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"jo",
	  		"ж":"zh","з":"z","и":"i","й":"J","к":"k","л":"l","м":"m","н":"n",
	  		"о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"x",
	  		"ц":"c","ч":"ch","ш":"sh","щ":"shh","ъ":"","ы":"y","ь":"","э":"e",
	  		"ю":"yu","я":"ya", "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"JO",
	  		"Ж":"ZH","З":"Z","И":"I","Й":"J","К":"K","Л":"L","М":"M","Н":"N",
	  		"О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F","Х":"X",
	  		"Ц":"C","Ч":"CH","Ш":"SH","Щ":"SHH","Ъ":"","Ы":"Y","Ь":"","Э":"E",
	  		"Ю":"YU","Я":"YA","\\":"-"," " :"-","/":"_",":":"-","<":"-",">":"-",
			"~":"-","*":"x","\"":"''",".":".",",":",",";":";","%":"%","(":"(",
			")":")","-":"-","_":"_","=":"=","+":"+","#":"#","&":"&","{":"{",
			"}":"}","[":"[","]":"]","'":"'"," ":" ","±":"+-","Ø":"o","°":'',
			"¼":"1-4","½":"1-2","¾":"3-4","№":"#"}
		for ch in name:
			if re.search(r"[a-zA-Z]", ch) is not None: trName.append(ch)
			elif re.search(r"[а-яА-Я]", ch) is not None: trName.append(gost7_79_2000Replacements[ch])
			elif re.search(r"\d", ch) is not None: trName.append(ch)
			else:
				try: trName.append(gost7_79_2000Replacements[ch])
				except: trName.append("▲")
		return "".join(trName)
	
	def checkExtendedViews(self):
		try:
			viewsStandardLib = ["Top","Front","Right","Back","Bottom","Left","Isometric","Trimetric"]
			viewsExtendedList = [item.Name for item in self.workPart.ModelingViews if not(item.Name in viewsStandardLib)]
			if len(viewsExtendedList) == 0: return True
			else: return "проверка наличия доп. видов: ЭМ содержит доп. виды: {0}".format(" | ".join(viewsExtendedList))
		except Exception as ex:
			return ("checkExtendedViews failed with {0}".format(ex))

	def checkWorkView(self):
		try:
			workView = self.configuration["sampleWorkView"]
			view = self.workPart.Views.WorkView
			if view.Name == workView: return True
			else: return "Проверка выбора рабочего вида: Рабочий вид выбран не верно"
		except Exception as ex:
			return ("checkWorkView failed with {0}".format(ex))

	def checkPmiOnViews(self):
		try:
			statementIsAnyNotes = len(list(self.workPart.Notes)) != 0
			statementIsAnyPMIs = len(list(self.workPart.PmiManager.Pmis)) != 0
			if statementIsAnyNotes or statementIsAnyPMIs: return "Проверка наличия информации на видах: виды содержат доп.информацию"
			else: return True			
		except Exception as ex:
			return ("checkPmiOnViews failed with {0}".format(ex))
	
	def checkAnyDrawings(self):
		try:
			if len(self.workPart.DrawingSheets) == 0: return True
			else: return "Проверка наличия чертежных листов: ЭМ содержит чертежные листы"
		except Exception as ex:
			return ("checkAnyDrawings failed with {0}".format(ex))

	def checkFileCompressionOnSaving(self):
		try:
			if self.workPart.SaveOptions.CompressPart : return True
			else: return "Проверка сжатия детали: деталь не сжимается при сохранении"
		except Exception as ex:
			return ("checkFileCompressionOnSaving failed with {0}".format(ex))
	
	def checkApplicationOnSaving(self):
		try:
			appllicationSet = self.configuration["sampleApllicationsSet"]
			if self.theSession.ApplicationName in appllicationSet: return True
			else: return "Проверка приложения детали: деталь сохранена в недопустимом приложении"
		except Exception as ex:
			return ("checkApplicationOnSaving failed with {0}".format(ex))

	def _getListFlat(self,glf_list):
		try:
			glf_flatList = []
			for item in glf_list:
				if isinstance(item, collections.Iterable):
					self._getListFlat(item)
				else: glf_flatList.append(item)
			return glf_flatList
		except Exception as ex:
			return ("_getListFlat failed with {0}".format(ex))

	def checkModelSections(self):
		try:
			if len(list(self.workPart.DynamicSections)) != 0: 
				dynamicSections = [item.Name for item in self.workPart.DynamicSections]
				return "ЭМ содержит рабочие сечения:%s" %("\n".join(dynamicSections))
			else: return True
		except Exception as ex:
			return ("checkModelSections %s" %ex)

	def checkHiddenComponents(self):
		if self.rtComp in [0,None]: return True
		try:
			chc_componentObjects = self._reportComponentChildren(self.rtComp,[self.rtComp]) 
			hidenObjects = [item.DisplayName for item in chc_componentObjects if item.IsBlanked]
			if len(hidenObjects) == 0: return True
			else: return "ЭМ содержит скрытые объекты:\n%s" %("\n".join(hidenObjects))
		except Exception as ex:
			return ("checkHiddenComponents failed with {0}".format(ex))

	def checkSuppressedObjects(self):
		if self.rtComp in  [0, None]: return True
		try:
			cso_list = []
			cso_componentObjects = self._reportComponentChildren(self.rtComp,[self.rtComp])
			for item in cso_componentObjects:
				if item.IsSuppressed:
					cso_attributesList = [item.Title for item in item.GetAttributeTitlesByType(NXOpen.NXObjectAttributeType.String)]
					if "REFERENCE_COMPONENT" in cso_attributesList:	continue
					else:
						parent = item.Parent
						cso_list.append("%s (%s)" %(item.DisplayName, parent.DisplayName))
						continue
				else: pass
			cso_list = set(cso_list) # почему?!
			if len(cso_list) == 0: return True
			elif len(cso_list) > 1:	cso_string = "ЭМ содержит подавленные объекты:\n%s" %("\n".join(cso_list))
			else: pass
			return cso_string
		except Exception as ex:
			return ("checkSuppressedObjects failed with: %s" %ex)

	def _reportComponentChildren(self,rcc_comp,rcc_compList):
		try: rcc_componentChildren = rcc_comp.GetChildren()
		except: return rcc_compList
		if len(rcc_componentChildren) != 0:
			for item in rcc_componentChildren:
				try:
					if item.IsSuppressed: rcc_compList.append(item)
					elif len(item.GetChildren()) != 0:
						rcc_compList.append(item)
						self._reportComponentChildren(item,rcc_compList)
					else: rcc_compList.append(item)
				except Exception as ex:
					return ("_reportComponentChildren failed with {0}".format(ex))
			return rcc_compList	
		else: return rcc_compList

	def checkUnparameterizedBodies(self):
		try:
			unparameterizedBodies = []
			if len(self.workPart.Features.GetFeatures()) != 0:
				for feature in self.workPart.Features:
					if isinstance(feature,NXOpen.Features.Brep):
						unparameterizedBodies.append("{0} - {1}".format(feature.Name, feature.JournalIdentifier))
				if len(unparameterizedBodies) == 0: return True
				else: return  "Проверка наличия непараметризованных тел: ЭМ содержит непараметризованные тела:\n{0}".format("\n".join(unparameterizedBodies))
			else: return  True 
		except Exception as ex:
			return ("checkUnparameterizedBodies failed with {0}".format(ex))

	def isComponentLinked(self):
		if self.rtComp in [0,None]: componentObjects = [self.workPart]
		else: componentObjects = self._reportComponentChildren(self.rtComp,[self.rtComp])
		for item in componentObjects: pass
			#######################################

	def checkWaveLinks(self):
		try:
			linkedBodies = [item for item in self.workPart.Features if "LINKED" in item.FeatureType]
			brokenLinks = [item.GetFeatureName() for item in linkedBodies if self.theUF.Wave.IsLinkBroken(item.Tag) ]	
			if len(brokenLinks) == 0: return True
			else: return "WAVE связи разорваны для тел:\n{0}".format(",\n".join(brokenLinks))
		except Exception as ex:
			return ("checkWaveLinks failed with {0}".format(ex))

	def checkItemType(self):
		try:
			_type = self.configuration["objectType"]
			partType = self.workPart.GetStringAttribute("DB_PART_TYPE")
			if partType == _type: return True
			else: return "Проверка типа объекта: Тип объекта не соответствует {0}".format(_type)
		except Exception as ex:
			return ("checkItemType failed with: %s" %ex)

	def checkWeightStatement(self): 
		if self.rtComp in [0,None]: componentObjects = [self.workPart]
		else: componentObjects = self._reportComponentChildren(self.rtComp,[self.rtComp])
		try:
			outList = []
			for item in componentObjects:
				cws_massProps = self.theUF.Weight.AskProps(item.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM)
				if cws_massProps.CacheState == NXOpen.UF.Weight.StateType.CACHED: pass #return True
				elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.NO_CACHE:
					try: outList.append("Проверка состояния массы: Состояние массы %s: Расчет массы не актуальный" %item.DisplayName)
					except: outList.append("Проверка состояния массы: Состояние массы %s: Расчет массы не актуальный" %item.Name)
				elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.ASSERTED:
					try: outList.append("Проверка состояния массы: Состояние массы %s: Масса назначена вручную" %item.DisplayName)
					except: outList.append("Проверка состояния массы: Состояние массы %s: Масса назначена вручную" %item.Name)
				elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.IMPLIED: pass
				elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.INHERITED: pass 
				elif cws_massProps.CacheState == NXOpen.UF.Weight.StateType.UNKNOWN: pass
			if len(outList) == 0: return True
			else: return "\n".join(outList)
		except Exception as ex:
			return ("checkWeightStatement failed with {0}".format(ex))

	def checkDirectModelCreationMode(self):
		try:
			if self.theSession.Parts.SaveOptions.VisualizationData: return True
			else: return "Проверка создания JT представления: JT представление не создается при сохранении"
		except Exception as ex:
			return ("checkDirectModelCreationMode failed with {0}".format(ex ))

	def checkWeightProps(self):
		if self.rtComp in [0,None]: cwp_componentObjects = [self.workPart]
		else: cwp_componentObjects = self._reportComponentChildren(self.rtComp,[self.rtComp])
		try:
			cwp_list = []
			for item in cwp_componentObjects:
				if isinstance(item, NXOpen.Part):
					cwp_weightProps = self.theUF.Weight.AskProps(item.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM)
					try: cwp_attrWeight = float(item.GetStringAttribute("WEIGHT"))
					except Exception as ex:
						cwp_prt = item.Parent
						cwp_list.append("Аттрибутивная масса %s (%s) отсутствует" %(item.DisplayName,cwp_prt.DisplayName))
						continue
					try: cwp_propsMass = round(cwp_weightProps.Mass,4)
					except Exception as ex:
						cwp_prt = item.Parent
						cwp_list.append("Системная масса %s (%s) отсутствует" %(item.DisplayName,cwp_prt.DisplayName))
						continue
					if cwp_attrWeight != cwp_propsMass:
						cwp_prt = item.Parent
						#cwp_list.append("Системная и аттрибутивная массы %s (%s) не совпадают %s -- %s" %(item.DisplayName,cwp_prt.DisplayName,cwp_attrWeight,cwp_propsMass))
						cwp_list.append("Системная и аттрибутивная массы %s (%s) не совпадают" %(item.DisplayName,cwp_prt.DisplayName))
					else: pass
				elif item.IsSuppressed:
					assembliesGeneralPropertiesBuilder = self.workPart.PropertiesManager.CreateAssembliesGeneralPropertiesBuilder([item])
					if assembliesGeneralPropertiesBuilder.ReferenceComponent == NXOpen.Assemblies.AssembliesGeneralPropertiesBuilder.ReferenceComponentOptions.Yes:
						continue
					else:
						self.workPart.ComponentAssembly.UnsuppressComponents([item])
						if len(item.GetChildren()) != 0: 
							self.workPart.ComponentAssembly.SuppressComponents([item]) 
							continue
						self.workPart.ComponentAssembly.SuppressComponents([item])
				elif len(item.GetChildren()) != 0: continue
				else: pass
			if len(cwp_list) == 0: return  True
			else: return  "Проверка параметров массы: ЭМ не соответствует требованиям:\n%s" %("\n".join(cwp_list))
		except Exception as ex:
			return ("checkWeightProps failed with {0}".format(ex ))

	def checkSaveMode(self):
		try:
			if self.theUF.Weight.AskPartSaveOption(self.workPart.Tag): return True
			else: return "Проверка режима обновления массы: Нет обновления массы при сохранении"
		except Exception as ex:
			return ("checkSaveMode failed with {0}".format(ex))

	def checkMassAccuracy(self):
		try: 
			massAccuracy = self.configuration["sampleMassAccuracy"]
			weightProps = self.theUF.Weight.AskProps(self.workPart.Tag, NXOpen.UF.Weight.UnitsType.UNITS_KMM)
			if weightProps.Accuracy == massAccuracy: return True
			else: return "Проверка точности расчета массы: точность не соответствует требованиям"
		except Exception as ex:
			return ("checkMassAccuracy failed with {0}".format(ex))

	def checkMassRefset(self):
		try: 
			massRefSet = self.configuration["massReferenceSet"]
			modelMassRefSet = self.theUF.Weight.AskPartRefSet(self.workPart.Tag)
			if modelMassRefSet == massRefSet: return True
			else: return "Проверка ссылочного набора расчета массы: СН не соответствует требованиям"
		except Exception as ex:
			return ("checkMassRefset failed with {0}".format(ex))

	def checkModelAccuracy(self):
		try:
			conclusion = []
			distanceTollerance = self.configuration["distanceTollerance"]
			angleTollerance = self.configuration["angleTollerance"]
			modelDistanceTollerance = self.workPart.Preferences.Modeling.DistanceToleranceData
			modelAngleTollerance = self.workPart.Preferences.Modeling.AngleToleranceData
			statementAngle = distanceTollerance == modelDistanceTollerance
			statementDistance = angleTollerance == modelAngleTollerance
			if statementAngle: pass
			else: conclusion.append("Проверка точности моделирования: угловой допуск не соответствует требованиям")
			if statementDistance: pass
			else: conclusion.append("Проверка точности моделирования: линейный допуск не соответствует требованиям")
			if len(conclusion) == 0: return True
			else: return "\n".join(conclusion)
		except Exception as ex:
			return ("checkModelAccuracy failed with {0}".format(ex))

	def _cycleObjects(self, _type, _subtype = None):
		objects = []
		tmpBodyTag = 0
		while True:
			tmpBodyTag = self.theUF.Obj.CycleObjsInPart(self.workPart.Tag, _type,tmpBodyTag)
			if tmpBodyTag == 0: break 
			else:
				theType, theSubType = self.theUF.Obj.AskTypeAndSubtype(tmpBodyTag)
				if _subtype is None:
					if theType == _type:
						objects.append(NXOpen.TaggedObjectManager.GetTaggedObject(tmpBodyTag)) 
				else:
					if theSubType == _subtype:
						objects.append(NXOpen.TaggedObjectManager.GetTaggedObject(tmpBodyTag))
		return objects

	def _cls_unifiedOutput(self,lst):
		try:
			if len(lst) <= 1: return lst
			else:
				lst.sort()
				uo_list = []
				fstElem = lst[0]
				lstElem = None
				for i,item in enumerate(lst):
					if lst.index(item) == len(lst)-1: 
						if fstElem is None:
							uo_list.append("%s" %(item))
							break
						else: uo_list.append("%s - %s" %(fstElem,item))
					elif lst[i+1] - item == 1:			
						if fstElem is None:	fstElem = item
						lstElem = lst[i+1]
					elif lst[i+1] - item > 1:
						if lstElem is None:
							uo_list.append("%s" %(item))
							fstElem = None		
						else:
							uo_list.append("%s - %s" %(fstElem,lstElem))
							fstElem, lstElem = None, None
				uo_string = "{0}".format(", ".join(uo_list))
				return uo_string
		except Exception as ex:
			return ("_cls_unifiedOutput failed with {0}".format(ex))

	def checkLayerStatement(self):
		try:
			conclusion = []
			layerManager = self.workPart.Layers
			selectableLayers = self.configuration["layerCollectionSelectable"]
			visibleLayers = self.configuration["layerCollectionVisible"]
			workLayers = self.configuration["layerCollectionWork"]
			modelLayersHidden = []
			modelLayersWork = []
			modelLayersSelectable = []
			modelLayersVisible = []
			for modelLayerNum in range(1,257):
				layerState = layerManager.GetState(modelLayerNum)
				if layerState == NXOpen.Layer.State.Hidden:	modelLayersHidden.append(modelLayerNum)
				elif layerState == NXOpen.Layer.State.Visible: modelLayersVisible.append(modelLayerNum) #ВОТ ТУТ ТРАБЛ
				elif layerState == NXOpen.Layer.State.Selectable: modelLayersSelectable.append(modelLayerNum)
				elif layerState == NXOpen.Layer.State.WorkLayer: modelLayersWork.append(modelLayerNum)
			nonHidenLayersUnion =  workLayers + selectableLayers
			if sorted(modelLayersWork) == sorted(workLayers): pass
			else: conclusion.append("Проверка набора слоев: неверный рабочий слой")
			if sorted(modelLayersVisible) == sorted([visibleLayers]): pass
			else: conclusion.append("Проверка набора слоев: неверный набор видимых слоев")
			if sorted(modelLayersSelectable) == sorted(selectableLayers): pass
			else: conclusion.append("Проверка набора слоев: неверный набор выбираемых слоев")
			if sorted(modelLayersHidden) == sorted(list(filter(lambda x: x not in nonHidenLayersUnion,[i for i in range(1,257)]))): pass
			else: conclusion.append("Проверка набора слоев: неверный набор скрытых слоев")
			if len(conclusion) == 0: return True
			else: return "\n".join(conclusion)
		except Exception as ex:
			return ("checkLayerStatement failed with {0}".format(ex))

	def checkReferenceSetDifferences(self):
		try:
			referenceSetCollection = self.workPart.GetAllReferenceSets()
			refSetCombinations = list(itertools.combinations(referenceSetCollection,2))
			equalReferenceSets = []
			for item in refSetCombinations:
				membersA = item[0].AskMembersInReferenceSet()
				membersB = item[1].AskMembersInReferenceSet()
				sortedMembersA = sorted(membersA, key = lambda member: member.Name)
				sortedMembersB = sorted(membersB, key = lambda member: member.Name)
				if sortedMembersA == sortedMembersB:
					equalFlagString = "Ссылочный набор {0} дублирует {1}".format(sortedMembersA,sortedMembersB)
					equalReferenceSets.append(equalFlagString)
				else: continue
			if len(equalReferenceSets) == 0: return True
			else: return ' | '.join(equalReferenceSets)
		except Exception as ex:
			return ("checkReferenceSetDifferences failed with {0}".format(ex))

	def checkLayerCategories(self):
		layerCats = list(self.workPart.LayerCategories)
		layerCatNames = [item.Name for item in layerCats]
		statement = sorted(layerCatNames) == sorted(self.configuration["sampleCategorySet"])
		if statement: return True
		else: return "Проверка набора категорий слоев: Набор категорий слоев задан неверно" 

	def checkComponentsRefSetAllocation(self):
		try:
			_placementMap = {"SOLIDS":[],"UGROUTE_MECH":[],"UGROTE_ELECT":[],"PKI":[]}
			#	most complex task for all check procedure
			if self.rtComp in [0,None]: 
				components = [self.workPart]
				conclusion = ["%s -- %s" %(item.Name,item.ReferenceSet) for item in components]
			else: 
				components = self._reportComponentChildren(self.rtComp,[self.rtComp])
				conclusion = ["%s -- %s" %(item.DisplayName,item.ReferenceSet) for item in components]
			#return TRUE OR FALSE of statement
			return "\n".join(conclusion)
		except Exception as ex:
			return("checkComponentsRefSetAllocation failed with %s"%ex)
	
	def checkHistoryMode(self):
		try:
			statement = self.workPart.Preferences.Modeling.GetHistoryMode() == eval(self.configuration["historyMode"],{})
			if statement: True
			else: return "Проверка режима истории: неверный режим сохранения истории" 
		except Exception as ex:
			return ("checkHistoryMode failed with {0}".format(ex))
	
	def checkHistoryFeatures(self):
		try:
			if len(list(self.workPart.Features)) != 0:
				chf_list = [item.JournalIdentifier for item in self.workPart.Features if "LINKED" not in item.FeatureType ]
				if len(chf_list) == 0: return True
				else: return "ЭМ содержит элементы истории модели"
			else: return True 
		except Exception as ex:
			return ("checkHistoryFeatures failed with {0}".format(ex))

	def checkModelRefSets(self):
		try:
			conclusion = []
			requirementSample = sorted(self.configuration["sampleReferenceSet"])
			requirementRefSet = self.configuration["requirementReferenceSet"]
			referenceSetToDelete = self.configuration["referenceSetToDelete"]
			modelRefSet = sorted([item.Name for item in self.workPart.GetAllReferenceSets()])
			if requirementSample == modelRefSet: return True
			else:
				if requirementSample != modelRefSet: conclusion.append("Проверка ссылочных наборов модели: неверный состав СН")
				if len(set(modelRefSet).intersection(set(requirementRefSet))) == 0: conclusion.append("Проверка ссылочных наборов модели: отсутствуют обязательные СН")
				if len(set(modelRefSet).intersection(set(referenceSetToDelete))): conclusion.append("Проверка ссылочных наборов модели: удалить недопустимые СН ")
				return "\n".join(conclusion)
		except Exception as ex:
			return ("checkModelRefSets failed with {0}".format(ex))

	def checkEmptyComponentsGroups(self):
		try:
			groupsCollection = [item for item in self.workPart.Features if isinstance(item,NXOpen.Features.FeatureGroup)]
			emptyGroups = [item.Name for item in groupsCollection if len(item.GetMembers())==0]
			if len(emptyGroups) == 0: return True
			else: return "ЭМ содержит пустые группы: %s" %("-".join(emptyGroups))
		except Exception as ex:
			return("checkEmptyComponentsGroups failed with {0}".format(ex))

def main():
	app = AKS_checker_application()
	if app.loadConfig(app.configurationFile):
		app.lw.Open()
		functions = app.configuration["functions"]	
		for func in functions:
			result = eval(func)() #очень небезопасно
			if isinstance(result, bool): pass
			else: app.lw.WriteLine(result)
	else: pass

if __name__=="__main__":
	main()

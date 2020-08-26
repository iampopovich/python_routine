import NXOpen
import NXOpen.UF
import NXOpen.Layer
import math
import time as tt
import datetime as dt

def main():
	theSession  = NXOpen.Session.GetSession()
	theUI = NXOpen.UI.GetUI()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	tStart = dt.datetime.now()
	lw.WriteLine('%s' %checkLayerStatement(workPart))
	lw.WriteLine('%s' %(dt.datetime.now()- tStart))
	
def lrs_unifiedOutput(lst):
	try:
		if len(lst) == 0: return lst
		else:
			lst.sort()
			uo_list = []
			fstElem = lst[0]
			for i,item in enumerate(lst):
				if lst.index(item) == len(lst)-1: 
					if fstElem is None:
						uo_list.append('%s' %(item))
						break
					else:
						uo_list.append('%s - %s' %(fstElem,item))
				elif lst[i+1] - item == 1:			
					if fstElem is None:
						fstElem = item
					lstElem = lst[i+1]
				elif lst[i+1] - item > 1:
					if lstElem is None:
						uo_list.append('%s' %(item))		
					else:
						uo_list.append('%s - %s' %(fstElem,lstElem))
						fstElem, lstElem = None, None
			uo_string = '%s' %(', '.join(map(str,uo_list)))
			return uo_string
	except Exception as ex:
		return('lrs_unifiedOutput failed with %s' %ex)
		
def checkLayerStatement(workPart):
	try:
		layerCats = workPart.LayerCategories
		layerManager = workPart.Layers
		lrs_layersHidden = []
		lrs_layersWork = []
		lrs_layersSelectable = []
		lrs_layersVisible = [] #почему-то не показывает никаких вилимых слоев. дальше разберусь 
		lrs_string = ''
		for lrs_layerNum in range(1,256):
			if layerManager.GetState(lrs_layerNum) == NXOpen.Layer.State.Hidden:
				lrs_layersHidden.append(lrs_layerNum)
			elif layerManager.GetState(lrs_layerNum) == NXOpen.Layer.State.Visible:
				lrs_layersVisible.append(lrs_layerNum)
			elif layerManager.GetState(lrs_layerNum) == NXOpen.Layer.State.Selectable:
				lrs_layersSelectable.append(lrs_layerNum)
			elif layerManager.GetState(lrs_layerNum) == NXOpen.Layer.State.WorkLayer:
				lrs_layersWork.append(lrs_layerNum)
		lrs_string += 'lrs_layersHidden %s\n' %lrs_unifiedOutput(lrs_layersHidden)
		lrs_string += 'lrs_layersSelectable %s\n' %lrs_unifiedOutput(lrs_layersSelectable)
		lrs_string += 'lrs_layersVisible %s\n' %lrs_unifiedOutput(lrs_layersVisible)
		lrs_string += 'lrs_layersWork %s\n' %lrs_unifiedOutput(lrs_layersWork)
		return lrs_string
	except Exception as ex:
		return('checkLayerStatement failed with %s' %ex)

if __name__ == '__main__':
	main()

'''
	stateLayerArray = NXOpen.UF.Layer.StateInfo(1, NXOpen.UF.Layer.State.WorkLayer)
	layer state enumeration. 
	WorkLayer	Work layer. All newly created objects are placed on the work layer.
	Selectable	Objects on the layer are selectable
	Visible	Objects on the layer are visible but not selectable
	Hidden	Objects on the layer are not visible and not selectable		
	'''

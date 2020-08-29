import NXOpen
import NXOpen.UF
import subprocess
import codecs
import sys
import os
import shutil



def main() :
	global theUF
	theUF = NXOpen.UF.UFSession.GetUFSession()
	theSession  = NXOpen.Session.GetSession()
	theUF = NXOpen.UF.UFSession.GetUFSession()
	workPart = theSession.Parts.Work
	displayPart = theSession.Parts.Display
	global lw
	lw = theSession.ListingWindow
	lw.Open()
	lw.WriteLine(checkBackgroundColor(workPart))

def validUsersBackground(workPart):
	#setter for custom backgroundcolor
	pass

def checkBackgroundColor(workPart):
	workView = workPart.ModelingViews
	cbc_badViews = []
	#cbc_fillMode = не определяется NX задается пользователем из формы
	for i,item in enumerate(workView):
		layout = workPart.Layouts.FindObject("L1") #слой вывода изображения???
		layout.ReplaceView(workPart.ModelingViews.WorkView, item, True)
		item.Orient(item.Name, NXOpen.View.ScaleAdjustment.Fit)
		cbc_strPartJpg = 'C:\\temp\\view-%s.jpg' %i
		theUF.Disp.CreateImage(cbc_strPartJpg, theUF.Disp.ImageFormat.BMP, theUF.Disp.BackgroundColor.ORIGINAL) #theUF.Disp.ImageFormat.JPEG
		#cbc_subp = subprocess.Popen(['%s\\analyze.exe' %os.getcwd(),cbc_strPartJpg])
		#cbc_subp = subprocess.Popen(['C:\\Users\\PopovAV\\Desktop\\tempWF\Разработка\\analyze.exe',cbc_strPartJpg])
		cbc_subp = subprocess.Popen(['D:\\Programs\\Python\\Python35\\python.exe','C:\\Users\\PopovAV\\Desktop\\tempWF\\Разработка\\_test_7-5-2-DONE_checkPixels.py',cbc_strPartJpg])
		cbc_subp.wait()
		cbc_badColorFlag = cbc_subp.communicate()
		cbc_subp.kill()
		#os.remove(cbc_strPartJpg)
		lw.WriteLine(str(cbc_badColorFlag))
		if cbc_badColorFlag:
			cbc_badViews.append(item.Name)

	if len(cbc_badViews) == 0: cbc_string = 'Закраска фона соответствует требованиям'
	elif len(cbc_badViews) == 1: cbc_string = 'Закраска фона вида %s не соответствует требованиям' %('\n'.join(map(str,cbc_badViews)))
	elif len(cbc_badViews) > 1: cbc_string = "Закраска фона видов не соответствует требованиям:\n%s" %('\n'.join(map(str,cbc_badViews)))
	else: pass
	return (cbc_string)
	
if __name__ == '__main__':
	main()



	'''
	from PIL import Image
import sys 

def checkImagePixels(cip_imgPath, cip_fillMode = None):
	try:
		cip_fillMode = 'graduated' #пока работает только для градиентной заливки
		cip_img = Image.open(cip_imgPath)
		cip_validList = [] #contains first pixels' column
		cip_correct, cip_false = 0,0
		for y in [0]:
			for x in range(0,cip_img.size[1]-1):
				cip_px = cip_img.getpixel((y,x))
				cip_hsv = rgb2hsv(cip_px[0],cip_px[1],cip_px[2])
				cip_validList.append(cip_hsv)
		if cip_fillMode =='flat':
			#set(cip_validList)
			for i,item in enumerate(cip_validList):
				try:
					if cip_validList[i][1] == cip_validList[i+1][1]: 
						cip_correct+=1
					else: cip_false+=1
				except: continue
		elif cip_fillMode == 'graduated':
			for i,item in enumerate(cip_validList):
				try:
					if cip_validList[i][1] < cip_validList[i+1][1]: cip_correct+=1
					else: cip_false+=1
				except: continue	
		elif cip_fillMode == 'image': pass
		elif cip_fillMode == 'hemiDome': pass
		else: pass
		if cip_correct > cip_false: return 'image %s passed' %cip_imgPath
		else: return 'image %s not passed' %cip_imgPath
		#[print(item) for item in cip_validList]
	except Exception as ex:
		return ('checkImagePixels failed with %s' %ex)

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn: h = 0
    elif mx == r: h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g: h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b: h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0: s = 0
    else: s = df/mx
    v = mx
    return h,s,v

def main(path):
	flag = checkImagePixels(path)
	print(flag)
	return flag

if __name__ == '__main__':
	main(sys.argv[1])
	'''

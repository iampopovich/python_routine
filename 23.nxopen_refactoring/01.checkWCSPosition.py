import NXOpen
import NXOpen.UF
import time as tt
import datetime as dt

class NXJournal:
	def __init__(self):
		self.theSession = NXOpen.Session.GetSession()
		self.workPart = self.theSession.Parts.Work
		self.displayPart = self.theSession.Parts.Display
		self.theUI = NXOpen.UI.GetUI()
		self.theUF = NXOpen.UF.UFSession.GetUFSession()
		self.lw = self.theSession.ListingWindow

	def checkWCSPosition(self):
		try:	
			cwo_WCSOrigin = self.workPart.WCS.CoordinateSystem.Origin 
			for item in [cwo_WCSOrigin.X,cwo_WCSOrigin.Y,cwo_WCSOrigin.Z]:
				if item == 0: continue
				else: return 'РСК смещена по позиции'
			return 'РСК в АСК'
		except Exception as ex:
			return ('checkWCSPosition failed with %s' %ex)

	def checkWCSOrientation(self):
		try:
			cwo_WCSRotationMatrix = self.workPart.WCS.CoordinateSystem.Orientation
			for item in [cwo_WCSRotationMatrix.Element.Xx,
						cwo_WCSRotationMatrix.Element.Yy,
						cwo_WCSRotationMatrix.Element.Zz]:
				if item == 1: continue
				else: return 'ОШИБКА! РСК была перемещена!'
			return 'РСК в АСК'
		except Exception as ex:
			return ('checkWCSOrientation failed with %s' %ex)

	def setWCSOrientation(self):
		try:
			swo_WCSOrigin = NXOpen.Point3d(0.0, 0.0, 0.0)
			swo_WCSMatrix = NXOpen.Matrix3x3()
			swo_WCSMatrix.Xx, swo_WCSMatrix.Xy, swo_WCSMatrix.Xz = 1.0, 0.0, 0.0
			swo_WCSMatrix.Yx, swo_WCSMatrix.Yy, swo_WCSMatrix.Yz = 0.0, 1.0, 0.0
			swo_WCSMatrix.Zx, swo_WCSMatrix.Zy, swo_WCSMatrix.Zz = 0.0, 0.0, 1.0
			self.workPart.WCS.SetOriginAndMatrix(swo_WCSOrigin, swo_WCSMatrix)
		except Exception as ex:
			return ('setWCSOrientation failed with %s' %ex)

def main():
	app = NXJournal()
	app.lw.Open()
	app.lw.WriteLine('%s' %app.checkWCSOrientation())
	app.lw.WriteLine('%s' %app.checkWCSPosition())
		
if __name__ == '__main__':
	main()

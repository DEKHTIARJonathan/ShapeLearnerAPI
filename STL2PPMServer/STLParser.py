################################# Import Libraries ################################
import os
import time
import vtk
from threading import Thread
import uuid

class Precision:
    Low, Medium, Superior, Huge, Extreme = range(5)
	
class OutputFormat:
	PPM, PNG, PPMandPNG = range(3)

class STLParser():
	def __init__(self, outdir = "../temp"):
	
		self._difficulty = []
		self._difficulty.append([1,4,1]) #Precision.Low
		self._difficulty.append([1,3,4,3,1])#Precision.Medium
		self._difficulty.append([1,3,6,8,6,3,1]) #Precision.Superior
		self._difficulty.append([1,3,5,6,8,6,5,3,1]) #Precision.Huge
		self._difficulty.append([1,3,5,6,7,8,7,6,5,3,1]) #Precision.Extreme
		
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
		self._outdir = outdir
			
	def _generateFilename (self):
		return str(uuid.uuid4().hex)
	
	def _snapshot(self, renderWindow, outputFormat) :
		formats = []
		if outputFormat == OutputFormat.PPM:
			formats = ["ppm"]
		elif outputFormat == OutputFormat.PNG:
			formats = ["png"]
		elif outputFormat == OutputFormat.PPMandPNG:
			formats = ["ppm", "png"]
			
		# setting the image filter & saving
		image_filter = vtk.vtkWindowToImageFilter()
		image_filter.SetInput(renderWindow)	
		filter_output = image_filter.GetOutput()	
		
		writerDic = dict()
		writerDic["png"] = vtk.vtkPNGWriter()
		writerDic["ppm"] = vtk.vtkPNMWriter()
		
		outname = self._generateFilename()
		
		output = dict()
		output["png"] = ""
		output["ppm"] = ""
		
		for format in formats : 	
		
			outfileName = self._outdir + "/" + outname + "." + format
			
			writerDic[format].SetInput(filter_output)
			writerDic[format].SetFileName(outfileName)
			writerDic[format].Write()
			
			output[format] = outfileName
			
		return output
	
	def generatePPMFiles(self, file, _format, precision):
		
		if precision > Precision.Extreme:
			precision = Precision.Extreme
		elif precision < Precision.Low:
			precision = Precision.Low
		
		format = ""
		if _format == "png":
			format = OutputFormat.PNG
		elif _format == "ppm&png":
			format = OutputFormat.PPMandPNG
		else :
			format = OutputFormat.PPM
		
		difficultyArray = self._difficulty[precision]
		difficultyLevel = len(difficultyArray)
		verticalRotAngle = 180 / float(difficultyLevel -1)
		horizontalRotAngle = [float(360) / x for x in difficultyArray]
	
		if not (file.endswith('.stl') or file.endswith('.STL')) :
			return False
		else :
			renderWindow = vtk.vtkRenderWindow()
			renderWindow.SetOffScreenRendering(1)			
		 
			reader = vtk.vtkSTLReader()
			reader.SetFileName(file)
			
			polydata = vtk.vtkPolyData()
			polydata = reader.GetOutput()
			polydata.Update()
			xmin, xmax, ymin, ymax, zmin, zmax = polydata.GetBounds()

			dx = (xmax + xmin) / 2
			dy = (ymax + ymin) / 2
			dz = (zmax + zmin) / 2
			
			mapper = vtk.vtkPolyDataMapper()
			if vtk.VTK_MAJOR_VERSION <= 5:
				mapper.SetInput(reader.GetOutput())
			else:
				mapper.SetInputConnection(reader.GetOutputPort())
				
			camera = vtk.vtkCamera()
			camera.SetPosition(0,0,1);
			camera.SetFocalPoint(0, 0, 0)
			camera.SetParallelProjection(1)
			
			# Create a rendering window and renderer
			renderer = vtk.vtkRenderer()
			renderer.SetActiveCamera(camera);
			renderWindow	= vtk.vtkRenderWindow()
			renderWindow.AddRenderer(renderer)
			renderWindow.SetSize(300,300)
			
			# create a renderwindowinteractor
			interactiveRenderer = vtk.vtkRenderWindowInteractor()
			interactiveRenderer.SetRenderWindow(renderWindow)
			
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetDiffuseColor(0,0,0)
			actor.SetOrigin(dx,dy,dz)
			
			# Assign actor to the renderer
			renderer.SetBackground(1,1,1)
			renderer.AddActor(actor)
			renderer.ResetCamera()

			renderWindow.Render()
			
			output = dict()
			output["png"] = []
			output["ppm"] = []
			for i in range(0, difficultyLevel):
				for x in range(0, difficultyArray[i]):
					renderer.ResetCameraClippingRange()
					
					tmp = self._snapshot(renderWindow, format)
					
					if tmp["png"] != "":
						output["png"].append(tmp["png"])
					if tmp["ppm"] != "":
						output["ppm"].append(tmp["ppm"])
					
					actor.RotateZ(horizontalRotAngle[i])
				actor.RotateX(verticalRotAngle)
					
			return output

'''
def getDirs(path) : 
	dirs = []
	listing = os.listdir(path)
	for d in listing:
		if os.path.isdir(path + "/" + d):
			dirs.append(d)
	return dirs

def getFiles(path) : 
	files = []
	listing = os.listdir(path)
	for f in listing:
		if os.path.isfile(path + "/" + f):
			files.append(f)
	return files
'''
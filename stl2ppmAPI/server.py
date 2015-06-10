import os
import time
import vtk
	
def snapshot(filename, subDirName) :
	global renderWindow
	
	formats = ["ppm", "png"]
		
	# setting the image filter & saving
	image_filter = vtk.vtkWindowToImageFilter()
	image_filter.SetInput(renderWindow)	
	
	outDir = "outputs"
				
	writerDic = dict()
	writerDic["png"] = vtk.vtkPNGWriter()
	writerDic["ppm"] = vtk.vtkPNMWriter()
	
	for format in formats : 
		
		output = outDir + "/" + format + "/" + subDirName
		
		if not os.path.isdir(output):
			os.makedirs(output)
		
		outName = output + "/" + filename + "." + format
		
		writerDic[format].SetInput(image_filter.GetOutput())
		writerDic[format].SetFileName(outName)
		writerDic[format].Write()

def computeSTL(subFolder, objName, subdir = ""):
	global renderWindow
	inputFolder = "inputs"
	filename = inputFolder + "/" + subFolder + "/" + objName
	basename = os.path.basename(filename)[:-4]
	
	print filename
 
	reader = vtk.vtkSTLReader()
	reader.SetFileName(filename)
	
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
		
	if subdir != "" :	
		outdir = subdir + "/" + subFolder
	else :
		outdir = subdir + "/" + subFolder
		
	outputName = outdir + "/" + basename

	counter = 1

	for i in range(0, difficultyLevel):
		for x in range(0, difficultyArray[i]):
			renderer.ResetCameraClippingRange()
			snapshot(basename + str(i) + str(x), outdir) 
			actor.RotateZ(horizontalRotAngle[i])
			counter += 1
		actor.RotateX(verticalRotAngle)


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

####################### Generation FUNCTION #######################

def launchGeneration(level):
	global precisionLevel
	global difficultyArray
	global difficultyLevel
	global verticalRotAngle
	global horizontalRotAngle
	
	
	precisionLevel = precision[level]
	difficultyArray = difficulty[precisionLevel]
	difficultyLevel = len(difficultyArray)
	verticalRotAngle = 180 / float(difficultyLevel -1)
	horizontalRotAngle = [float(360) / x for x in difficultyArray]

	
	inputDir = "inputs"

	subDirs = getDirs(inputDir)

	for d in subDirs :
		files = getFiles(inputDir + "/" + d)
		for f in files :
			if (f.endswith('.stl') or f.endswith('.STL')) and f[0] != "." :
				computeSTL(d,f, precisionLevel)				

####################### LAUNCH EXECUTION #######################
				
precision = ["Low", "Medium", "High", "Extreme", "Ultimate"]

difficulty = dict()
difficulty[precision[0]] = [1,4,1]	# LOW
difficulty[precision[1]] = [1,3,4,3,1]	# MEDIUM
difficulty[precision[2]] = [1,3,6,8,6,3,1]	# HIGH
difficulty[precision[3]] = [1,3,5,6,8,6,5,3,1]	# EXTREME
difficulty[precision[4]] = [1,3,5,6,7,8,7,6,5,3,1]	# ULTIMATE

precisionLevel = -1
difficultyArray = -1
difficultyLevel = -1
verticalRotAngle = -1
horizontalRotAngle = -1

renderWindow	= vtk.vtkRenderWindow()

launchGeneration(0)
launchGeneration(1)
launchGeneration(2)
launchGeneration(3)
launchGeneration(4)
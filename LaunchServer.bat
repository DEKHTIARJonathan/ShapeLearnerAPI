set absPath=%cd%

set sub1=\ShapeLearnerAPI
set ShapeLearnerAPI=%absPath%%sub1%

set sub2=\PredictionAPI
set PredictionAPI=%absPath%%sub2%

set sub3=\ShockGraphAPI
set ShockGraphAPI=%absPath%%sub3%

set sub4=\JobServer
set JobServer=%absPath%%sub4%

set sub5=\STL2PPMServer
set STL2PPMServer=%absPath%%sub5%

START cmd.exe /k "cd %ShapeLearnerAPI% & LaunchServer.bat"
START cmd.exe /k "cd %STL2PPMServer% & LaunchServer.bat"
START cmd.exe /k "cd %JobServer% & LaunchServer.bat"
START cmd.exe /k "cd %ShockGraphAPI% & LaunchServer.bat"

::START cmd.exe /k "cd %PredictionAPI% & LaunchServer.bat"

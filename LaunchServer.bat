set absPath=%cd%
set sub1=\ShapeLearnerAPI
set sub2=\PredictionAPI
set sub3=\ShockGraphAPI
set sub4=\JobServer
set sub5=\STL2PPMServer
set ShapeLearnerAPI=%absPath%%sub1%
set PredictionAPI=%absPath%%sub2%
set ShockGraphAPI=%absPath%%sub3%
set JobServer=%absPath%%sub4%
set STL2PPMServer=%absPath%%sub5%

START cmd.exe /k "cd %STL2PPMServer% & LaunchServer.bat"
START cmd.exe /k "cd %JobServer% & LaunchServer.bat"
START cmd.exe /k "cd %ShockGraphAPI% & LaunchServer.bat"
::START cmd.exe /k ""cd %ShapeLearnerAPI% & LaunchServer.bat"
::START cmd.exe /k "cd %PredictionAPI% & LaunchServer.bat"

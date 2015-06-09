set absPath=%cd%
set sub1=\ShapeLearnerAPI
set sub2=\PredictionAPI
set ShapeLearnerAPI=%absPath%%sub1%
set PredictionAPI=%absPath%%sub2%

START cmd.exe /k "cd %ShapeLearnerAPI% & LaunchServer.bat"
START cmd.exe /k "cd %PredictionAPI% & LaunchServer.bat"

call "C:\Anaconda\Scripts\anaconda.bat"
conda update conda -y
conda install numpy scikit-learn sqlalchemy vtk uuid -y 
conda install -c https://conda.binstar.org/topper psycopg2-win-py27 -y
pip install bottle paste
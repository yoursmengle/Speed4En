import os
import nicegui
from pathlib import Path
import subprocess
import coincurve 

'''
#
# -i icon of this app
# -n filename of execute, will add .exe in windows
# -F generate a single file
# -w generate a window programe, no shell info display
# --add-data  add static files
# --hidden-import matplotlib.backends.backend_svg import svg of matplotlib
'''

script = f''' \
    python -m PyInstaller main.py \
    -i favicon.ico \
    -n speed4en \
    -F \
    -w \
    --add-data="{Path(nicegui.__file__).parent}{os.pathsep}nicegui" \
    --add-data="{Path(coincurve.__file__).parent}{os.pathsep}coincurve" \
    --hidden-import matplotlib.backends.backend_svg \
'''

subprocess.call(script, shell=True)

venv/scripts/activate.ps1
python -m pip install -r requirements.txt
python build.py
cp dist/*.exe .
dir *.exe



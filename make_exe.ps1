# Check if activate.ps1 exists
if (-Not (Test-Path -Path "venv/scripts/activate.ps1")) {
    # If activate.ps1 does not exist, create the virtual environment
    python -m venv venv
}
venv/scripts/activate.ps1
python -m pip install -r requirements.txt
python build.py
cp dist/*.exe .
dir *.exe



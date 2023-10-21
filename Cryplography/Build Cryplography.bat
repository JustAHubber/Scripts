winget install python.python.3.12
python -m pip install cryptography
python -m pip install pyinstaller
pyinstaller --noconfirm --onefile --console --name "Cryplography" --clean --hidden-import "cryptography" "Cryplography.py"
del build && del Crypolography_Custom.spec
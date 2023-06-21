winget install Python.Python.3.11
pip install pyinstaller
pyinstaller --noconfirm --onefile --console --icon pong.ico --name "Pong Admin" --clean  "Pong Admin.py"
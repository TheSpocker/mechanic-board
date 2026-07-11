Mechanic Board Windows Installer
================================

Option 1: simple local installer
--------------------------------
1. Open PowerShell in this folder.
2. Run:
   powershell -ExecutionPolicy Bypass -File .\install.ps1
3. The installer will create a local app folder under %LOCALAPPDATA%\MechanicBoard and install Python dependencies.
4. Run the generated start-mechanic-board.bat file to launch the app.

Option 2: build a real Windows installer EXE
-------------------------------------------
1. Install NSIS from https://nsis.sourceforge.io/
2. Open PowerShell in this folder.
3. Run:
   powershell -ExecutionPolicy Bypass -File .\build-installer.ps1
4. This will generate mechanic-board-installer.exe in the windows folder.

The app will be available at:
- http://127.0.0.1:8000/board/
- http://127.0.0.1:8000/admin/

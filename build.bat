@echo off
echo Building Screenshot Service...
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Creating icon...
python create_icon.py
if %errorlevel% neq 0 (
    echo Warning: Failed to create icon, continuing without custom icon...
)

echo.
echo Step 3: Building executable...
python build.py
if %errorlevel% neq 0 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\ScreenshotService.exe
echo.
echo You can now run ScreenshotService.exe to start the application.
pause 
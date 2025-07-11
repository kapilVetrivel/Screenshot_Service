import subprocess
import sys
import os

def build_executable():
    """Build the screenshot application into an executable"""
    
    # PyInstaller command to create a single executable file
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable
        "--windowed",                   # Don't show console window
        "--name=ScreenshotService",     # Name of the executable
        "--icon=icon.ico",              # Icon file (if available)
        "--add-data=icon.ico;.",        # Include icon file
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets", 
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=keyboard",
        "--hidden-import=pyautogui",
        "--hidden-import=PIL",
        "--hidden-import=tkinter",
        "screenshot_app.py"
    ]
    
    try:
        print("Building executable...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created in: dist/ScreenshotService.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it first:")
        print("pip install pyinstaller")
        return False

if __name__ == "__main__":
    build_executable() 
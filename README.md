# Screenshot Service

A Windows application that runs in the background and allows you to take screenshots using the F12 hotkey. The application appears as a system tray icon and provides options for both full-screen and cropped screenshots.

## Features

- **Background Operation**: Runs silently in the system tray
- **Hotkey Trigger**: Press F12 to activate screenshot capture
- **Two Screenshot Modes**:
  - Full Screen Screenshot
  - Cropped Screenshot (with area selection)
- **Automatic File Management**: Screenshots are saved with timestamps
- **System Tray Menu**: Quick access to functions and settings
- **No Console Window**: Clean execution without visible command prompts

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11

### Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Icon** (optional):
   ```bash
   python create_icon.py
   ```

3. **Build Executable**:
   ```bash
   python build.py
   ```

   This will create `dist/ScreenshotService.exe`

## Usage

### Running the Application

1. **Double-click** `ScreenshotService.exe` to start the application
2. The app will appear as a **system tray icon** (near the clock)
3. A notification will confirm the service is running

### Taking Screenshots

1. **Press F12** anywhere on your screen
2. Choose your screenshot type:
   - **Full Screen Screenshot**: Captures the entire screen
   - **Cropped Screenshot**: Allows you to select a specific area
3. For cropped screenshots:
   - Click and drag to select the area
   - Release to capture
4. Screenshots are automatically saved to `~/Screenshots/`

### System Tray Menu

Right-click the system tray icon to access:
- **Open Screenshots Folder**: View saved screenshots
- **Take Screenshot Now**: Manual screenshot trigger
- **Quit**: Close the application

## File Structure

```
Screenshot_Service/
├── screenshot_app.py      # Main application code
├── requirements.txt       # Python dependencies
├── build.py              # Build script for executable
├── create_icon.py        # Icon generation script
├── README.md             # This file
├── icon.ico              # Application icon (generated)
└── dist/
    └── ScreenshotService.exe  # Final executable
```

## Screenshot Storage

- **Location**: `%USERPROFILE%\Screenshots\`
- **Naming Convention**: 
  - Full screenshots: `full_screenshot_YYYYMMDD_HHMMSS.png`
  - Cropped screenshots: `cropped_screenshot_YYYYMMDD_HHMMSS.png`

## Development

### Running from Source

```bash
python screenshot_app.py
```

### Key Components

- **ScreenshotCapture**: Handles screenshot functionality
- **ScreenshotDialog**: UI for screenshot type selection
- **HotkeyListener**: Background thread for F12 detection
- **ScreenshotApp**: Main application with system tray integration

## Troubleshooting

### Common Issues

1. **F12 not working**: 
   - Ensure the application has focus or try running as administrator
   - Check if F12 is used by other applications

2. **Screenshots not saving**:
   - Verify write permissions in the user directory
   - Check available disk space

3. **Cropped screenshot issues**:
   - Ensure you select an area larger than 10x10 pixels
   - Try running the application as administrator

### Building Issues

If the build fails:
1. Ensure PyInstaller is installed: `pip install pyinstaller`
2. Check all dependencies are installed: `pip install -r requirements.txt`
3. Try running the build script as administrator

## Security Notes

- The application requires keyboard hook access for F12 detection
- Screenshots are saved locally in the user's directory
- No data is transmitted to external servers

## License

This project is open source and available under the MIT License. 
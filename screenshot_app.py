import sys
import os
import threading
import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QWidget, 
                             QVBoxLayout, QPushButton, QLabel, QMessageBox,
                             QDialog, QHBoxLayout, QFileDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QEventLoop, QCoreApplication, QSharedMemory
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QGuiApplication, QPainter, QPaintEvent, QClipboard
import pyautogui
import keyboard
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import messagebox

# --- Single instance check ---
shared_memory = QSharedMemory('ScreenshotServiceUniqueKey')
if not shared_memory.create(1):
    app = QApplication(sys.argv)
    QMessageBox.warning(None, "Screenshot Service", "The Screenshot Service is already running.")
    sys.exit(0)
# --- End single instance check ---

class CroppingWidget(QWidget):
    cropped = pyqtSignal(int, int, int, int)
    cropped_and_saved = pyqtSignal(str)  # filepath

    def __init__(self, screen_pixmap, parent=None):
        super().__init__(parent)
        print("[DEBUG] CroppingWidget created.")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.SplashScreen)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.screen_pixmap = screen_pixmap
        self.origin = None
        self.crop_rect = None
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.show()
        self.activateWindow()
        self.raise_()
        print("[DEBUG] CroppingWidget shown and raised.")
        # Set screenshot_dir attribute
        if parent and hasattr(parent, 'screenshot_capture'):
            self.screenshot_dir = parent.screenshot_capture.screenshot_dir
        else:
            documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
            self.screenshot_dir = os.path.join(documents_dir, "ScreenshotService")
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def showEvent(self, event):
        print("[DEBUG] CroppingWidget showEvent triggered.")
        super().showEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw the full screenshot
        painter.drawPixmap(0, 0, self.screen_pixmap)
        # Draw a translucent overlay over the whole screen
        overlay_color = QColor(0, 0, 0, int(255 * 0.5))
        painter.fillRect(self.rect(), overlay_color)
        # If cropping, draw the crop area as a direct copy of the screenshot
        if self.crop_rect is not None:
            # Draw the original screenshot in the crop area (makes it look transparent)
            crop = self.screen_pixmap.copy(self.crop_rect)
            painter.drawPixmap(self.crop_rect.topLeft(), crop)
            # Draw a red border around the crop area
            pen = QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.crop_rect)

    def mousePressEvent(self, event):
        print(f"[DEBUG] Mouse press at {event.pos()}")
        self.origin = event.pos()
        self.crop_rect = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.origin is not None:
            self.crop_rect = QRect(self.origin, event.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        print(f"[DEBUG] Mouse release at {event.pos()}")
        if self.origin is not None and self.crop_rect is not None:
            x1 = self.crop_rect.left()
            y1 = self.crop_rect.top()
            x2 = self.crop_rect.right()
            y2 = self.crop_rect.bottom()
            print(f"[DEBUG] Emitting cropped: ({x1}, {y1}, {x2}, {y2})")
            self.cropped.emit(x1, y1, x2, y2)
            # Save the cropped image and emit the path
            crop = self.screen_pixmap.copy(self.crop_rect)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cropped_screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            crop.save(filepath)
            print(f"[DEBUG] Cropped screenshot saved: {filepath}")
            self.cropped_and_saved.emit(filepath)
            self.close()

    def closeEvent(self, event):
        print("[DEBUG] CroppingWidget closeEvent triggered.")
        super().closeEvent(event)

class ScreenshotCapture:
    def __init__(self):
        documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
        self.screenshot_dir = os.path.join(documents_dir, "ScreenshotService")
        self.ensure_screenshot_dir()
        
    def ensure_screenshot_dir(self):
        """Ensure the screenshots directory exists"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def take_full_screenshot(self):
        """Take a full screen screenshot"""
        print("[DEBUG] Taking full screenshot...")
        try:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"full_screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            screenshot.save(filepath)
            print(f"[DEBUG] Full screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"[ERROR] Error taking full screenshot: {e}")
            return None
    
    def take_cropped_screenshot_pyqt(self, parent=None, tray_icon=None):
        # Deprecated: now handled asynchronously
        return None

class ScreenshotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("[DEBUG] ScreenshotDialog created.")
        self.setWindowTitle("Screenshot Options")
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Window)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.activateWindow()
        self.raise_()
        self.show()

        layout = QVBoxLayout()
        instruction_label = QLabel("Choose screenshot type:")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)
        full_screenshot_btn = QPushButton("Full Screen Screenshot")
        full_screenshot_btn.clicked.connect(self.accept_full)
        layout.addWidget(full_screenshot_btn)
        cropped_screenshot_btn = QPushButton("Cropped Screenshot")
        cropped_screenshot_btn.clicked.connect(self.accept_cropped)
        layout.addWidget(cropped_screenshot_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        self.setLayout(layout)
        self.choice = None

        # For debugging: auto-select full screenshot after 2 seconds
        # from PyQt6.QtCore import QTimer
        # QTimer.singleShot(2000, self.accept_full)

    def accept_full(self):
        print("[DEBUG] Full Screen Screenshot button clicked.")
        self.choice = "full"
        self.accept()
    def accept_cropped(self):
        print("[DEBUG] Cropped Screenshot button clicked.")
        self.choice = "cropped"
        self.accept()
    def reject(self):
        print("[DEBUG] ScreenshotDialog cancelled.")
        super().reject()

class HotkeyListener(QThread):
    screenshot_triggered = pyqtSignal()
    
    def run(self):
        """Listen for F12 key press"""
        keyboard.on_press_key("F12", lambda _: self.screenshot_triggered.emit())
        keyboard.wait()

class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.screenshot_capture = ScreenshotCapture()
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.screenshot_triggered.connect(self.show_screenshot_dialog)
        print("[DEBUG] ScreenshotApp initialized.")
        self.hotkey_listener.start()
        self.create_system_tray()
        self.hide()
        self._cropping_widget = None
        self._original_pos = None

    def create_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        tray_menu = QMenu()
        open_folder_action = tray_menu.addAction("Open Screenshots Folder")
        open_folder_action.triggered.connect(self.open_screenshots_folder)
        tray_menu.addSeparator()
        take_screenshot_action = tray_menu.addAction("Take Screenshot Now")
        take_screenshot_action.triggered.connect(self.show_screenshot_dialog)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("Screenshot Service (Press F12 to capture)")
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "Screenshot Service",
            "Service is running. Press F12 to take a screenshot.",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )
        print("[DEBUG] System tray created.")
    
    def show_screenshot_dialog(self):
        print("[DEBUG] show_screenshot_dialog called.")
        self.activateWindow()
        self.raise_()
        dialog = ScreenshotDialog(self)
        result = dialog.exec()
        print(f"[DEBUG] ScreenshotDialog result: {result}, choice: {dialog.choice}")
        if result == QDialog.DialogCode.Accepted:
            if dialog.choice == "full":
                self._original_pos = self.pos()
                print(f"[DEBUG] Moving main window off-screen from {self._original_pos} for full screenshot.")
                self.move(-10000, -10000)
                QTimer.singleShot(250, self.take_full_screenshot_and_restore)
            elif dialog.choice == "cropped":
                self._original_pos = self.pos()
                print(f"[DEBUG] Moving main window off-screen from {self._original_pos}.")
                self.move(-10000, -10000)
                QTimer.singleShot(250, self.start_cropping_async)

    def start_cropping_async(self):
        print("[DEBUG] start_cropping_async called.")
        app = QApplication.instance()
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            print("[ERROR] No primary screen found.")
            self.showNormal()
            return
        pixmap = screen.grabWindow(0)
        self._cropping_widget = CroppingWidget(pixmap, self)
        self._cropping_widget.cropped_and_saved.connect(self.on_cropped_and_saved)
        self._cropping_widget.show()
        self._cropping_widget.activateWindow()
        self._cropping_widget.raise_()

    def on_cropped_and_saved(self, filepath):
        print(f"[DEBUG] on_cropped_and_saved: {filepath}")
        if not filepath:
            self.tray_icon.showMessage(
                "Error",
                "Failed to capture cropped screenshot",
                QSystemTrayIcon.MessageIcon.Warning,
                3000
            )
        else:
            # Copy cropped screenshot to clipboard
            clipboard = QGuiApplication.clipboard()
            pixmap = QPixmap(filepath)
            clipboard.setPixmap(pixmap, QClipboard.Mode.Clipboard)
            print(f"[DEBUG] Cropped screenshot copied to clipboard: {filepath}")
        # Move main window back to original position
        if self._original_pos is not None:
            print(f"[DEBUG] Restoring main window to {self._original_pos}.")
            self.move(self._original_pos)
            self._original_pos = None
        if self._cropping_widget is not None:
            self._cropping_widget.deleteLater()
            self._cropping_widget = None

    def showNormal(self):
        print("[DEBUG] showNormal called.")
        super().showNormal()

    def hide(self):
        print("[DEBUG] hide called.")
        super().hide()

    def setVisible(self, visible):
        print(f"[DEBUG] setVisible({visible}) called.")
        super().setVisible(visible)
    
    def take_full_screenshot(self):
        # Deprecated: now handled by take_full_screenshot_and_restore
        pass
    
    def take_cropped_screenshot(self):
        # Deprecated: now handled asynchronously
        pass
    
    def open_screenshots_folder(self):
        """Open the screenshots folder in file explorer"""
        os.startfile(self.screenshot_capture.screenshot_dir)
    
    def quit_app(self):
        """Quit the application"""
        self.hotkey_listener.terminate()
        self.hotkey_listener.wait()
        QApplication.quit()

    def take_full_screenshot_and_restore(self):
        print("[DEBUG] take_full_screenshot_and_restore called.")
        # Take screenshot and save to file
        filepath = self.screenshot_capture.take_full_screenshot()
        if filepath:
            # Copy to clipboard
            clipboard = QGuiApplication.clipboard()
            pixmap = QPixmap(filepath)
            clipboard.setPixmap(pixmap, QClipboard.Mode.Clipboard)
            print(f"[DEBUG] Full screenshot saved and copied to clipboard: {filepath}")
        else:
            self.tray_icon.showMessage(
                "Error",
                "Failed to capture screenshot",
                QSystemTrayIcon.MessageIcon.Warning,
                3000
            )
        if self._original_pos is not None:
            print(f"[DEBUG] Restoring main window to {self._original_pos} after full screenshot.")
            self.move(self._original_pos)
            self._original_pos = None

def main():
    # Create application without showing console window
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Create and show the main application
    screenshot_app = ScreenshotApp()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
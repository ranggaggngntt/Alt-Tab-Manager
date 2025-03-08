import ctypes
import time
import win32gui
import win32con
import os

cwd = os.getcwd()

explorer_dll = ctypes.WinDLL(f"{cwd}\\focus_injector.dll")

SetTargetWindow = explorer_dll.SetTargetWindow
ForceFocus = explorer_dll.ForceFocus

SetTargetWindow.argtypes = [ctypes.wintypes.HWND]
ForceFocus.argtypes = []

def force_focus(hwnd):
    """Force focus to a window using the injected DLL."""
    if not hwnd or not win32gui.IsWindow(hwnd):
        return False

    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    SetTargetWindow(hwnd)
    time.sleep(0.05)
    ForceFocus()

    return win32gui.GetForegroundWindow() == hwnd

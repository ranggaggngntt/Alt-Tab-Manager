from pynput.mouse import Controller as MouseController
from pywinauto import Desktop
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
import ctypes

from config.window_config import BLACKLIST_TITLES, BLACKLIST_CLASSES

mouse = MouseController()

def get_current_monitor():
    """Get the monitor that currently contains the mouse cursor."""
    x, y = mouse.position
    monitor = win32api.MonitorFromPoint((x, y), win32con.MONITOR_DEFAULTTONEAREST)
    monitor_info = win32api.GetMonitorInfo(monitor)
    return monitor_info['Monitor']

def get_windows_on_current_monitor():
    """Get all visible windows on the current monitor that appear in the taskbar, excluding blacklisted windows."""
    monitor_rect = get_current_monitor()
    windows = []

    desktop = Desktop(backend="win32")
    for window in desktop.windows():
        try:
            if window.is_visible() and window.window_text():
                rect = window.rectangle()
                center_x = (rect.left + rect.right) // 2
                center_y = (rect.top + rect.bottom) // 2

                if (monitor_rect[0] <= center_x <= monitor_rect[2] and
                    monitor_rect[1] <= center_y <= monitor_rect[3]):

                    title = window.window_text()
                    class_name = window.class_name()

                    if (title not in BLACKLIST_TITLES and 
                        class_name not in BLACKLIST_CLASSES):
                        if not window.has_style(win32con.WS_EX_TOOLWINDOW):
                            windows.append({
                                'hwnd': window.handle,
                                'title': title,
                                'class': class_name,
                                'pid': window.process_id()
                            })
        except Exception:
            continue

    return windows

def get_window_thumbnail(hwnd, max_width=200, max_height=150):
    """
    Capture a thumbnail of a specific window.

    Args:
        hwnd (int): Window handle
        max_width (int, optional): Maximum width of the thumbnail
        max_height (int, optional): Maximum height of the thumbnail

    Returns:
        PIL.Image: Thumbnail image of the window or None if capture fails
    """
    try:
        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        is_minimized = win32gui.IsIconic(hwnd)
        if is_minimized:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        if max_width and max_height:
            img.thumbnail((max_width, max_height), Image.LANCZOS)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if is_minimized:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

        return img

    except Exception:
        return None
import ctypes
import time
import platform

user32 = ctypes.windll.user32
SW_RESTORE = 9
SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001
SPIF_SENDCHANGE = 2
VK_MENU = 0x12  # ALT key (for focus trick)

def force_focus(hwnd):
    """Force focus to a window by bypassing SetForegroundWindow restrictions."""
    if platform.system() != 'Windows':
        return False

    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)

    if user32.GetForegroundWindow() == hwnd:
        return True

    foreground_thread_id = user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), None)
    this_thread_id = user32.GetWindowThreadProcessId(hwnd, None)

    if user32.AttachThreadInput(this_thread_id, foreground_thread_id, True):
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
        user32.AttachThreadInput(this_thread_id, foreground_thread_id, False)

        if user32.GetForegroundWindow() == hwnd:
            return True

    timeout = ctypes.c_int()
    zero = ctypes.c_int(0)

    if user32.SystemParametersInfoW(SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0):
        user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(zero), SPIF_SENDCHANGE)

    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)

    user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), SPIF_SENDCHANGE)

    if user32.GetForegroundWindow() == hwnd:
        return True

    # Bypass Focus by sending alt key
    user32.keybd_event(VK_MENU, 0, 0, 0)  # Press ALT
    time.sleep(0.05)
    user32.keybd_event(VK_MENU, 0, 2, 0)  # Release ALT

    return user32.GetForegroundWindow() == hwnd

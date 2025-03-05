import ctypes
from ctypes import wintypes
import threading
import atexit
from ui.overlay import AltTabOverlay

# Constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
VK_TAB = 0x09
VK_LMENU = 0xA4  # Left Alt
VK_RMENU = 0xA5  # Right Alt

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
user32 = ctypes.windll.user32

# Global variables
overlay = None
hook = None

def low_level_keyboard_handler(nCode, wParam, lParam):
    """Low-level keyboard hook handler to intercept key events and block Alt+Tab."""
    global overlay
    
    if nCode >= 0 and overlay is not None:
        key_struct = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong * 2)).contents
        key_code = key_struct[0] & 0xFF

        if key_code in (VK_LMENU, VK_RMENU):
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                overlay.alt_pressed = True
            elif wParam in (WM_KEYUP, WM_SYSKEYUP):
                overlay.alt_pressed = False
                if overlay.root.winfo_viewable():
                    overlay.root.after(10, overlay.activate_selected_window)
                    overlay.root.after(20, overlay.hide_overlay)

        if key_code == VK_TAB and overlay.alt_pressed:
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                overlay.tab_pressed = True
                if not overlay.root.winfo_viewable():
                    overlay.root.after(10, overlay.show_overlay)
                    overlay.root.after(10, overlay.next_window)
                else:
                    overlay.root.after(10, overlay.next_window)
            elif wParam in (WM_KEYUP, WM_SYSKEYUP):
                overlay.tab_pressed = False
            return 1  # Block the event

    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

def hook_thread():
    """Runs the keyboard hook in a separate thread."""
    set_keyboard_hook()
    msg = wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), 0, 0, 0) > 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageA(ctypes.byref(msg))

def set_keyboard_hook():
    """Set up the low-level keyboard hook."""
    global hook
    hook_proc = HOOKPROC(low_level_keyboard_handler)
    set_keyboard_hook.hook_proc = hook_proc  # Prevent garbage collection
    hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, hook_proc, None, 0)
    if not hook:
        raise ctypes.WinError()

def remove_keyboard_hook():
    """Remove the low-level keyboard hook."""
    global hook
    if hook:
        user32.UnhookWindowsHookEx(hook)
        hook = None

def cleanup():
    """Remove the keyboard hook and perform cleanup."""
    remove_keyboard_hook()

def main():
    global overlay
    overlay = AltTabOverlay()
    threading.Thread(target=hook_thread, daemon=True).start()
    overlay.run()
    cleanup()

atexit.register(cleanup)

if __name__ == "__main__":
    main()

import tkinter as tk
from PIL import ImageTk
import math

from utils.window_utils import get_window_thumbnail, get_windows_on_current_monitor
from utils.focus_utils import force_focus
from config.window_config import BLACKLIST_TITLES, BLACKLIST_CLASSES

import win32api
import win32con
import win32gui

class AltTabOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg='black')

        self.main_frame = tk.Frame(self.root, bg='#1A1A1A')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.thumbnails_frame = tk.Frame(self.main_frame, bg='#1A1A1A')
        self.thumbnails_frame.pack(fill=tk.BOTH, expand=True)

        self.info_var = tk.StringVar()
        self.info_label = tk.Label(
            self.main_frame, 
            textvariable=self.info_var, 
            font=('Segoe UI', 10), 
            fg='white', 
            bg='#1A1A1A'
        )
        self.info_label.pack(side=tk.BOTTOM, pady=10)

        self.current_index = 0
        self.windows = []
        self.current_monitor = None

        self.alt_pressed = False
        self.tab_pressed = False

    def get_active_monitor(self):
        """Get the monitor of the active window."""
        try:
            x, y = win32api.GetCursorPos()
            monitor = win32api.MonitorFromPoint((x, y), win32con.MONITOR_DEFAULTTONEAREST)
            return monitor
        except Exception:
            return win32api.MonitorFromWindow(0, win32con.MONITOR_DEFAULTTOPRIMARY)

    def center_overlay(self, monitor):
        """Dynamically center and resize the overlay based on open windows count."""
        try:

            self.windows = get_windows_on_current_monitor()

            num_windows = len(self.windows)

            monitor_info = win32api.GetMonitorInfo(monitor)
            monitor_rect = monitor_info['Monitor']

            screen_width = monitor_rect[2] - monitor_rect[0]
            screen_height = monitor_rect[3] - monitor_rect[1]

            if num_windows <= 4:
                cols, rows = num_windows, 1
            else:
                cols = min(5, math.ceil(math.sqrt(num_windows)))  # Dynamic column count, up to 5 max
                rows = math.ceil(num_windows / cols)


            thumb_width = int(screen_width * 0.15)
            thumb_height = int(screen_height * 0.2)

            overlay_width = cols * (thumb_width + 20)
            overlay_height = rows * (thumb_height + 20)

            x = monitor_rect[0] + (screen_width - overlay_width) // 2
            y = monitor_rect[1] + (screen_height - overlay_height) // 2

            self.root.geometry(f"{overlay_width}x{overlay_height}+{x}+{y}")

        except Exception:
            pass

    def create_thumbnail_grid(self):
        """Create a grid of thumbnails for active windows."""
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()

        self.windows = []
        self.current_monitor = self.get_active_monitor()

        def enum_windows_callback(hwnd, lParam):
            try:
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    window_monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)

                    if window_monitor == self.current_monitor:
                        window_title = win32gui.GetWindowText(hwnd)
                        window_class = win32gui.GetClassName(hwnd)

                        if (window_title not in BLACKLIST_TITLES and 
                            window_class not in BLACKLIST_CLASSES):
                            self.windows.append({
                                'hwnd': hwnd,
                                'title': window_title,
                                'class': window_class
                            })
            except Exception:
                pass

            return True

        win32gui.EnumWindows(enum_windows_callback, None)
        self.windows = self.windows[:10]

        columns = min(5, len(self.windows))

        for i, window in enumerate(self.windows):
            frame = tk.Frame(
                self.thumbnails_frame, 
                bg='#3A3A3A' if i == self.current_index else '#1A1A1A',
                borderwidth=2,
                relief=tk.RAISED if i == self.current_index else tk.FLAT
            )
            frame.grid(
                row=i // columns, 
                column=i % columns, 
                padx=10, 
                pady=10, 
                sticky='nsew'
            )

            self.thumbnails_frame.grid_columnconfigure(i % columns, weight=1)
            self.thumbnails_frame.grid_rowconfigure(i // columns, weight=1)

            try:
                thumbnail = get_window_thumbnail(window['hwnd'], max_width=200, max_height=100)
                if thumbnail:
                    thumbnail_tk = ImageTk.PhotoImage(thumbnail)

                    img_label = tk.Label(frame, image=thumbnail_tk, bg=frame['bg'])
                    img_label.image = thumbnail_tk
                    img_label.pack(expand=True, fill=tk.BOTH)

                    title_label = tk.Label(
                        frame, 
                        text=window['title'], 
                        font=('Segoe UI', 10), 
                        fg='white', 
                        bg=frame['bg']
                    )
                    title_label.pack(side=tk.BOTTOM, fill=tk.X)

            except Exception:
                pass

        if self.windows:
            selected_window = self.windows[self.current_index]
            self.info_var.set(f"{selected_window['title']} - {selected_window['class']}")

    def show_overlay(self):
        """Show the overlay and update the thumbnails."""
        try:
            self.current_index = 0
            current_monitor = self.get_active_monitor()
            self.center_overlay(current_monitor)
            self.create_thumbnail_grid()

            self.root.deiconify()  
            self.root.lift()  
            self.root.focus_force()
        except Exception:
            pass

    def hide_overlay(self):
        """Hide the overlay."""
        self.root.withdraw()

    def next_window(self):
        """Select next window."""
        if self.windows:
            self.current_index = (self.current_index + 1) % len(self.windows)
            self._update_grid_highlight()

    def previous_window(self):
        """Select previous window."""
        if self.windows:
            self.current_index = (self.current_index - 1 + len(self.windows)) % len(self.windows)
            self._update_grid_highlight()

    def _update_grid_highlight(self):
        """Update grid highlighting without full refresh."""
        for i, frame in enumerate(self.thumbnails_frame.winfo_children()):
            if i == self.current_index:
                frame.configure(bg='#3A3A3A', relief=tk.RAISED)
                for child in frame.winfo_children():
                    child.configure(bg='#3A3A3A')
            else:
                frame.configure(bg='#1A1A1A', relief=tk.FLAT)
                for child in frame.winfo_children():
                    child.configure(bg='#1A1A1A')

        if self.windows:
            selected_window = self.windows[self.current_index]
            self.info_var.set(f"{selected_window['title']} - {selected_window['class']}")

    def activate_selected_window(self):
        """Activate the currently selected window."""
        if self.windows:
            selected_window = self.windows[self.current_index]
            try:
                force_focus(selected_window['hwnd'])
                self.hide_overlay()
            except Exception:
                pass

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()
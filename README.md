# Alt+Tab Manager

A customizable Alt+Tab replacement for Windows, built with Python. This tool provides an enhanced Alt+Tab experience with window thumbnails, multi-monitor support, and blacklist functionality. The Alt+Tab Manager only displays applications on the currently active monitor.

---

## Features

- **Window Thumbnails**: Displays live thumbnails of open windows.
- **Multi-Monitor Support**: Works seamlessly across multiple monitors.
- **Blacklist**: Exclude specific windows or applications from the Alt+Tab list.
- **Customizable UI**: Modern and customizable overlay UI.
- **Low-Level Keyboard Hook**: Intercepts and replaces the default Alt+Tab behavior.

---

## Installation

### Prerequisites

- Python 3.8 or higher (tested on Python 3.13)
- Windows OS (tested on Windows 10)

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/ranggaggngntt/alt-tab-manager.git
   cd alt-tab-manager
   ```
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```sh
   python index.py
   ```

---

## Usage

- Press **Alt + Tab** to open the overlay.
- Use **Tab** to cycle through open windows.
- Release **Alt** to switch to the selected window.

---

## Blacklist Configuration

To exclude specific windows or applications from the Alt+Tab list, edit the `BLACKLIST_TITLES` and `BLACKLIST_CLASSES` lists in `config/window_config.py`.

### Example:
```python
BLACKLIST_TITLES = ["Calculator", "Settings"]
BLACKLIST_CLASSES = ["Shell_TrayWnd", "WorkerW"]
```

---

## To-Do

Here are some planned improvements and bug fixes:

- [ ]  **Fix Tab Width and Height**: Ensure all thumbnails are the same size for a consistent look.
- [ ]  **Fix Full-Screen Applications**: Address issues with full-screen applications (e.g., games) requiring manual clicking.
- [ ]  **Create an Installer**: Develop an installer for easier installation and setup.
- [ ]  **Fix Cursor Loading Bug**: Resolve the issue where the cursor shows a loading icon after using Alt+Tab (fixed by moving the mouse).
- [ ]  **Increase Window Limit**: Allow more than 10 windows to be displayed on the active monitor.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
   ```sh
   git checkout -b feature/YourFeatureName
   ```
3. **Commit your changes**:
   ```sh
   git commit -m "Add some feature"
   ```
4. **Push to the branch**:
   ```sh
   git push origin feature/YourFeatureName
   ```
5. **Open a pull request**.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **pywinauto** for window management.
- **pynput** for Mouse and Keyboard Listener.
- **Pillow** for image processing.
- **ctypes** for Windows API integration.
- **tkinter** for creating UI Overlay.

---

## Support

If you encounter any issues or have questions, please open an issue.

---

## Author

**Rangga**  
📧 Email: ranggaa.dwi@hotmail.com
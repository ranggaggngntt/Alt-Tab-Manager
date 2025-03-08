#include "pch.h"
#include <windows.h>

HWND g_targetHwnd = NULL;

extern "C" __declspec(dllexport) void SetTargetWindow(HWND hwnd) {
    g_targetHwnd = hwnd;
}

extern "C" __declspec(dllexport) void ForceFocus() {
    if (g_targetHwnd) {
        ShowWindow(g_targetHwnd, SW_SHOWMINIMIZED);
        ShowWindow(g_targetHwnd, SW_RESTORE);
        SetForegroundWindow(g_targetHwnd);
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}

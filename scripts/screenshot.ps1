Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win32 {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, IntPtr dwExtraInfo);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern IntPtr GetDlgItem(IntPtr hWnd, int nIDDlgItem);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool RedrawWindow(IntPtr hWnd, IntPtr lprcUpdate, IntPtr hrgnUpdate, uint flags);
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
    public const uint WM_LBUTTONDOWN = 0x0201;
    public const uint WM_LBUTTONUP = 0x0202;
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
}
"@

# Get handle from command line arg (or find cursor-setup window)
$handle = [IntPtr]::Zero
if ($args[0] -and $args[0] -match '^\d+$') {
    $handle = [IntPtr][int64]$args[0]
} else {
    $script:windows = @()
    $targetPid = [uint32](Get-Process cursor-setup-wpf -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id)
    if ($targetPid -eq 0) { Write-Error "cursor-setup-wpf not running"; exit 1 }
    $enum = [Win32+EnumWindowsProc]{
        param($hWnd, $lParam)
        $procId = 0
        [void][Win32]::GetWindowThreadProcessId($hWnd, [ref]$procId)
        if ($procId -eq $script:targetPid -and [Win32]::IsWindowVisible($hWnd)) {
            $len = [Win32]::GetWindowTextLength($hWnd)
            $sb = New-Object System.Text.StringBuilder ($len + 1)
            [void][Win32]::GetWindowText($hWnd, $sb, $sb.Capacity)
            $script:windows += [PSCustomObject]@{ Handle=$hWnd; Title=$sb.ToString() }
        }
        return $true
    }
    [void][Win32]::EnumWindows($enum, [IntPtr]::Zero)
    $main = $script:windows | Select-Object -First 1
    if (-not $main) { Write-Error "window not found"; exit 1 }
    $handle = $main.Handle
    Write-Host "Found: '$($main.Title)' handle=$handle"
}

# Restore and resize
[void][Win32]::ShowWindow($handle, 1)  # SW_SHOWNORMAL
Start-Sleep -Milliseconds 400
[void][Win32]::MoveWindow($handle, 60, 60, 1200, 880, $true)
Start-Sleep -Milliseconds 700

# Tab click if specified (e.g., "tab=1")
if ($args[1] -and $args[1] -like "tab=*") {
    $tabIdx = [int]$args[1].Replace("tab=", "")
    # Tab strip: header=96px, tabs start at y=96, each tab ~140px wide, padding=20
    # Tab y center = 96 + 21 = 117
    $cx = 70 + ($tabIdx * 140)
    $cy = 117
    [void][Win32]::SetCursorPos(60 + $cx, $cy)
    Start-Sleep -Milliseconds 200
    [void][Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, [IntPtr]::Zero)
    [void][Win32]::mouse_event([Win32]::MOUSEEVENTF_LEFTUP, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 1200
}

# Get window rect and capture
$rect = New-Object Win32+RECT
[void][Win32]::GetWindowRect($handle, [ref]$rect)
$w = $rect.Right - $rect.Left
$h = $rect.Bottom - $rect.Top
Write-Host "Window: $($rect.Left),$($rect.Top) ${w}x${h}"

$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($rect.Left, $rect.Top, 0, 0, $bmp.Size)
$out = $args[2]
if (-not $out) { $out = "d:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR\_previews\gui.png" }
$bmp.Save($out)
Write-Host "Saved: $out"

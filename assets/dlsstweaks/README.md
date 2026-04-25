# DLSSTweaks Assets

This folder contains the DLSSTweaks release files used by the panel:

```text
dxgi.dll
dlsstweaks.ini
```

The panel copies `dxgi.dll` to the game Win64 folder as:

```text
winmm.dll
```

Do not rename the asset file here. The rename happens during install.

If you update DLSSTweaks:

1. Replace `dxgi.dll`.
2. Replace `dlsstweaks.ini`.
3. Start the panel and install to a test folder first.
4. Confirm `dlsstweaks.log` contains `WINMM.dll wrapper loaded`.

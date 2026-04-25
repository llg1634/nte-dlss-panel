# Third-Party Notices

This project wraps and automates DLSSTweaks for a specific game workflow.

## DLSSTweaks

- Upstream author: emoose
- Upstream project/release page: https://www.nexusmods.com/site/mods/550
- Source repository note: https://github.com/emoose/DLSSTweaks
- License: MIT License

The files under `assets/dlsstweaks/` come from a DLSSTweaks release:

```text
assets/dlsstweaks/dxgi.dll
assets/dlsstweaks/dlsstweaks.ini
```

The tool copies `dxgi.dll` as `winmm.dll` into the selected game Win64 folder because `dxgi.dll` was detected by the target game during testing, while `winmm.dll` was the working wrapper entry for this game.

## NVIDIA / DLSS

This project does not include NVIDIA DLSS DLLs. It relies on the user's installed NVIDIA driver and NGX runtime.

The NVIDIA DLSS HUD toggle writes this registry value:

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

This registry value only controls HUD visibility. It does not set the DLSS render scale.

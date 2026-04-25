# NTE DLSS Panel

Chinese-first local WebUI for applying the tested DLSSTweaks `winmm.dll` workflow to Neverness To Everness / Ananta.

Keywords: Neverness To Everness, NTE, Ananta, DLSS, DLSSTweaks, NVIDIA DLSS HUD, DLSS render scale, DLSS low resolution, winmm.dll wrapper, local WebUI.

Chinese README: [README.md](README.md)

## What It Does

This tool starts a local-only WebUI at:

```text
http://127.0.0.1:22532
```

It detects the Neverness To Everness / Ananta game folder, backs up existing files, installs the DLSSTweaks wrapper as `winmm.dll`, writes `dlsstweaks.ini`, and provides a manifest-based restore flow.

## Scope

The DLSS render scale override is local to the selected game folder:

```text
<Game>\Client\WindowsNoEditor\HT\Binaries\Win64\dlsstweaks.ini
```

The tool does not write NVIDIA App / DRS `GlobalForcedScale`.

The only NVIDIA global value it can write is the DLSS HUD registry toggle:

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

That registry value only controls DLSS HUD visibility. It does not control render scale.

## Third-Party Notice

This project is not DLSSTweaks itself and is not an official NVIDIA tool.

It is a Chinese local WebUI and automation wrapper around DLSSTweaks, specifically documenting and automating the tested Neverness To Everness / Ananta path:

```text
winmm.dll + dlsstweaks.ini
```

DLSSTweaks is authored by emoose:

```text
https://www.nexusmods.com/site/mods/550
https://github.com/emoose/DLSSTweaks
```

Files under `assets/dlsstweaks/` come from a DLSSTweaks release:

```text
assets/dlsstweaks/dxgi.dll
assets/dlsstweaks/dlsstweaks.ini
```

The panel copies `dxgi.dll` as `winmm.dll` into the selected game Win64 folder because `dxgi.dll` was detected by the target game during testing, while `winmm.dll` was the working wrapper entry.

Please keep `NOTICE.md` and the MIT License attribution when redistributing this project.

## Quick Start

Source version:

```text
Double-click run.bat
```

If the DLSS HUD toggle needs administrator permission:

```text
Double-click run_as_admin.bat
```

Packaged release:

```text
Run NTEDLSSPanel.exe
```

If the HUD toggle needs administrator permission:

```text
Run run_exe_as_admin.bat
```

Then open:

```text
http://127.0.0.1:22532
```

Basic flow:

1. Select the game root, for example `<game install folder>`.
2. Click detect.
3. Choose a ratio, commonly `0.30` or `0.315`.
4. Keep all four DLSS quality levels synced unless you know the exact mapping.
5. Install/update.
6. Fully restart the game.
7. Enable DLSS in game and verify with the DLSS HUD.

## Successful Log Markers

After restarting the game, `dlsstweaks.log` should contain:

```text
WINMM.dll wrapper loaded
DLSS functions found & parameter hooks applied
```

## Restore

Every install creates:

```text
<Win64>\_nte_dlss_backups\<timestamp>
```

Restore uses `manifest.json` from the selected backup folder and attempts to return the game folder to the state before that install.

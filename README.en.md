# NTE DLSS 4.5 One-Click Low Render Scale Panel

Chinese-first local WebUI for Neverness To Everness / Ananta DLSS 4.x / DLSS 4.5 one-click low render scale deployment. It targets 33%-below, sub-720p, 680p, 648p, 540p, and 25%-30% render scale experiments at 4K output, using the tested DLSSTweaks `winmm.dll + dlsstweaks.ini` workflow.

Keywords: Neverness To Everness, Ananta, NTE, NTE DLSS Panel, NTE DLSS one click, NTE DLSS one click deploy, DLSS 4, DLSS 4.5, DLSS L model, NVIDIA NGX, NVIDIA DLSS HUD, DLSSTweaks, dlsstweaks.ini, winmm.dll wrapper, dxgi.dll detected, DLSS render scale, low render scale, 33% render scale, sub-720p DLSS, 540p to 4K, 648p to 4K, 680p to 4K, 25% render scale, 30% render scale, Unreal Engine 5, UE5, local WebUI.

Chinese README: [README.md](README.md)

## Search Queries

Neverness To Everness DLSS one click, NTE DLSS one click deploy, Neverness To Everness DLSS 4.5, Ananta DLSS 4.5, NTE DLSS low render scale, NTE sub-720p DLSS, NTE 33% render scale, NTE 540p to 4K, NTE 25% render scale, NTE 30% render scale, Neverness To Everness DLSSTweaks, Ananta winmm.dll wrapper, DLSS 540p to 4K, DLSS 648p to 4K, DLSS 680p to 4K, DLSS L model, NVIDIA NGX, DLSSTweaks winmm wrapper, Unreal Engine 5 DLSS.

## Project Positioning

This is not a generic one-click DLSS deployment tool. It packages one tested Neverness To Everness / Ananta workflow into a reusable local panel:

- Neverness To Everness / Ananta is a newer UE5 game, and its DLSS loading path is not identical to every other game.
- DLSS 4.x / 4.5 with the L model can make very low input resolutions more usable when upscaling to 4K, so sub-720p render scale testing is meaningful.
- The normal game or NVIDIA App path usually bottoms out around 33%, which is roughly 720p at 4K output.
- Dropping `dxgi.dll` directly was detected by the game during testing; the working path was `winmm.dll + dlsstweaks.ini`.
- This tool only automates that NTE / Ananta tested path with a local WebUI, backup, restore, DLSS HUD verification, and a WebUI shutdown button.

## What It Does

This NTE / Ananta focused tool starts a local-only WebUI at:

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

This project is not DLSSTweaks itself, is not an official NVIDIA tool, and is not meant to be a generic DLSS mod manager.

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

## Frontend vs Backend Service

The browser page is only the WebUI frontend. The actual local backend is `NTEDLSSPanel.exe` or `python app.py`, which listens on `127.0.0.1:22532` and performs folder selection, file writes, backup/restore, and the DLSS HUD toggle.

Closing the browser tab does not stop the backend process. Use the WebUI `退出工具` / shutdown button in the top-right corner to stop the local service. If the page is already closed, open `http://127.0.0.1:22532` again and click the shutdown button, or end `NTEDLSSPanel.exe` from Task Manager.

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

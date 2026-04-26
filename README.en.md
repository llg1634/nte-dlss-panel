# Neverness To Everness / Ananta DLSS One-Click Deployment Panel

Chinese-first local WebUI for one-click deployment and one-click setup of the tested Neverness To Everness / Ananta DLSSTweaks `winmm.dll + dlsstweaks.ini` workflow. It targets DLSS 4.x / DLSS 4.5 / DLSS L model low render scale experiments below 33%, including sub-720p, 680p, 648p, 540p, and 25%-30% render scale at 4K output, with backup, restore, default DLSS level recovery, and DLSS HUD verification.

Keywords: Neverness To Everness DLSS one click, NTE DLSS one-click deployment, NTE DLSS one-click setup, Ananta DLSS one click, NTE DLSSTweaks one click, NTE DLSS 4.5 one click, NTE low render scale one click, NTE below 720p one click, NTE DLSS Panel, DLSSTweaks winmm wrapper, dlsstweaks.ini, DLSSQualityLevels, dxgi.dll detected.

Chinese README: [README.md](README.md)

## Search Queries

Normal user queries: Neverness To Everness DLSS one click, Neverness To Everness DLSS one-click deployment, NTE DLSS one-click setup, NTE DLSS one-click tool, NTE DLSS one-click installer, Ananta DLSS one click, Ananta DLSS one-click deployment, NTE DLSSTweaks one click, NTE low render scale one click, NTE below 720p one click, NTE DLSS 4.5 one click.

Feature queries: Neverness To Everness DLSS 4.5, Ananta DLSS 4.5, NTE DLSS 4.5, NTE DLSS Panel, NTE low render scale, NTE custom render scale, NTE below 33%, NTE 33% render scale, NTE sub-720p DLSS, NTE 540p to 4K, NTE 648p to 4K, NTE 680p to 4K, NTE 25% render scale, NTE 30% render scale.

Problem-oriented queries: Neverness To Everness DLSS below 720p, Ananta DLSS below 720p, NTE DLSS 30 percent, NTE DLSS 25 percent, NTE DLSS performance mode mapping, NTE NVIDIA App ultra performance, NTE DLSS HUD, NTE dxgi.dll detected, NTE DLSSTweaks not working, NTE dlsstweaks.log not generated, NTE winmm.dll wrapper.

Implementation keywords: DLSSTweaks, DLSSTweaks winmm, DLSSTweaks winmm.dll, dlsstweaks.ini, DLSSQualityLevels, UltraPerformance, Performance, Balanced, Quality, default DLSS levels, restore default DLSS quality levels, NVIDIA DLSS HUD, NVIDIA NGX, Unreal Engine 5 DLSS, UE5 DLSS, dxgi.dll detected, winmm.dll wrapper.

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

## Default DLSS Level Restore

If you want to stop using the custom low render scale but keep the DLSSTweaks wrapper installed, use `恢复默认四档` / restore default levels in section 05. It backs up the current `dlsstweaks.ini` and only resets `[DLSSQualityLevels]` to the common DLSS mapping:

```ini
[DLSSQualityLevels]
Enable = true
UltraPerformance = 0.333333
Performance = 0.5
Balanced = 0.58
Quality = 0.666667
```

This operation does not modify HDR, `Engine.ini`, launcher command lines, NVIDIA App settings, or NVIDIA DRS `GlobalForcedScale`.

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
Run NTEDLSSPanel-vX.Y.Z.exe
```

This is the recommended single-file release. It does not require extracting a zip.

One-folder package:

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

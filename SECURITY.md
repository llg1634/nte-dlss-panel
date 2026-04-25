# Security

This is a local Windows utility. It should only bind to:

```text
127.0.0.1:22532
```

Do not expose the panel to a LAN or public network.

## File Operations

The tool writes only inside the selected game Win64 folder, except for the optional NVIDIA DLSS HUD toggle.

The HUD toggle writes:

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

## Reporting Issues

When reporting a problem, include:

- Windows version.
- GPU and driver version.
- Game install path, with personal account names removed if needed.
- Whether `winmm.dll`, `dlsstweaks.ini`, and `dlsstweaks.log` exist in the game Win64 folder.
- The last 80 lines of `dlsstweaks.log`.

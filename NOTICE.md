# 第三方声明 / Third-Party Notices

本项目不是 DLSSTweaks 本体，也不是 NVIDIA 官方工具。它基于 DLSSTweaks 做中文本地 WebUI、自动化安装、备份和恢复，并针对异环（Neverness To Everness / Ananta）的实际加载路径整理出 `winmm.dll + dlsstweaks.ini` 方案。

This project is not DLSSTweaks itself and is not an official NVIDIA tool. It is a Chinese local WebUI and automation wrapper around DLSSTweaks for the tested Neverness To Everness / Ananta `winmm.dll + dlsstweaks.ini` workflow.

## DLSSTweaks

- 原作者：emoose
- 发布页：https://www.nexusmods.com/site/mods/550
- 源码说明页：https://github.com/emoose/DLSSTweaks
- 许可证：MIT License

`assets/dlsstweaks/` 下的文件来自 DLSSTweaks release：

```text
assets/dlsstweaks/dxgi.dll
assets/dlsstweaks/dlsstweaks.ini
```

工具安装时会把 `dxgi.dll` 复制为 `winmm.dll` 放入所选游戏 Win64 目录。这样做是因为实测 `dxgi.dll` 会被异环检测，而 `winmm.dll` 是可用入口。

The tool copies `dxgi.dll` as `winmm.dll` into the selected game Win64 folder because `dxgi.dll` was detected by the target game during testing, while `winmm.dll` was the working wrapper entry.

请在再分发时保留本声明和 MIT License 归属信息。

Please keep this notice and the MIT License attribution when redistributing this project.

## NVIDIA / DLSS

本项目不包含 NVIDIA DLSS DLL。运行时依赖用户本机 NVIDIA 驱动和 NGX 组件。

NVIDIA DLSS HUD 开关会写入：

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

这个注册表值只控制 HUD 显示，不控制 DLSS 渲染比例。

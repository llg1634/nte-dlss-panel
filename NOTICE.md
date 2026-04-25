# 第三方声明

本项目基于 DLSSTweaks 做自动化安装和恢复，针对异环的实际加载路径整理成 WebUI。

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

## NVIDIA / DLSS

本项目不包含 NVIDIA DLSS DLL。运行时依赖用户本机 NVIDIA 驱动和 NGX 组件。

NVIDIA DLSS HUD 开关会写入：

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

这个注册表值只控制 HUD 显示，不控制 DLSS 渲染比例。

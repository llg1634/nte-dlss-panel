# 安全说明

这是一个本机 Windows 工具。服务只应监听：

```text
127.0.0.1:22532
```

不要把面板暴露到局域网或公网。

## 文件操作

除可选的 NVIDIA DLSS HUD 开关外，工具只写入用户选择的游戏 Win64 目录。

HUD 开关写入：

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

## 反馈问题

反馈问题时建议包含：

- Windows 版本。
- 显卡型号和驱动版本。
- 游戏安装路径，可自行去掉个人账号名。
- Win64 目录里是否存在 `winmm.dll`、`dlsstweaks.ini`、`dlsstweaks.log`。
- `dlsstweaks.log` 最后 80 行。

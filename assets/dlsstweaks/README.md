# DLSSTweaks 资产

这个目录放面板使用的 DLSSTweaks release 文件：

```text
dxgi.dll
dlsstweaks.ini
```

面板安装时会把 `dxgi.dll` 复制到游戏 Win64 目录并改名为：

```text
winmm.dll
```

不要在这里手动改名。改名发生在安装流程里。

如果要更新 DLSSTweaks：

1. 替换 `dxgi.dll`。
2. 替换 `dlsstweaks.ini`。
3. 先用面板安装到测试目录。
4. 确认 `dlsstweaks.log` 包含 `WINMM.dll wrapper loaded`。

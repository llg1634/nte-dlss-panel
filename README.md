# 异环等 UE5 游戏 DLSS 4.5 自定义 33% 以下渲染分辨率一键部署工具

**搜索关键词**：异环 DLSS 一键、异环 DLSS 一键部署、NTE DLSS Panel、异环低渲染比例、异环 720p 以下、异环 DLSSTweaks 一键、异环 DLSS 4.5、异环 33% 以下分辨率。

异环（Neverness To Everness / Ananta）DLSS 4.x / DLSS 4.5 低渲染倍率本地 WebUI。它用于在 4K 输出下测试 33% 以下、720p 以下、680p、648p、540p、25%-30% render scale 等 DLSS 自定义比例，并把异环实测可用的 DLSSTweaks `winmm.dll + dlsstweaks.ini` 路径做成可备份、可恢复的一键流程。

English README: [README.en.md](README.en.md)

Local URL:

```text
http://127.0.0.1:22532
```

它不是在线服务，只在本机运行。本机网页负责选择游戏目录，Python / exe 后端负责文件检测、备份、写入和恢复。只关闭浏览器标签页不会退出后端服务，需要在面板里点“退出工具”。

## 搜索关键词 / Search Keywords

异环 DLSS 一键，异环 DLSS 一键部署，异环 DLSS 4.5，异环 DLSS 4，异环 33% 以下分辨率，异环低渲染比例，异环自定义渲染比例，异环 720p 以下，异环 540p 超分 4K，异环 25% 渲染倍率，异环 30% 渲染倍率，异环 DLSS 低分辨率，异环 DLSSTweaks 一键，异环 winmm.dll，异环 dxgi.dll detected，异环 DLSS HUD，异环 NVIDIA App 超级性能，异环性能档，异环 UE5 DLSS。

Neverness To Everness DLSS one click, NTE DLSS one click deploy, Neverness To Everness DLSS 4.5, Ananta DLSS 4.5, NTE DLSS Panel, NTE sub-720p DLSS, NTE low render scale, NTE 33% render scale, DLSS 540p to 4K, DLSS 648p to 4K, DLSS 680p to 4K, DLSS 25% render scale, DLSS 30% render scale, DLSS L model, NVIDIA NGX, DLSSTweaks winmm wrapper, dlsstweaks.ini, Unreal Engine 5 DLSS.

## 项目定位

这个项目的重点不是“通用一键部署”，而是把异环这个具体场景里的 DLSS 低倍率方案做成可复用流程：

- 异环（Neverness To Everness / Ananta）是 UE5 新游戏，DLSS 加载路径和普通游戏不完全一样。
- DLSS 4.x / 4.5 的 L 模型在低输入分辨率到 4K 输出时表现更强，所以 720p 以下的渲染倍率有实际测试价值。
- 游戏/NVIDIA App 常规入口通常只能到 33% 左右，4K 下约等于 720p。
- 直接放 `dxgi.dll` 会被异环检测，实测最终可用入口是 `winmm.dll + dlsstweaks.ini`。
- 本工具只把这个异环实测路径做成本地 WebUI、备份、恢复、HUD 验证和退出后端服务的流程。

## 第三方项目说明

本项目不是 DLSSTweaks 本体，也不是 NVIDIA 官方工具，也不是通用 DLSS Mod 管理器。它是专门给异环（Neverness To Everness / Ananta）整理的中文本地 WebUI 和自动化安装脚本，目标是把异环实测可用的 `winmm.dll + dlsstweaks.ini` 路径做成可恢复的一键流程。

DLSSTweaks 的原作者是 emoose，发布页是：

```text
https://www.nexusmods.com/site/mods/550
```

原始 GitHub / 源码说明页：

```text
https://github.com/emoose/DLSSTweaks
```

本仓库 `assets/dlsstweaks/` 中的 `dxgi.dll` 和 `dlsstweaks.ini` 来自 DLSSTweaks release。再分发时请保留本仓库的 [NOTICE.md](NOTICE.md) 和 DLSSTweaks 的 MIT License 说明。

## 文档导航

第一次使用建议按顺序看：

1. [快速使用](docs/01-快速使用.md)
2. [原理与试错路径](docs/02-原理与试错路径.md)
3. [备份、恢复与修改范围](docs/03-备份恢复与修改范围.md)
4. [常见问题](docs/05-常见问题.md)

## 项目特点

- 本机 WebUI：默认只监听 `127.0.0.1:22532`。
- 零配置路径检测：可选择异环根目录，也可选择 `HTGame.exe` 所在 Win64 目录。
- 局部比例修改：只写当前游戏目录的 `dlsstweaks.ini`，不修改 NVIDIA App / DRS 全局比例。
- 自动备份恢复：每次安装都会生成独立 manifest，恢复时按清单回滚。
- 默认四档恢复：可把 `UltraPerformance / Performance / Balanced / Quality` 恢复成常规 DLSS 映射，只改 `dlsstweaks.ini`。
- HUD 辅助验证：可开启/关闭 NVIDIA DLSS HUD，用于确认实际输入/输出分辨率。
- 后端退出按钮：网页前端和本地后端分离，关闭网页不会结束 exe；面板提供“退出工具”按钮关闭本地服务。

## 适用目标

异环官方/NVIDIA App 可调比例通常在 33% 到 100% 附近，4K 下 33% 约等于 720p。本工具主要用于写入 33% 以下的 DLSS 渲染比例，例如：

```text
0.30  ≈ 648p  适合 4K 下明显低于 720p
0.315 ≈ 680p  接近 680p
0.333 ≈ 720p  官方下限附近
0.05  ≈ 108p  只用于测试是否生效
```

公式：

```text
内部渲染高度 = 输出高度 × DLSS 比例
```

## 最终可用方案

最终生效方式是 `winmm.dll` 代理，不是 `dxgi.dll`。

工具会把 DLSSTweaks release 里的：

```text
assets\dlsstweaks\dxgi.dll
```

复制到游戏目录并改名为：

```text
<游戏目录>\Client\WindowsNoEditor\HT\Binaries\Win64\winmm.dll
```

同时写入：

```text
<游戏目录>\Client\WindowsNoEditor\HT\Binaries\Win64\dlsstweaks.ini
```

最终游戏 Win64 目录只需要保留：

```text
winmm.dll
dlsstweaks.ini
```

不要保留这些旧入口：

```text
dxgi.dll
nvngx.dll
XInput1_4.dll
```

工具安装时会自动清理这些旧入口。如果它们存在，会先备份再删除。

## 修改范围

渲染比例是局部修改，只写当前游戏目录：

```text
<游戏 Win64>\dlsstweaks.ini
```

面板不会修改 NVIDIA App / DRS 全局档案里的 `GlobalForcedScale`。如果之前用 DLSSTweaks Config 或 NVIDIA App 试过全局强制比例，建议恢复为 `0` 或默认值，避免影响其它 DLSS 游戏。

面板里唯一会写 NVIDIA 全局位置的是 DLSS HUD 开关：

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

它只控制 DLSS HUD 是否显示，不控制渲染比例。

## 档位映射

异环不同版本、不同入口或 NVIDIA App 配置下，实际调用的 DLSS 档位可能不同。

异环实测：游戏内“性能”更可能对应 `Performance`。
部分配置：可能仍会调用 `UltraPerformance`。
最稳妥方式：把四个档位写成同一个比例。

工具默认统一写入：

```ini
[DLSSQualityLevels]
Enable = true
UltraPerformance = 0.30
Performance = 0.30
Balanced = 0.30
Quality = 0.30
```

如果你明确知道异环当前配置调用哪个档位，可以在面板里关闭“四个 DLSS 档位使用同一个比例”，然后分别填写：

```text
UltraPerformance
Performance
Balanced
Quality
```

## 恢复默认四档映射

如果你只是想取消低倍率自定义，不想完全卸载 `winmm.dll` 代理，可以在 05 区域点击“恢复默认四档”。它会先备份当前 `dlsstweaks.ini`，然后只把 `[DLSSQualityLevels]` 改回常规 DLSS 映射：

```ini
[DLSSQualityLevels]
Enable = true
UltraPerformance = 0.333333
Performance = 0.5
Balanced = 0.58
Quality = 0.666667
```

这个操作不修改 HDR，不修改 `Engine.ini`，不修改启动器参数，也不修改 NVIDIA App / DRS 全局比例。它适合下面几种情况：

- 之前把四个档位都写成 `0.30`、`0.25` 或其它低倍率，现在想回到普通 DLSS 档位。
- 想保留 DLSSTweaks 代理和 HUD/日志验证能力，但暂时不用 33% 以下比例。
- 不确定当前游戏内“性能”到底映射到哪个档位，想先恢复到最接近原始 DLSS 档位的状态。

## 安装时会改什么

选择游戏目录并点击“按当前档位设置安装 / 更新”后，工具按顺序执行：

1. 定位 `HTGame.exe`。
2. 确认 Win64 目录。
3. 创建备份目录。
4. 备份同名文件。
5. 删除旧代理入口。
6. 写入 `winmm.dll`。
7. 写入 `dlsstweaks.ini`。
8. 删除旧 `dlsstweaks.log`，让游戏下次启动重新生成日志。

会处理的目录：

```text
<游戏目录>\Client\WindowsNoEditor\HT\Binaries\Win64
```

会写入或替换：

```text
winmm.dll
dlsstweaks.ini
```

会清理旧入口：

```text
dxgi.dll
nvngx.dll
XInput1_4.dll
```

会让游戏重新生成：

```text
dlsstweaks.log
```

## 备份位置

每次安装都会创建一个独立备份目录：

```text
<Win64>\_nte_dlss_backups\<时间戳>
```

示例：

```text
<游戏安装目录>\Client\WindowsNoEditor\HT\Binaries\Win64\_nte_dlss_backups\<时间戳>
```

备份目录里包含：

```text
manifest.json
winmm.dll              如果安装前存在
dlsstweaks.ini         如果安装前存在
dlsstweaks.log         如果安装前存在
dxgi.dll               如果安装前存在
nvngx.dll              如果安装前存在
XInput1_4.dll          如果安装前存在
```

`manifest.json` 记录这次安装时的比例、备份了哪些文件、清理了哪些文件、写入了哪些文件。恢复操作会读取这个清单。

## 恢复逻辑

面板里的“恢复所选备份”不是简单删除当前文件，而是按所选备份的 `manifest.json` 执行：

如果某个文件在安装前存在：从备份目录复制回 Win64。  
如果某个文件在安装前不存在：恢复时会删除当前工具创建的同名文件。  
如果备份里记录旧 `dxgi.dll` / `nvngx.dll` / `XInput1_4.dll`：会恢复它们。  
如果安装前没有这些旧入口：恢复后它们不会出现。

也就是说，恢复目标是“回到那次安装之前的状态”。

## 使用方法

推荐下载 Release 里的单文件版：

```text
NTEDLSSPanel-v版本号.exe
```

双击即可运行，不需要解压。如果 Windows 或杀软拦截，需要手动允许。

打包版：

```text
双击 NTEDLSSPanel.exe
```

如果 HUD 开关提示没有权限：

```text
双击 run_exe_as_admin.bat
```

源码方式：

```text
双击 run.bat
```

然后浏览器打开：

```text
http://127.0.0.1:22532
```

## 运行与退出

这个工具分成两层：

- 前端 WebUI：浏览器里的页面，只负责显示和发起操作。
- 后端服务：`NTEDLSSPanel.exe` 或 `python app.py`，负责监听 `127.0.0.1:22532`、选择文件夹、写入文件、备份恢复和 HUD 开关。

所以只关闭网页标签页，不会关闭后端服务，`22532` 端口也会继续被占用。需要退出时，在 WebUI 右上角点“退出工具”。如果页面已经关掉，也可以重新打开 `http://127.0.0.1:22532` 后再点“退出工具”；或者在任务管理器里结束 `NTEDLSSPanel.exe`。

页面步骤：

1. 点“浏览”。
2. 选择异环安装根目录，例如 `<游戏安装目录>`。
3. 点“检测路径”。
4. 选择比例，默认 `0.30`。
5. 点“按当前档位设置安装 / 更新”。
6. 完整退出游戏和启动器。
7. 重新进入游戏。
8. 回到面板点“刷新日志”。

成功日志应出现：

```text
WINMM.dll wrapper loaded
DLSS functions found & parameter hooks applied
```

日志位置：

```text
<Win64>\dlsstweaks.log
```

## NVIDIA DLSS HUD

面板集成了 DLSS HUD 检测和开关。它读写的注册表是：

```text
HKLM\SOFTWARE\NVIDIA Corporation\Global\NGXCore\ShowDlssIndicator
```

常见值：

```text
0       关闭
1024    开启，适用于所有 DLSS DLL
```

如果面板显示“没有权限写入”，用管理员方式启动：

```text
run_as_admin.bat
```

也可以单独运行脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\nvidia_dlss_hud.ps1 status
powershell -ExecutionPolicy Bypass -File scripts\nvidia_dlss_hud.ps1 on
powershell -ExecutionPolicy Bypass -File scripts\nvidia_dlss_hud.ps1 off
```

HUD 开启后，进游戏并启用 DLSS，屏幕角落应显示 DLSS 输入/输出信息。它用于确认实际分辨率是否低于 720p。

## Python

源码运行需要本机有 Python 3。

本项目没有运行时第三方 Python 依赖。打包工具 PyInstaller 只在构建机器上需要。

## 资产说明

`assets\dlsstweaks` 需要包含：

```text
dxgi.dll
dlsstweaks.ini
```

它们来自 DLSSTweaks release。这个 DLL 不需要按玩家显卡驱动版本单独匹配，运行时会加载玩家本机 NVIDIA NGX 组件。

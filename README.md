# NTE DLSS Panel

异环（Neverness To Everness）本地 DLSSTweaks WebUI。工具启动后监听：

```text
http://127.0.0.1:22532
```

它不是在线服务，只在本机运行。本机网页负责选择游戏目录，Python 后端负责文件检测、备份、写入和恢复。

## 文档导航

第一次使用建议按顺序看：

1. [快速使用](docs/01-快速使用.md)
2. [原理与试错路径](docs/02-原理与试错路径.md)
3. [备份、恢复与修改范围](docs/03-备份恢复与修改范围.md)
4. [常见问题](docs/05-常见问题.md)

如果你是项目维护者，先看：

1. [GitHub 上传指南](docs/04-GitHub上传指南.md)
2. [发布检查清单](docs/06-发布检查清单.md)

## 项目特点

- 本机 WebUI：默认只监听 `127.0.0.1:22532`。
- 零配置路径检测：可选择异环根目录，也可选择 `HTGame.exe` 所在 Win64 目录。
- 局部比例修改：只写当前游戏目录的 `dlsstweaks.ini`，不修改 NVIDIA App / DRS 全局比例。
- 自动备份恢复：每次安装都会生成独立 manifest，恢复时按清单回滚。
- HUD 辅助验证：可开启/关闭 NVIDIA DLSS HUD，用于确认实际输入/输出分辨率。

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

不同游戏实际调用的 DLSS 档位可能不同。

异环实测：游戏内“性能”更可能对应 `Performance`。  
有些游戏：可能调用 `UltraPerformance`。  
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

如果你明确知道某个游戏调用哪个档位，可以在面板里关闭“四个 DLSS 档位使用同一个比例”，然后分别填写：

```text
UltraPerformance
Performance
Balanced
Quality
```

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
E:\Neverness To Everness\Client\WindowsNoEditor\HT\Binaries\Win64\_nte_dlss_backups\20260425-135421-489
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

源码方式：

```text
双击 run.bat
```

然后浏览器打开：

```text
http://127.0.0.1:22532
```

页面步骤：

1. 点“浏览”。
2. 选择异环安装根目录，例如 `E:\Neverness To Everness`。
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

## Python 与打包

源码运行需要本机有 Python 3。

如果要发给没有 Python 的人，建议用 PyInstaller 打包成 exe，再发布 `dist` 里的成品。打包后仍然是本机 WebUI，只是用户不需要单独安装 Python。

本项目没有运行时第三方 Python 依赖。打包工具 PyInstaller 只在构建机器上需要。

## 资产说明

`assets\dlsstweaks` 需要包含：

```text
dxgi.dll
dlsstweaks.ini
```

它们来自 DLSSTweaks release。这个 DLL 不需要按玩家显卡驱动版本单独匹配，运行时会加载玩家本机 NVIDIA NGX 组件。

## Git 提交

```powershell
git init
git add nte-dlss-panel
git commit -m "Add NTE DLSS web panel"
```

公开发布前，建议在仓库说明里保留 DLSSTweaks 来源和第三方文件再分发说明。

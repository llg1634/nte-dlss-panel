# 更新日志

## 0.1.5

- 新增“恢复默认四档”功能：一键把 `UltraPerformance / Performance / Balanced / Quality` 写回常规 DLSS 映射。
- 默认四档映射为 `0.333333 / 0.5 / 0.58 / 0.666667`，用于取消低倍率自定义但保留 DLSSTweaks 代理。
- 检测结果和状态条会显示当前 `dlsstweaks.ini` 是默认映射还是自定义映射。
- 文档明确说明该恢复功能只修改当前游戏 Win64 目录的 `dlsstweaks.ini`，不会修改 HDR、`Engine.ini`、启动器参数或 NVIDIA 全局比例。

## 0.1.4

- 调整 WebUI 顶部操作区布局：01 选择游戏卡片不再被 02 渲染比例卡片撑高。
- 将 03 DLSS HUD 放到 01 选择游戏下方，左列底部与 02 渲染比例卡片底部齐平。
- 首页简介补充 01 到 05 的功能简述：选择游戏、设置比例、HUD 验证、安装步骤、日志与备份恢复。
- 比例圆环保持只显示当前比例，避免放入额外说明造成视觉干扰。

## 0.1.3

- 强化中文项目名：`异环等 UE5 游戏 DLSS 4.5 自定义 33% 以下渲染分辨率一键部署工具`。
- README 顶部新增醒目中文搜索行，覆盖“异环 DLSS 一键”“异环 DLSS 一键部署”“异环 DLSSTweaks 一键”等玩家常用搜索词。
- 同步更新英文 README、发布指南和发布检查清单中的项目标题与搜索描述。
- Release 新增单文件 exe，普通用户可直接下载运行，不必下载 zip 后解压。

## 0.1.2

- 重写 README 第一屏定位，强调异环 / Neverness To Everness / Ananta、DLSS 4.x / 4.5、L 模型、720p 以下、540p 到 4K、25%-30% 渲染倍率等搜索场景。
- 新增中英文搜索关键词段，覆盖 `sub-720p DLSS`、`low render scale`、`DLSSTweaks winmm wrapper`、`UE5` 等关键词。
- WebUI 新增“退出工具”按钮，可从页面关闭本地后端服务，避免只关网页后 exe 仍在后台运行。
- README、快速使用和常见问题补充“前端 WebUI 与后端服务不是同一个进程”的说明。

## 0.1.1

- 补充英文 README：`README.en.md`。
- 在中文 README 顶部补充异环相关英文关键词，方便搜索和非中文用户理解项目用途。
- 强化 DLSSTweaks 第三方归属说明，明确本项目是围绕 DLSSTweaks 的异环专用 WebUI/自动化封装，不是 DLSSTweaks 本体，也不是通用 DLSS Mod 管理器。
- 修复 `--noconsole` 打包版因无 stdout 导致 HTTP 接口断连的问题。
- 发布 Windows 打包版 zip，包含 `NTEDLSSPanel.exe`、管理员启动脚本和用户文档。

## 0.1.0

- 新增本机 WebUI，默认监听 `127.0.0.1:22532`。
- 新增异环 / `HTGame.exe` 路径检测。
- 新增 DLSSTweaks `winmm.dll` 安装流程。
- 新增每次安装独立备份 manifest 和恢复流程。
- 新增 DLSS 档位比例编辑。
- 新增 NVIDIA DLSS HUD 状态检测和开关。
- 新增最终可用路径和失败试错路径文档。

# GitHub 上传指南

这个项目目录已经按“可以直接上传”的方式整理好。

## 应该上传什么

上传仓库根目录中的这些内容：

```text
app.py
web/
assets/
scripts/
docs/
.github/
README.md
LICENSE
NOTICE.md
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
requirements.txt
run.bat
run_as_admin.bat
build_exe.bat
.gitignore
.gitattributes
```

不要上传：

```text
_local_backups/
__pycache__/
dist/
build/
*.spec
*.log
```

## 只用 GitHub 网页上传

适合只注册了 GitHub、不会用命令行的人。

1. 打开 GitHub。
2. 点右上角 `+`。
3. 点 `New repository`。
4. Repository name 填 `nte-dlss-panel` 或你自己的项目名。
5. Description 填：

```text
Chinese local WebUI for the tested DLSSTweaks winmm.dll workflow in Neverness To Everness / Ananta.
```

6. 选择 `Public` 或 `Private`。
7. 不要勾选 `Add a README file`，因为本目录已经有 README。
8. 点 `Create repository`。
9. 进入空仓库页面后，点 `uploading an existing file`。
10. 把本文件夹里的所有文件和文件夹拖进去。
11. Commit message 写：

```text
Initial release
```

12. 点 `Commit changes`。

## 用 Git 命令上传

如果本机安装了 Git：

```powershell
cd <仓库文件夹>
git init
git add .
git commit -m "Initial release"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

## 发布 exe

源码上传后，普通用户仍需要 Python。要让用户免 Python，构建 exe：

```text
双击 build_exe.bat
```

构建完成后，把 `dist\NTEDLSSPanel` 打包成 zip，然后在 GitHub：

1. 点右侧 `Releases`。
2. 点 `Draft a new release`。
3. Tag 写 `v0.1.0`。
4. Title 写 `异环 DLSS Panel v0.1.0`。
5. 上传 zip。
6. 发布。

## README 应该写什么

README 至少包含：

- 项目是做什么的。
- 支持什么游戏和系统。
- 一句话说明最终生效方式。
- 快速使用步骤。
- 备份和恢复说明。
- 修改范围。
- 常见问题链接。
- 第三方项目声明。

本仓库已经包含这些内容。

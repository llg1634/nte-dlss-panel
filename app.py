from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
import winreg
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


APP_DIR = Path(__file__).resolve().parent
WEB_DIR = APP_DIR / "web"
ASSET_DIR = APP_DIR / "assets" / "dlsstweaks"
ASSET_DLL = ASSET_DIR / "dxgi.dll"
ASSET_INI = ASSET_DIR / "dlsstweaks.ini"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 22532

PROXY_DLL = "winmm.dll"
STALE_PROXY_FILES = ("dxgi.dll", "nvngx.dll", "XInput1_4.dll")
MANAGED_FILES = (PROXY_DLL, "dlsstweaks.ini", "dlsstweaks.log", *STALE_PROXY_FILES)
DLSS_LEVELS = ("UltraPerformance", "Performance", "Balanced", "Quality")
UNCHANGED_QUALITY_LEVELS = {"DLAA": "1", "UltraQuality": "0"}
HUD_REGISTRY_PATH = r"SOFTWARE\NVIDIA Corporation\Global\NGXCore"
HUD_REGISTRY_VALUE = "ShowDlssIndicator"
HUD_ENABLED_VALUE = 0x400
HUD_DISABLED_VALUE = 0


def safe_console_log(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    if stream is None:
        return
    try:
        stream.write(message + "\n")
        stream.flush()
    except Exception:
        pass


class AppError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def now_id() -> str:
    stamp = datetime.now()
    return stamp.strftime("%Y%m%d-%H%M%S") + f"-{stamp.microsecond // 1000:03d}"


def as_text_path(path: Path | str | None) -> str | None:
    if path is None:
        return None
    return str(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def normalize_ratio(value: object) -> tuple[float, str]:
    if value is None or str(value).strip() == "":
        raise AppError("请输入 DLSS 比例，例如 0.30 或 31.5%。")
    raw = str(value).strip().replace("%", "")
    try:
        ratio = float(raw)
    except ValueError as exc:
        raise AppError("DLSS 比例不是有效数字。") from exc

    if ratio > 1:
        ratio = ratio / 100.0
    if ratio < 0.01 or ratio > 1.0:
        raise AppError("DLSS 比例需要在 0.01 到 1.00 之间。")

    if abs(ratio - 0.30) < 0.0005:
        display = "0.30"
    elif abs(ratio - 0.315) < 0.0005:
        display = "0.315"
    else:
        display = f"{ratio:.4f}".rstrip("0").rstrip(".")
    return ratio, display


def normalize_ratio_map(value: object) -> dict[str, str]:
    if isinstance(value, dict):
        fallback = value.get("default") or value.get("ratio") or "0.30"
        return {level: normalize_ratio(value.get(level, fallback))[1] for level in DLSS_LEVELS}

    _, ratio_text = normalize_ratio(value)
    return {level: ratio_text for level in DLSS_LEVELS}


def run_native_folder_dialog() -> str | None:
    if os.name != "nt":
        raise AppError("原生文件夹选择器只支持 Windows。")

    script = r"""
Add-Type -AssemblyName System.Windows.Forms
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = '选择异环安装根目录，或选择包含 HTGame.exe 的 Win64 文件夹'
$dialog.ShowNewFolderButton = $false
$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$form.ShowInTaskbar = $false
$form.Width = 1
$form.Height = 1
$form.StartPosition = 'CenterScreen'
$result = $dialog.ShowDialog($form)
if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    Write-Output $dialog.SelectedPath
}
"""
    proc = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-STA",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise AppError(proc.stderr.strip() or "文件夹选择器启动失败。")
    selected = proc.stdout.strip()
    return selected or None


def expand_user_path(value: str | None) -> Path:
    if not value or not value.strip():
        raise AppError("请选择或输入游戏路径。")
    cleaned = value.strip().strip('"')
    return Path(os.path.expandvars(cleaned)).expanduser()


def likely_htgame_path(base: Path) -> list[Path]:
    return [
        base / "HTGame.exe",
        base / "Client" / "WindowsNoEditor" / "HT" / "Binaries" / "Win64" / "HTGame.exe",
        base / "WindowsNoEditor" / "HT" / "Binaries" / "Win64" / "HTGame.exe",
        base / "HT" / "Binaries" / "Win64" / "HTGame.exe",
        base / "Binaries" / "Win64" / "HTGame.exe",
    ]


def limited_find_htgame(base: Path, limit: int = 160000) -> Path | None:
    if not base.is_dir():
        return None

    skipped = {
        "$RECYCLE.BIN",
        "System Volume Information",
        "Saved",
        "Logs",
        "UserData",
        "cef_cache_0",
    }
    checked = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skipped and not d.startswith(".")]
        checked += len(files)
        if "HTGame.exe" in files:
            return Path(root) / "HTGame.exe"
        if checked > limit:
            break
    return None


def detect_game(path_value: str | None) -> dict:
    base = expand_user_path(path_value)
    if not base.exists():
        raise AppError("路径不存在。")

    exe: Path | None = None
    if base.is_file():
        if base.name.lower() != "htgame.exe":
            raise AppError("请选择异环根目录、Win64 文件夹，或 HTGame.exe。")
        exe = base
    else:
        for candidate in likely_htgame_path(base):
            if candidate.is_file():
                exe = candidate
                break
        if exe is None:
            exe = limited_find_htgame(base)

    if exe is None:
        raise AppError("没有找到 HTGame.exe。请选择异环安装根目录或 Win64 文件夹。")

    win64 = exe.parent
    if win64.name.lower() != "win64":
        raise AppError("找到了 HTGame.exe，但它不在预期的 Win64 目录。")

    root = win64
    for _ in range(5):
        if root.name.lower() == "client":
            break
        root = root.parent

    return {
        "input": str(base),
        "gameRoot": str(root),
        "win64": str(win64),
        "exe": str(exe),
        "status": inspect_install(win64),
        "processes": running_processes(),
    }


def running_processes() -> list[dict]:
    if os.name != "nt":
        return []

    try:
        proc = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-Process HTGame,NTEGame,NTEBrowser,NTEWebBooster -ErrorAction SilentlyContinue | "
                "Select-Object ProcessName,Id,StartTime | ConvertTo-Json -Compress",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=6,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            return []
        data = json.loads(proc.stdout)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []


def read_hud_status() -> dict:
    if os.name != "nt":
        return {
            "available": False,
            "enabled": False,
            "value": None,
            "path": f"HKLM\\{HUD_REGISTRY_PATH}",
            "valueName": HUD_REGISTRY_VALUE,
            "message": "只支持 Windows NVIDIA DLSS HUD 注册表。"
        }

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, HUD_REGISTRY_PATH, 0, winreg.KEY_READ) as key:
            value, value_type = winreg.QueryValueEx(key, HUD_REGISTRY_VALUE)
        value_int = int(value)
        return {
            "available": True,
            "enabled": value_int != HUD_DISABLED_VALUE,
            "value": value_int,
            "mode": "EnabledAllDlls" if value_int == HUD_ENABLED_VALUE else ("Disabled" if value_int == 0 else "Custom"),
            "path": f"HKLM\\{HUD_REGISTRY_PATH}",
            "valueName": HUD_REGISTRY_VALUE,
            "message": "DLSS HUD 已开启。" if value_int != 0 else "DLSS HUD 未开启。",
        }
    except FileNotFoundError:
        return {
            "available": True,
            "enabled": False,
            "value": None,
            "mode": "Missing",
            "path": f"HKLM\\{HUD_REGISTRY_PATH}",
            "valueName": HUD_REGISTRY_VALUE,
            "message": "未找到 HUD 注册表值，开启时会自动创建。",
        }
    except PermissionError:
        return {
            "available": False,
            "enabled": False,
            "value": None,
            "path": f"HKLM\\{HUD_REGISTRY_PATH}",
            "valueName": HUD_REGISTRY_VALUE,
            "message": "没有权限读取 NVIDIA HUD 注册表。",
        }


def write_hud_status(enabled: bool) -> dict:
    if os.name != "nt":
        raise AppError("DLSS HUD 开关只支持 Windows。")

    try:
        access = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, HUD_REGISTRY_PATH, 0, access)
        with key:
            winreg.SetValueEx(
                key,
                HUD_REGISTRY_VALUE,
                0,
                winreg.REG_DWORD,
                HUD_ENABLED_VALUE if enabled else HUD_DISABLED_VALUE,
            )
    except PermissionError as exc:
        raise AppError("没有权限写入 NVIDIA HUD 注册表。请用管理员权限运行 run.bat 或打包后的 exe。", 403) from exc

    return read_hud_status()


def read_log_summary(log_path: Path) -> dict:
    if not log_path.is_file():
        return {
            "exists": False,
            "loaded": False,
            "hooks": False,
            "ratios": {},
            "tail": "",
        }

    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""

    ratio_matches = re.findall(r"-\s+([A-Za-z]+)\s+ratio:\s+([0-9.]+)", text)
    tail_lines = text.splitlines()[-120:]
    return {
        "exists": True,
        "size": log_path.stat().st_size,
        "modified": log_path.stat().st_mtime,
        "loaded": "WINMM.dll wrapper loaded" in text,
        "hooks": "DLSS functions found & parameter hooks applied" in text,
        "configUpdated": "Config updated from" in text,
        "ratios": {name: value for name, value in ratio_matches},
        "tail": "\n".join(tail_lines),
    }


def inspect_install(win64: Path) -> dict:
    files = {}
    asset_hash = sha256(ASSET_DLL) if ASSET_DLL.is_file() else None
    for name in MANAGED_FILES:
        target = win64 / name
        info = {"exists": target.exists()}
        if target.exists():
            stat = target.stat()
            info.update(
                {
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "sha256": sha256(target),
                }
            )
            if asset_hash:
                info["matchesDlsstweaksDll"] = info["sha256"] == asset_hash
        files[name] = info

    return {
        "assetsReady": ASSET_DLL.is_file() and ASSET_INI.is_file(),
        "proxyInstalled": (win64 / PROXY_DLL).is_file(),
        "iniInstalled": (win64 / "dlsstweaks.ini").is_file(),
        "staleProxyFiles": [name for name in STALE_PROXY_FILES if (win64 / name).exists()],
        "files": files,
        "log": read_log_summary(win64 / "dlsstweaks.log"),
        "backups": list_backups(win64),
    }


def list_backups(win64: Path) -> list[dict]:
    backup_root = win64 / "_nte_dlss_backups"
    if not backup_root.is_dir():
        return []
    rows = []
    for folder in sorted(backup_root.iterdir(), reverse=True):
        manifest = folder / "manifest.json"
        if manifest.is_file():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except Exception:
                data = {}
            rows.append(
                {
                    "name": folder.name,
                    "path": str(folder),
                    "created": data.get("created"),
                    "ratio": data.get("ratio"),
                    "ratios": data.get("ratios"),
                    "files": data.get("files", {}),
                    "operations": data.get("operations", []),
                }
            )
    return rows


def update_dlss_ini(template: str, ratios: dict[str, str]) -> str:
    section = "DLSSQualityLevels"
    desired = {"Enable": "true", **ratios, **UNCHANGED_QUALITY_LEVELS}
    lines = template.splitlines()
    out: list[str] = []
    in_section = False
    seen = set()

    for line in lines:
        header = re.match(r"^\s*\[([^\]]+)\]\s*$", line)
        if header:
            if in_section:
                for key, value in desired.items():
                    if key not in seen:
                        out.append(f"{key} = {value}")
                seen.clear()
            in_section = header.group(1).strip().lower() == section.lower()
            out.append(line)
            continue

        if in_section:
            key_match = re.match(r"^(\s*)([A-Za-z0-9_]+)(\s*=).*$", line)
            if key_match and key_match.group(2) in desired:
                key = key_match.group(2)
                out.append(f"{key_match.group(1)}{key}{key_match.group(3)} {desired[key]}")
                seen.add(key)
                continue
        out.append(line)

    if in_section:
        for key, value in desired.items():
            if key not in seen:
                out.append(f"{key} = {value}")
    elif not any(re.match(r"^\s*\[DLSSQualityLevels\]\s*$", line, re.I) for line in lines):
        out.extend(["", "[DLSSQualityLevels]"])
        for key, value in desired.items():
            out.append(f"{key} = {value}")

    return "\n".join(out).rstrip() + "\n"


def copy_to_backup(source: Path, backup_dir: Path) -> dict:
    record = {"path": str(source), "existed": source.exists()}
    if source.exists():
        backup_name = source.name
        backup_path = backup_dir / backup_name
        shutil.copy2(source, backup_path)
        record["backup"] = backup_name
        record["size"] = source.stat().st_size
        record["sha256"] = sha256(source)
    return record


def install_patch(path_value: str | None, ratio_value: object) -> dict:
    if not ASSET_DLL.is_file() or not ASSET_INI.is_file():
        raise AppError("缺少 DLSSTweaks 资产。需要 assets/dlsstweaks/dxgi.dll 和 dlsstweaks.ini。", 500)

    ratios = normalize_ratio_map(ratio_value)
    unique_ratios = sorted(set(ratios.values()))
    ratio_text = unique_ratios[0] if len(unique_ratios) == 1 else "mixed"
    detected = detect_game(path_value)
    win64 = Path(detected["win64"])

    backup_dir = win64 / "_nte_dlss_backups" / now_id()
    backup_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "tool": "nte-dlss-panel",
        "ratio": ratio_text,
        "ratios": ratios,
        "win64": str(win64),
        "backupDir": str(backup_dir),
        "files": {},
        "operations": [],
    }

    for name in MANAGED_FILES:
        target = win64 / name
        manifest["files"][name] = copy_to_backup(target, backup_dir)
        if target.exists():
            manifest["operations"].append(f"备份 {name}")

    for name in STALE_PROXY_FILES:
        target = win64 / name
        if target.exists():
            target.unlink()
            manifest["operations"].append(f"清理旧代理 {name}")

    log_path = win64 / "dlsstweaks.log"
    if log_path.exists():
        log_path.unlink()
        manifest["operations"].append("清理旧日志 dlsstweaks.log")

    shutil.copy2(ASSET_DLL, win64 / PROXY_DLL)
    manifest["operations"].append("写入 winmm.dll")
    template = ASSET_INI.read_text(encoding="utf-8", errors="replace")
    (win64 / "dlsstweaks.ini").write_text(update_dlss_ini(template, ratios), encoding="utf-8")
    manifest["operations"].append("写入 dlsstweaks.ini")

    (backup_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "ok": True,
        "message": "已安装 winmm.dll 代理并写入 dlsstweaks.ini。",
        "ratio": ratio_text,
        "ratios": ratios,
        "backup": str(backup_dir),
        "operations": manifest["operations"],
        "detected": detect_game(path_value),
    }


def restore_patch(path_value: str | None, backup_name: str | None = None) -> dict:
    detected = detect_game(path_value)
    win64 = Path(detected["win64"])
    backups = list_backups(win64)
    if not backups:
        raise AppError("没有找到可恢复的备份。")

    selected = backup_name or backups[0]["name"]
    backup_dir = win64 / "_nte_dlss_backups" / selected
    manifest_path = backup_dir / "manifest.json"
    if not manifest_path.is_file():
        raise AppError("备份清单不存在。")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for name, record in manifest.get("files", {}).items():
        target = win64 / name
        if record.get("existed") and record.get("backup"):
            shutil.copy2(backup_dir / record["backup"], target)
        elif target.exists() and name in MANAGED_FILES:
            target.unlink()

    return {
        "ok": True,
        "message": f"已恢复备份 {selected}。",
        "restoredBackup": str(backup_dir),
        "detected": detect_game(path_value),
    }


def common_game_candidates() -> list[Path]:
    candidates: list[Path] = []
    env_path = os.environ.get("NTE_GAME_PATH")
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend(Path(f"{drive}:\\Neverness To Everness") for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ")
    return candidates


def detect_common_game() -> dict | None:
    for candidate in common_game_candidates():
        try:
            if candidate.exists():
                return detect_game(str(candidate))
        except (AppError, OSError):
            continue
    return None


def api_state() -> dict:
    return {
        "assetsReady": ASSET_DLL.is_file() and ASSET_INI.is_file(),
        "assetDll": str(ASSET_DLL),
        "assetIni": str(ASSET_INI),
        "defaultPort": DEFAULT_PORT,
        "commonDetected": detect_common_game(),
        "processes": running_processes(),
        "hud": read_hud_status(),
    }


def schedule_shutdown(server: ThreadingHTTPServer) -> None:
    def worker() -> None:
        time.sleep(0.35)
        safe_console_log("Shutdown requested from WebUI.")
        server.shutdown()

    threading.Thread(target=worker, name="nte-shutdown", daemon=True).start()


class Handler(BaseHTTPRequestHandler):
    server_version = "NTEDLSSPanel/0.1.4"

    def log_message(self, fmt: str, *args: object) -> None:
        safe_console_log("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def send_json(self, data: object, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)
        try:
            self.wfile.flush()
        except OSError:
            pass

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise AppError("请求 JSON 无效。") from exc

    def handle_error(self, exc: Exception) -> None:
        if isinstance(exc, AppError):
            self.send_json({"ok": False, "error": str(exc)}, exc.status)
        else:
            self.send_json({"ok": False, "error": f"内部错误: {exc}"}, 500)

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/api/state":
                self.send_json({"ok": True, **api_state()})
                return
            if parsed.path == "/api/log":
                query = parse_qs(parsed.query)
                detected = detect_game(query.get("path", [""])[0])
                win64 = Path(detected["win64"])
                self.send_json({"ok": True, "log": read_log_summary(win64 / "dlsstweaks.log")})
                return
            if parsed.path == "/api/hud":
                self.send_json({"ok": True, "hud": read_hud_status()})
                return

            rel = unquote(parsed.path.lstrip("/")) or "index.html"
            target = (WEB_DIR / rel).resolve()
            if not str(target).startswith(str(WEB_DIR.resolve())) or not target.is_file():
                target = WEB_DIR / "index.html"
            content = target.read_bytes()
            mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as exc:
            self.handle_error(exc)

    def do_POST(self) -> None:
        try:
            parsed = urlparse(self.path)
            data = self.read_json()

            if parsed.path == "/api/browse":
                selected = run_native_folder_dialog()
                self.send_json({"ok": True, "path": selected, "cancelled": selected is None})
                return
            if parsed.path == "/api/detect":
                self.send_json({"ok": True, "detected": detect_game(data.get("path"))})
                return
            if parsed.path == "/api/install":
                ratio_payload = data.get("ratios", data.get("ratio", "0.30"))
                self.send_json(install_patch(data.get("path"), ratio_payload))
                return
            if parsed.path == "/api/restore":
                self.send_json(restore_patch(data.get("path"), data.get("backup")))
                return
            if parsed.path == "/api/hud":
                self.send_json({"ok": True, "hud": write_hud_status(bool(data.get("enabled")))})
                return
            if parsed.path == "/api/shutdown":
                self.send_json({
                    "ok": True,
                    "message": "后端服务正在退出。浏览器页面可以关闭；再次使用时重新运行 NTEDLSSPanel.exe 或 run.bat。",
                })
                schedule_shutdown(self.server)
                return

            raise AppError("未知 API。", 404)
        except Exception as exc:
            self.handle_error(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Neverness To Everness DLSSTweaks WebUI")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    if not WEB_DIR.is_dir():
        safe_console_log("web directory missing", error=True)
        return 1

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    safe_console_log(f"异环 DLSS Panel running at {url}")
    safe_console_log("Press Ctrl+C to stop.")

    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        safe_console_log("Stopping...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

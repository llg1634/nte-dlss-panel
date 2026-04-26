const levels = ["UltraPerformance", "Performance", "Balanced", "Quality"];

const state = {
  path: "",
  detected: null,
  ratio: "0.30",
  backups: [],
};

const $ = (id) => document.getElementById(id);

const gamePath = $("gamePath");
const ratioInput = $("ratioInput");
const ratioPreview = $("ratioPreview");
const outputHeight = $("outputHeight");
const estimateBox = $("estimateBox");
const syncLevels = $("syncLevels");
const levelPanel = $("levelPanel");
const detectCard = $("detectCard");
const logBox = $("logBox");
const statusStrip = $("statusStrip");
const assetPill = $("assetPill");
const toast = $("toast");
const filePlan = $("filePlan");
const backupSelect = $("backupSelect");
const backupDetails = $("backupDetails");
const hudCard = $("hudCard");
const serviceCard = $("serviceCard");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 3200);
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || "请求失败");
  }
  return data;
}

function setBusy(isBusy) {
  for (const button of document.querySelectorAll("button")) {
    button.disabled = isBusy;
  }
}

function formatPath(path) {
  return path || "未找到";
}

function parseRatio(value) {
  const text = String(value || "").trim().replace("%", "");
  const number = Number(text);
  if (!Number.isFinite(number)) return null;
  return number > 1 ? number / 100 : number;
}

function ratioLabel(value) {
  const ratio = parseRatio(value);
  if (ratio === null) return "无效比例";
  if (ratio < 0.333) return "低于官方 33% 下限";
  if (Math.abs(ratio - 0.333) < 0.002) return "约等于官方 720p 下限";
  return "官方可调区间内";
}

function updateEstimate() {
  const ratio = parseRatio(ratioInput.value);
  const height = Number(String(outputHeight.value || "").trim());
  if (!ratio || !Number.isFinite(height) || height <= 0) {
    estimateBox.textContent = "输入输出高度后会估算内部渲染高度。";
    return;
  }
  const renderHeight = Math.round(ratio * height);
  estimateBox.innerHTML = `
    <strong>${ratioInput.value}</strong> × ${height} ≈ <strong>${renderHeight}p</strong>。
    <span>${ratioLabel(ratio)}</span>
  `;
}

function setLevelInputs(value) {
  for (const level of levels) {
    $(`level-${level}`).value = value;
  }
}

function updateRatio(value) {
  state.ratio = value;
  ratioInput.value = value;
  ratioPreview.textContent = value;
  if (syncLevels.checked) setLevelInputs(value);
  document.querySelectorAll(".preset").forEach((button) => {
    button.classList.toggle("active", button.dataset.ratio === value);
  });
  updateEstimate();
}

function getRatios() {
  if (syncLevels.checked) {
    return Object.fromEntries(levels.map((level) => [level, ratioInput.value.trim()]));
  }
  return Object.fromEntries(levels.map((level) => [level, $(`level-${level}`).value.trim()]));
}

function formatQualityLevels(status) {
  const quality = status?.dlssQualityLevels;
  if (!quality?.exists) return "未读取到 dlsstweaks.ini";
  const ratios = quality.ratios || {};
  const label = quality.isDefaultMapping ? "默认映射" : "自定义映射";
  return `${label}：UP ${ratios.UltraPerformance || "-"} / P ${ratios.Performance || "-"} / B ${ratios.Balanced || "-"} / Q ${ratios.Quality || "-"}`;
}

function renderDetection(detected) {
  state.detected = detected;
  state.path = detected.input;
  gamePath.value = detected.input;

  const status = detected.status || {};
  const stale = status.staleProxyFiles?.length ? status.staleProxyFiles.join(", ") : "无";
  const qualityLine = formatQualityLevels(status);
  const running = detected.processes?.length
    ? detected.processes.map((p) => `${p.ProcessName}#${p.Id}`).join(", ")
    : "未运行";

  detectCard.classList.remove("muted");
  detectCard.innerHTML = `
    <strong>检测成功</strong><br>
    HTGame：<code>${formatPath(detected.exe)}</code><br>
    Win64：<code>${formatPath(detected.win64)}</code><br>
    当前代理：${status.proxyInstalled ? "已存在 winmm.dll" : "未安装"}<br>
    四档映射：${qualityLine}<br>
    旧代理残留：${stale}<br>
    运行进程：${running}
  `;

  renderFilePlan(detected);
  renderBackups(status.backups || [], detected.win64);
  renderStatus(status);
}

function renderFilePlan(detected) {
  const win64 = detected?.win64 || "<Win64>";
  filePlan.innerHTML = `
    <strong>安装时会处理的文件</strong><br>
    备份目录：<code>${win64}\\_nte_dlss_backups\\时间戳</code><br>
    写入：<code>${win64}\\winmm.dll</code><br>
    写入：<code>${win64}\\dlsstweaks.ini</code><br>
    清理旧入口：<code>dxgi.dll</code>、<code>nvngx.dll</code>、<code>XInput1_4.dll</code>，如果存在会先备份再删除。<br>
    日志：<code>dlsstweaks.log</code> 会在启动游戏后重新生成。
  `;
}

function renderBackups(backups, win64) {
  state.backups = backups;
  backupSelect.innerHTML = "";

  if (!backups.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "暂无备份";
    backupSelect.append(option);
    backupDetails.classList.add("muted");
    backupDetails.innerHTML = `
      备份位置：<code>${win64 || "<Win64>"}\\_nte_dlss_backups</code><br>
      还没有安装记录。第一次点击“按当前档位设置安装 / 更新”时会自动创建。
    `;
    return;
  }

  for (const backup of backups) {
    const option = document.createElement("option");
    option.value = backup.name;
    option.textContent = `${backup.name} ${backup.ratio ? `(${backup.ratio})` : ""}`;
    backupSelect.append(option);
  }
  backupDetails.classList.remove("muted");
  renderBackupDetails();
}

function renderBackupDetails() {
  const selected = state.backups.find((item) => item.name === backupSelect.value) || state.backups[0];
  if (!selected) return;

  const backedFiles = Object.entries(selected.files || {})
    .filter(([, record]) => record.existed)
    .map(([name]) => name);
  const ops = selected.operations?.length ? selected.operations.join(" / ") : "旧版本备份，无操作摘要";

  backupDetails.innerHTML = `
    <strong>所选备份</strong>：${selected.name}<br>
    路径：<code>${selected.path}</code><br>
    比例：${selected.ratio || "未记录"}<br>
    已备份文件：${backedFiles.length ? backedFiles.map((name) => `<code>${name}</code>`).join(" ") : "当时没有同名文件"}<br>
    安装动作：${ops}
  `;
}

function renderStatus(status) {
  const log = status?.log || {};
  const parts = [];
  parts.push(status?.proxyInstalled ? "winmm.dll 已安装" : "winmm.dll 未安装");
  parts.push(status?.iniInstalled ? "ini 已安装" : "ini 未安装");
  if (status?.dlssQualityLevels?.exists) {
    parts.push(status.dlssQualityLevels.isDefaultMapping ? "四档默认映射" : "四档自定义映射");
  }
  if (log.loaded) parts.push("WINMM 已加载");
  if (log.hooks) parts.push("DLSS Hook 已完成");
  if (status?.staleProxyFiles?.length) parts.push(`旧代理残留：${status.staleProxyFiles.join(", ")}`);
  statusStrip.innerHTML = parts.map((part) => `<span>${part}</span>`).join("");

  if (log.tail) {
    logBox.textContent = log.tail;
  }
}

function renderHud(hud) {
  if (!hud) {
    hudCard.classList.add("muted");
    hudCard.textContent = "未读取到 HUD 状态。";
    return;
  }

  hudCard.classList.toggle("muted", !hud.enabled);
  const stateText = hud.enabled ? "已开启" : "未开启";
  const valueText = hud.value === null || hud.value === undefined ? "未创建" : hud.value;
  hudCard.innerHTML = `
    <strong>DLSS HUD：${stateText}</strong><br>
    注册表：<code>${hud.path}\\${hud.valueName}</code><br>
    当前值：<code>${valueText}</code>，模式：${hud.mode || "Unknown"}<br>
    ${hud.message || ""}
  `;
}

async function refreshHud(showMessage = true) {
  try {
    const data = await request("/api/hud");
    renderHud(data.hud);
    if (showMessage) showToast("HUD 状态已刷新。");
  } catch (error) {
    hudCard.classList.add("muted");
    hudCard.textContent = error.message;
    if (showMessage) showToast(error.message);
  }
}

async function setHud(enabled) {
  setBusy(true);
  try {
    const data = await request("/api/hud", {
      method: "POST",
      body: JSON.stringify({ enabled }),
    });
    renderHud(data.hud);
    showToast(enabled ? "DLSS HUD 已开启。" : "DLSS HUD 已关闭。");
  } catch (error) {
    showToast(error.message);
  } finally {
    setBusy(false);
  }
}

async function browsePath() {
  setBusy(true);
  try {
    const data = await request("/api/browse", { method: "POST", body: "{}" });
    if (data.cancelled) {
      showToast("已取消选择。");
      return;
    }
    gamePath.value = data.path;
    await detectPath();
  } finally {
    setBusy(false);
  }
}

async function detectPath() {
  const path = gamePath.value.trim();
  if (!path) {
    showToast("先选择或输入游戏路径。");
    return;
  }
  setBusy(true);
  try {
    const data = await request("/api/detect", {
      method: "POST",
      body: JSON.stringify({ path }),
    });
    renderDetection(data.detected);
    showToast("路径检测完成。");
  } catch (error) {
    detectCard.classList.add("muted");
    detectCard.textContent = error.message;
    showToast(error.message);
  } finally {
    setBusy(false);
  }
}

async function installPatch() {
  const path = gamePath.value.trim();
  if (!path) {
    showToast("先选择游戏路径。");
    return;
  }
  setBusy(true);
  try {
    const data = await request("/api/install", {
      method: "POST",
      body: JSON.stringify({ path, ratios: getRatios() }),
    });
    renderDetection(data.detected);
    await refreshLog(false);
    showToast(`安装完成。备份已写入：${data.backup}`);
  } catch (error) {
    showToast(error.message);
  } finally {
    setBusy(false);
  }
}

async function refreshLog(showMessage = true) {
  const path = gamePath.value.trim();
  if (!path) {
    if (showMessage) showToast("先选择游戏路径。");
    return;
  }
  try {
    const data = await request(`/api/log?path=${encodeURIComponent(path)}`);
    logBox.textContent = data.log.tail || "还没有 dlsstweaks.log。启动游戏后再刷新。";
    if (showMessage) showToast("日志已刷新。");
  } catch (error) {
    if (showMessage) showToast(error.message);
  }
}

async function restorePatch() {
  const path = gamePath.value.trim();
  const backup = backupSelect.value;
  if (!path) {
    showToast("先选择游戏路径。");
    return;
  }
  if (!backup) {
    showToast("没有可恢复的备份。");
    return;
  }
  if (!confirm(`恢复备份 ${backup}？当前 winmm.dll/dlsstweaks.ini 会按备份清单还原或移除。`)) {
    return;
  }
  setBusy(true);
  try {
    const data = await request("/api/restore", {
      method: "POST",
      body: JSON.stringify({ path, backup }),
    });
    renderDetection(data.detected);
    showToast("已恢复所选备份。");
  } catch (error) {
    showToast(error.message);
  } finally {
    setBusy(false);
  }
}

async function restoreDefaultLevels() {
  const path = gamePath.value.trim();
  if (!path) {
    showToast("先选择游戏路径。");
    return;
  }
  if (!confirm("恢复异环默认 DLSS 四档映射？只会改 dlsstweaks.ini，不会修改 HDR、Engine.ini、启动器配置或 NVIDIA 全局比例。")) {
    return;
  }
  setBusy(true);
  try {
    const data = await request("/api/default-levels", {
      method: "POST",
      body: JSON.stringify({ path }),
    });
    renderDetection(data.detected);
    showToast("已恢复默认四档映射。");
  } catch (error) {
    showToast(error.message);
  } finally {
    setBusy(false);
  }
}

async function shutdownTool() {
  if (!confirm("退出本地后端服务？关闭后需要重新运行 NTEDLSSPanel.exe 或 run.bat 才能再次打开面板。")) {
    return;
  }

  $("shutdownBtn").disabled = true;
  statusStrip.innerHTML = "<span>本地服务正在退出</span>";
  serviceCard.innerHTML = `
    <strong>本地服务正在退出</strong><br>
    后端会在几百毫秒后关闭。这个网页可能会失去连接，可以直接关闭浏览器标签页。
  `;

  try {
    const data = await request("/api/shutdown", { method: "POST", body: "{}" });
    showToast(data.message || "后端服务正在退出。");
  } catch (error) {
    showToast(error.message);
    $("shutdownBtn").disabled = false;
    return;
  }

  setTimeout(() => {
    serviceCard.classList.add("muted");
    serviceCard.innerHTML = `
      <strong>本地服务已关闭</strong><br>
      如果需要继续使用，请重新运行 <code>NTEDLSSPanel.exe</code> 或 <code>run.bat</code>。
    `;
  }, 900);
}

function initTheme() {
  const saved = localStorage.getItem("nte-theme");
  if (saved === "dark") {
    document.documentElement.dataset.theme = "dark";
  }
  $("themeToggle").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    if (next === "dark") {
      document.documentElement.dataset.theme = "dark";
      localStorage.setItem("nte-theme", "dark");
    } else {
      delete document.documentElement.dataset.theme;
      localStorage.setItem("nte-theme", "light");
    }
  });
}

async function initState() {
  try {
    const data = await request("/api/state");
    assetPill.textContent = data.assetsReady ? "DLSSTweaks 资产就绪" : "缺少 DLSSTweaks 资产";
    renderHud(data.hud);
    if (data.commonDetected) {
      renderDetection(data.commonDetected);
      gamePath.value = data.commonDetected.input;
    } else {
      renderFilePlan({ win64: "<Win64>" });
    }
  } catch (error) {
    assetPill.textContent = "服务状态异常";
    showToast(error.message);
  }
}

document.querySelectorAll(".preset").forEach((button) => {
  button.addEventListener("click", () => updateRatio(button.dataset.ratio));
});

ratioInput.addEventListener("input", () => {
  ratioPreview.textContent = ratioInput.value || "0.30";
  document.querySelectorAll(".preset").forEach((button) => button.classList.remove("active"));
  if (syncLevels.checked) setLevelInputs(ratioInput.value);
  updateEstimate();
});

outputHeight.addEventListener("input", updateEstimate);

syncLevels.addEventListener("change", () => {
  levelPanel.classList.toggle("is-disabled", syncLevels.checked);
  if (syncLevels.checked) setLevelInputs(ratioInput.value);
});

for (const level of levels) {
  $(`level-${level}`).addEventListener("input", () => {
    if (!syncLevels.checked && level === "Performance") {
      ratioPreview.textContent = $(`level-${level}`).value || ratioInput.value;
    }
  });
}

backupSelect.addEventListener("change", renderBackupDetails);

$("browseBtn").addEventListener("click", browsePath);
$("detectBtn").addEventListener("click", detectPath);
$("installBtn").addEventListener("click", installPatch);
$("refreshLogBtn").addEventListener("click", () => refreshLog(true));
$("defaultLevelsBtn").addEventListener("click", restoreDefaultLevels);
$("restoreBtn").addEventListener("click", restorePatch);
$("hudRefreshBtn").addEventListener("click", () => refreshHud(true));
$("hudOnBtn").addEventListener("click", () => setHud(true));
$("hudOffBtn").addEventListener("click", () => setHud(false));
$("shutdownBtn").addEventListener("click", shutdownTool);

initTheme();
updateRatio("0.30");
initState();

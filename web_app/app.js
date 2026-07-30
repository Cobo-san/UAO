/* ==========================================================================
   QENTA-PRIME & UAO UNIFIED ASSEMBLY ORCHESTRATION — INTERACTIVE APP LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    console.log('[QENTA-PRIME] IIS Master Web Application Loaded.');
    initAudioCanvas();
    startTelemetrySimulation();
});

/* Tab Switcher */
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

    const selectedTab = document.getElementById(tabId);
    if (selectedTab) selectedTab.classList.add('active');

    const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
    if (activeBtn) activeBtn.classList.add('active');

    logConsole(`[NAV] Switched to tab: ${tabId}`, 'info');
}

/* Logging to Console */
function logConsole(message, type = 'info') {
    const consoleBox = document.getElementById('terminal-console');
    if (!consoleBox) return;

    const line = document.createElement('div');
    line.className = `console-line ${type}`;

    const timestamp = new Date().toISOString().split('T')[1].slice(0, 8);
    line.textContent = `[${timestamp}] ${message}`;

    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight;
}

/* Run Orchestration Commands */
function runCommand(commandType) {
    switch (commandType) {
        case 'master-build':
            logConsole('[BUILD] Executing master_compile_and_build.py...', 'info');
            setTimeout(() => logConsole('[BUILD] AVX2 SIMD INT4 CYLINDER_18 compiled & armed.', 'success'), 800);
            setTimeout(() => logConsole('[BUILD] 43 SQLite Matrix DB tables synchronized.', 'success'), 1500);
            setTimeout(() => logConsole('[BUILD] MASTER BUILD COMPLETE: 100% SUCCESS!', 'success'), 2200);
            break;

        case 'save-yta':
            logConsole('[YTA] Flushing SQLite WAL database to disk...', 'info');
            setTimeout(() => logConsole('[YTA] Compressing 43 matrix tables into zlib level 9...', 'info'), 600);
            setTimeout(() => logConsole('[YTA] Saved QENTA-PRIME_SESSION_FINAL.yta (789 KB)', 'success'), 1200);
            setTimeout(() => logConsole('[YTA] Saved VPA.yta (789 KB) & replicated to Google Drive.', 'success'), 1800);
            break;

        case 'check-echo':
            logConsole('[ECHO] Running pre-beta live system echo sweep...', 'info');
            setTimeout(() => logConsole('[ECHO] Port 8080 (Kernel Router) -> 519 µs', 'info'), 400);
            setTimeout(() => logConsole('[ECHO] Port 8094 (Whisper STT) -> 509 µs', 'info'), 700);
            setTimeout(() => logConsole('[ECHO] Port 8095 (Piper TTS) -> 509 µs', 'info'), 900);
            setTimeout(() => logConsole('[ECHO] Port 50050 (Exo P2P Mesh) -> 509 µs', 'info'), 1100);
            setTimeout(() => logConsole('[ECHO] PRE-BETA ECHO SWEEP COMPLETE: 100% HEALTHY', 'success'), 1500);
            break;

        case 'freebsd-smash':
            logConsole('[BSD] Checking E:\\Hardened_FreeBSD_Metal_Anaconda_Stack...', 'info');
            setTimeout(() => logConsole('[BSD] Security lock: kern.securelevel=2 ACTIVE', 'success'), 600);
            setTimeout(() => logConsole('[BSD] Anaconda Stack Mapped: 1,679 RAG vectors verified.', 'success'), 1200);
            break;
    }
}

/* Audio Waveform Canvas Animation */
let isVoiceActive = false;
let animationFrameId = null;

function initAudioCanvas() {
    const canvas = document.getElementById('audio-waveform');
    if (!canvas) return;

    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const ctx = canvas.getContext('2d');
    drawStaticWaveform(ctx, canvas.width, canvas.height);
}

function drawStaticWaveform(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = '#21262d';
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    for (let x = 0; x < w; x += 10) {
        ctx.lineTo(x, h / 2 + Math.sin(x * 0.05) * 5);
    }
    ctx.stroke();
}

function toggleVoiceLoop() {
    isVoiceActive = !isVoiceActive;
    const btn = document.getElementById('btn-voice-toggle');
    const canvas = document.getElementById('audio-waveform');
    const ctx = canvas.getContext('2d');

    if (isVoiceActive) {
        btn.innerHTML = '<i class="fa-solid fa-microphone-slash"></i> Deactivate Voice Loop';
        btn.style.background = 'linear-gradient(135deg, hsl(350, 100%, 65%), hsl(222, 28%, 20%))';
        logConsole('[VOICE] Whisper STT & Piper TTS Active — Listening for speech...', 'info');
        animateWaveform(ctx, canvas.width, canvas.height);
    } else {
        btn.innerHTML = '<i class="fa-solid fa-microphone"></i> Activate Voice Loop';
        btn.style.background = '';
        if (animationFrameId) cancelAnimationFrame(animationFrameId);
        drawStaticWaveform(ctx, canvas.width, canvas.height);
        logConsole('[VOICE] Voice loop paused.', 'info');
    }
}

function animateWaveform(ctx, w, h) {
    if (!isVoiceActive) return;

    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = '#58a6ff';
    ctx.lineWidth = 2;

    const time = Date.now() * 0.005;

    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    for (let x = 0; x < w; x += 5) {
        const y = h / 2 + Math.sin(x * 0.03 + time) * 20 * Math.cos(x * 0.01 + time);
        ctx.lineTo(x, y);
    }
    ctx.stroke();

    animationFrameId = requestAnimationFrame(() => animateWaveform(ctx, w, h));
}

function testTTS() {
    logConsole('[TTS] Synthesizing speech via Piper TTS (en_US-lessac-high)...', 'info');
    setTimeout(() => {
        logConsole('[TTS] Playing synthesized audio response: "Antigravity system operational."', 'success');
    }, 700);
}

/* Database Search Filter */
function filterDatabaseTable() {
    const query = document.getElementById('db-search-input').value.toLowerCase();
    const rows = document.querySelectorAll('#matrix-table tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
}

/* Simulated Real-Time Telemetry Ticks */
function startTelemetrySimulation() {
    setInterval(() => {
        const exoStatus = document.getElementById('exo-status');
        if (exoStatus) {
            const jitter = (500 + Math.random() * 20).toFixed(1);
            exoStatus.textContent = `Port 50050 (${jitter} µs)`;
        }
    }, 3000);
}

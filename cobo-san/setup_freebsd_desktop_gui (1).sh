#!/bin/sh
# Automated FreeBSD 14.1 Full Desktop GUI (XFCE4 + SDDM + XRDP Remote Desktop) Setup Script
# Configures Xorg, XFCE4 desktop, audio daemons, DRM GPU acceleration, and XRDP RDP gateway.

set -e

echo "=== INITIALIZING FREEBSD 14.1 FULL DESKTOP GUI SETUP ==="

# 1. Install Required Desktop Packages
echo "[1/4] Installing Xorg, XFCE4, SDDM, XRDP, and Firefox Browser..."
pkg update && pkg install -y xorg xfce4 xfce4-goodies sddm xrdp xorgxrdp drm-kmod pulseaudio firefox

# 2. Enable System Daemons in /etc/rc.conf
echo "[2/4] Configuring System Daemons in /etc/rc.conf..."
sysrc dbus_enable="YES"
sysrc sddm_enable="YES"
sysrc xrdp_enable="YES"
sysrc xrdp_sesman_enable="YES"

# Load DRM GPU graphics acceleration driver
echo 'kld_list="i915kms fusefs linux64"' >> /etc/rc.conf

# 3. Configure Session Startup Files
echo "[3/4] Setting up XFCE4 Desktop Startup Files..."
echo "exec startxfce4" > ~/.xinitrc
echo "exec startxfce4" > ~/.xsession
chmod +x ~/.xsession

# 4. Start XRDP and SDDM Services
echo "[4/4] Starting XRDP & Session Manager Services..."
service dbus start || true
service xrdp start || true
service xrdp_sesman start || true

echo "=== FREEBSD 14.1 FULL DESKTOP GUI SETUP COMPLETE ==="
echo "[+] Connect from Windows Host using Remote Desktop (mstsc.exe /v:localhost:3389)"

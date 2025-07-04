#!/bin/bash
# =====================================
# 🚀 WIFI LOGIN TOOL - AUTO INSTALLER
# 🧠 Coded by Zombie Noyon (@cbx.noyon)
# =====================================

echo -e "\033[1;32m📦 Installing required packages...\033[0m"

# Detect environment
if [[ $PREFIX == *"com.termux"* ]]; then
    pkg update -y && pkg upgrade -y
    pkg install -y python git curl php openssh
else
    sudo apt update -y && sudo apt install -y python3 git curl php openssh
fi

echo -e "\033[1;32m🔐 Setting executable permissions...\033[0m"

# Give permission to scripts
chmod +x wifi_brute.py
chmod +x *.sh

echo -e "\033[1;32m✅ All dependencies installed!\033[0m"
echo -e "\033[1;36m💻 You can now run the tool using:\033[0m"
echo -e "\033[1;33mpython wifi_brute.py\033[0m"

#!/bin/bash

echo "🚀 DRX POWER SYSTEM STARTING..."

# 1. Installing required libraries
echo "📦 Installing Python libraries..."
pip install flask telebot requests psutil --quiet

# 2. Compiling C binary
echo "⚙️ Compiling drx.c binary..."
gcc drx.c -o drx -lpthread -O3
chmod +x drx

# 3. Cleaning up old processes
echo "🧹 Cleaning old sessions..."
pkill -f api.py
pkill -f drx.py

# 4. Starting Telegram Bot in background
echo "🤖 Starting Telegram Bot..."
nohup python3 drx.py > bot_logs.txt 2>&1 &
sleep 2

# 5. Starting Flask API in FOREGROUND (Important for Render Port Binding)
echo "🌐 Starting Flask API..."
python3 api.py

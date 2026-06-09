import telebot
import json
import requests
import datetime
import os
import time
import psutil
import socket
import threading

if os.path.exists('config.json'):
    with open('config.json') as f:
        config = json.load(f)
else:
    print("Error: config.json file nahi mili!")
    exit()

bot = telebot.TeleBot(config['token'])

# Render dynamic local port usage (matching api.py port 10000)
API_URL = "http://127.0.0.1:10000/hit" 
AUTH_TOKEN = "DRX_POWER_ULTRA_V4"

KEYS_FILE = "keys.json"
**USERS_FILE** = "users.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)

@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "🔥 **DRX POWER Bot Active**\n\nWelcome! Use /help to see command list.")

@bot.message_handler(commands=['help'])
def help_cmd(m):
    help_text = "🚀 **Available Commands...**"
    bot.reply_to(m, help_text)

@bot.message_handler(commands=['hit'])
def handle_hit(m):
    # Parsing logic for ip, port, time
    try:
        parts = m.text.split()
        if len(parts) < 4:
            bot.reply_to(m, "❌ **Format:** /hit <IP> <PORT> <TIME>")
            return
        
        target_ip = parts[1]
        target_port = parts[2]
        duration = parts[3]
        
        params = {
            'token': AUTH_TOKEN,
            'ip': target_ip,
            'port': target_port,
            'time': duration
        }
        
        res = requests.get(API_URL, params=params, timeout=10)
        if res.status_code == 200:
            bot.reply_to(m, f"🚀 **Attack Sent!**\nIP: {target_ip}\nPort: {target_port}\nTime: {duration}")
        else:
            bot.reply_to(m, "❌ **API ERROR!**\nServer responded but with an error.")
            
    except Exception as e:
        bot.reply_to(m, "❌ **VPS OFFLINE!**\nCould not connect to API. `python3 api.py` start hai?")

@bot.message_handler(commands=['myinfo'])
def myinfo(m):
    users = load_data('users.json')
    user_id = str(m.from_user.id)
    if user_id in users:
        bot.reply_to(m, f"👤 **User Info:**\nPlan: {users[user_id]['plan']}\nStatus: Active ✅")
    else:
        bot.reply_to(m, "❌ No active plan found.")

@bot.message_handler(commands=['status'])
def status(m):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('127.0.0.1', 10000))
        api_status = "Online 🟢"
        s.close()
    except:
        api_status = "Offline 🔴"

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    bot.reply_to(m, f"📊 **System Status:**\nAPI: {api_status}\nCPU: {cpu_usage}%\nRAM: {ram_usage}%")

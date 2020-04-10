import os 
import datetime 
import random
import json

import discord

CLIENT_ID = os.getenv('ISABELLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('ISABELLE_CLIENT_SECRET')
TOKEN = os.getenv('ISABELLE_TOKEN')
SERVER_NAME = os.getenv('SERVER_NAME')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('AC_CHANNEL_ID')
data_file_path = ('isabelle.json')

client = discord.Client()
server = None
channel = None

random_messages = None
final_sayings = None
dailies = None

def construct_daily_message():
    now = datetime.datetime.now()
    now_string = now.strftime("%I:%M %p on %A, %B, %dth, %Y.")
    event_string = ''
    if (now.strftime("%A") == 'Sunday' and now.hour < 12 and now.hour > 6):
        event_string += "Don't forget to buy turnips today! Daisy is leaving at 12PM!\n"
    dailies_string = 'Daily Tasks:\n'
    for daily in dailies:
        dailies_string = dailies_string + daily + '\n'
    unrelated_message = random.choice(unrelated_messages)
    final_saying = random.choice(final_sayings)
    greeting = f"Hello Villagers!\n\nRight now on {SERVER_NAME}, it's {now_string}"
    return greeting + "\n\n" + event_string + dailies_string + "\n" + unrelated_message + "\n\n" + final_saying


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER_NAME:
            break
    for chat in guild.channels:
        if chat.name == 'animal-crossing':
            channel = chat
            break
    print(f'{client.user} has connected to Discord!')

    daily_message = construct_daily_message()
    await channel.send(daily_message)


with open(data_file_path, 'r') as data_file:
    isabelle_data = json.load(data_file)
unrelated_messages = isabelle_data['unrelated_messages']
final_sayings = isabelle_data['final_sayings']
dailies = isabelle_data['dailies']

client.run(TOKEN)

import discord
from discord.ext import commands
from discord import app_commands
import asyncio

import os
from dotenv import load_dotenv 

from turingmachine import TuringMachine 


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.default()
intents.message_content = True
client=discord.Client(intents=intents)
tree=app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} \nID: {bot.user.id}')
    print('================')
    await bot.add_cog(TuringMachine(bot))
    synced=await bot.tree.sync()
    print("Slash Command " + str(len(synced))) 

load_dotenv()
bot.run(os.environ.get('TOKEN'))
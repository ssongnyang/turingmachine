import discord
from discord.ext import commands
from discord import app_commands
import asyncio

import os
from dotenv import load_dotenv 

from turingmachine.turingmachine import TuringMachine
from loveletter.loveletter import LoveLetter


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
    await bot.add_cog(LoveLetter(bot))
    synced=await bot.tree.sync()
    print("Loaded Slash Command: " + str(len(synced))) 
    
@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"synced: {len(synced)}")

@app_commands.command(name="테스트", description="테스트")    
@app_commands.choices(테스트옵션=[
        app_commands.Choice(name='5개', value=5),
        app_commands.Choice(name='6개', value=6),
        app_commands.Choice(name='7개', value=7)
    ])
async def test(itc: discord.Interaction, 테스트옵션: int):
    print(test, 테스트옵션)
    
@bot.command()
async def image(ctx: commands.Context):
    embed=discord.Embed(title="title", description="description", url="https://www.youtube.com/")
    embed1 = discord.Embed(title="title", url="https://www.youtube.com/").set_image(url="https://mybox.naver.com/#/my/viewer/3472590704186383416:15902618?resourceKey=c3VobzA2MDR8MzQ3MjU5MDcwNDE4MTk1NTM4NHxEfDA&fileResourceKey=c3VobzA2MDR8MzQ3MjU5MDcwNDE4NjM4MzQxNnxGfDA&downloadable=true&editable=true")
    embed2 = discord.Embed(title="title", url="https://www.youtube.com/").set_image(url="https://mybox.naver.com/#/my/viewer/3472590704186383928:15902618?resourceKey=c3VobzA2MDR8MzQ3MjU5MDcwNDE4MTk1NTM4NHxEfDA&fileResourceKey=c3VobzA2MDR8MzQ3MjU5MDcwNDE4NjM4MzkyOHxGfDA&downloadable=true&editable=true")
    await ctx.channel.send(embeds=[embed1, embed2])
    
load_dotenv()
bot.run(os.environ.get('TOKEN'))
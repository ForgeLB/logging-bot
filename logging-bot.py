import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LOGGING_CHANNEL_ID = int(os.getenv('LOGGING_CHANNEL_ID'))

# Set up the bot with intent to track message updates and deletions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(
            f'**New message in {message.channel.mention} by {message.author.mention}:**\n{message.content}'
        )
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(
            f'**Message edited in {before.channel.mention} by {before.author.mention}:**\n'
            f'**Before:** {before.content}\n**After:** {after.content}'
        )

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(
            f'**Message deleted in {message.channel.mention} by {message.author.mention}:**\n{message.content}'
        )

bot.run(TOKEN)

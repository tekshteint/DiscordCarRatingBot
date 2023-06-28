import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import Crawler
import json
import MongoDB_Client
from keepAlive import keep_alive

#used for repl.it to keep bot alive 
#keep_alive()

def createEnv():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        token = config['token']

    with open('.env', 'w') as env_file:
        env_file.write(f'DISCORD_TOKEN={token}')



intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_message(message):
    if message.channel.name == "bot-tests":
        if message.author == bot.user:
            return

    await bot.process_commands(message)


@bot.command(name='addToDB')
async def add_to_db(ctx, *, command):
    try:
        await Crawler.processListing(command)
        await ctx.send("Added to DB")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='rateListing')
async def rateListing(ctx, *, command):
    try:
        rating = await Crawler.rateListing(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    if os.path.exists(".env"):
        load_dotenv()
    else:
        createEnv()
        load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
    
    """
    TODO:
    -add feature to search for listings locally with restrictions
    -add automatic crawling every X amount of hours for DB
    -add rating command and logic
    
    """
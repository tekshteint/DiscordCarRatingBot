import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import Crawler
import json

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
    
    
    """@bot.command()
async def name(ctx):
    await ctx.send("Hello {}".format(ctx.author.name))
    
 @bot.command()
async def addToDB(ctx):
    await Crawler.listingCrawler(ctx.message.content)
    await ctx.send("Added to DB") """
import os
try:
    from time import sleep
    import discord
    from discord.ext import commands
    from dotenv import load_dotenv
    import Crawler
    import json
except ImportError:
    os.system("pip install -r requirements.txt")
    print("\n-----------------------\nDependencies Installed\n-----------------------\n")
    os.system("py CarRatingBot.py")
    exit()
    

def createEnv():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'config.json')
    with open(filename, 'r') as config_file:
        config = json.load(config_file)
        token = config['token']

    envPath = os.path.join(here, '.env')
    with open(envPath, 'w') as env_file:
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


@bot.command(name='add')
async def add_to_db(ctx, *, command):
    try:
        urls = command.split()
        for url in urls:
            await Crawler.processListing(url)
            await ctx.send("Added to DB")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='rate')
async def rateListing(ctx, *, command):
    try:
        rating = await Crawler.rateListing(command)
        await ctx.send(rating)
    except discord.errors.HTTPException as e:
        await ctx.send("More than likely you tried to rate a model. Either use the $avg command or use $rate with the URL")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}. More than likely this car wasn't in the database. Trying to add it now.")
        await Crawler.processListing(command)
        try:
            print(command)
            rating = await Crawler.rateListing(command)
            await ctx.send(rating)
        except Exception as e:
            pass
        
@bot.command(name='avg')
async def rateModel(ctx, *, command):
    try:
        rating = await Crawler.rateModel(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='tweak')
async def tweak(ctx, *, command):
    try:
        rating = await Crawler.tweak(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='return')
async def returnDocument(ctx, *, command):
    try:
        rating = await Crawler.returnDocument(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='kbb')
async def kbb(ctx, *, command):
    try:
        area = ctx.message.channel
        #rating = await Crawler.kbb(command)
        await Crawler.kbb(command)
        await ctx.send("For now, until I figure out a way to convert this just download and open the SVG file to see the KBB market value", file=discord.File("Bot/kbbSVG.svg"))
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
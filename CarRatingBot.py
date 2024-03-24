import os
try:
    from time import sleep
    import discord
    from discord.ext import commands
    from dotenv import load_dotenv
    import Crawler
    import json
except ImportError:
    os.system("python -m pip install -r requirements.txt")
    print("\n-----------------------\nDependencies Installed\n-----------------------\n")
    os.system("python CarRatingBot.py")
    exit()
    

def createEnv():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            token = config['token']

        with open('.env', 'w') as env_file:
            env_file.write(f'DISCORD_TOKEN={token}')

    except FileNotFoundError:
        print("config.json not found. Please create a config.json file following the README")


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
        await Crawler.processListing(command)
        await ctx.send("Added to DB")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
@bot.command(name='rate')
async def rateListing(ctx, *, command):
    try:
        rating = await Crawler.rateListing(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}. More than likely this car wasn't in the database. Adding it now.")
        await Crawler.processListing(command)
        try:
            print(command)
            rating = await Crawler.rateListing(command)
            await ctx.send(rating)
        except Exception as e:
            pass
        
@bot.command(name='averagePriceOf')
async def rateModel(ctx, *, command):
    try:
        rating = await Crawler.rateModel(command)
        await ctx.send(rating)
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
        
""" @bot.command(name='help')
async def rateListing(ctx, *, command):
    try:
        await ctx.send("Commands:\n$add stores a listing to the database\n$rate rates that specific listing. Semi-broken.\n$rateModel followed by the model of car will search across the database for that model string")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")
 """


if __name__ == "__main__":
    if os.path.exists(".env"):
        load_dotenv()
    else:
        import createDB
        createDB.run()
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
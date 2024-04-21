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
        document = await Crawler.getDocument(command)
        if document:
            for key, value in document.items():
                await ctx.send(f"Current value for {key}:\n{value}\nDo you want to make changes to {key}? y/n or 'stop' at any time to cancel")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['y', 'n', 'yes', 'no', 'stop']

                try:
                    user_response = await bot.wait_for('message', check=check, timeout=60)  

                    if user_response.content.lower() == 'y':
                        await ctx.send(f"What changes do you want to make to {key}?")
                        # Wait for user input for changes
                        user_changes = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120)

                        # Update the value in the document
                        document[key] = user_changes.content

                        await ctx.send("Value updated successfully.")
                    elif user_response.content.lower() == 'stop':
                        await ctx.send("Changes stopped.")
                        break
                    else:
                        await ctx.send(f"No changes requested for {key}.")
                except Exception as e:
                    await ctx.send(f"Error occurred: {str(e)}")
            await Crawler.tweak(command, document)
            await ctx.send("Tweak Operations complete.")
        else:
            await ctx.send("Car not found. Make sure to add it to the database first.")
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
        import svg2gif
        svg2gif
        await ctx.send(file=discord.File("Bot/kbbSVG.gif"))
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
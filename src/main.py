import discord, os
from dotenv import load_dotenv
from discord.ext import commands


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def hi(ctx):
    await ctx.send("hi!")

print(f"Token: {bot_token}")


# uruchamianie bota
bot.run(bot_token)
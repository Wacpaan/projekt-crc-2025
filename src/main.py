import discord, os, requests
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def get_APOD():
    url = "https://api.nasa.gov/planetary/apod?api_key=Hp6AA7vgFAcYM4TVcH3baG13fybg87Rdqmty1di8"
    response = requests.get(url)
    data = response.json()

    title = data.get("title", "Brak tytułu")
    explanation = data.get("explanation", "Brak opisu")
    image_url = data.get("url", "Brak obrazka")
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image = discord.File(image_bytes, filename="image.jpg")


    return f"**{title}**\n{explanation}\n{image_url}", image





@bot.command()
async def hi(ctx):
    await ctx.send("hi!")

print(f"Token: {bot_token}")

@bot.command()
async def daily(ctx):
    apod_info, image = get_APOD()
    
    await ctx.send(apod_info, file=image)


# uruchamianie bota
bot.run(bot_token)
import discord, os, requests
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO
from datetime import datetime, timedelta



env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
bot_token = os.getenv("BOT_TOKEN")
nasa_api_key = os.getenv("APOD_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



def daily_APOD():
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
    response = requests.get(url)
    data = response.json()

    title = data.get("title", "Brak tytułu")
    explanation = data.get("explanation", "Brak opisu")
    image_url = data.get("url", "Brak obrazka")
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image = discord.File(image_bytes, filename="image.jpg")


    return f"**{title}**\n{explanation}\n{image_url}", image

def get_APDO(date):
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}"

    response = requests.get(url)

    if response.status_code == 200:
        photo_data = response.json()

        if photo_data.get("media_type") != "image":
            return f"**{photo_data.get('title', 'Brak tytułu')}**\n{photo_data.get('explanation', 'Brak opisu')}\n🔗 Link: {photo_data.get('url')}", None

        title = photo_data.get("title", "Brak tytułu")
        explanation = photo_data.get("explanation", "Brak opisu")
        image_url = photo_data.get("url", "")

        image_response = requests.get(image_url)
        image_bytes = BytesIO(image_response.content)
        image = discord.File(image_bytes, filename="image.jpg")

        formatted_text = f"**{title}**\n{explanation}\n{image_url}"
        return formatted_text, image

    else:
        return "❌ Nie udało się pobrać danych z NASA API.", None





@bot.command()
async def hi(ctx):
    await ctx.send("hi!")

print(f"Token: {bot_token}")

@bot.command()
async def daily(ctx):
    daily_apod, image = daily_APOD()
    
    await ctx.send(daily_apod, file=image)

@bot.command()
async def APOD(ctx, *, date: str = None):
    if not date:
        today = datetime.today().strftime('%Y-%m-%d')
        await ctx.send(f"❗ Użycie: `!APOD <rrrr-mm-dd>`\nNp: `!APOD {today}`")
        return

    opis, image = get_APDO(date)

    if opis:
        if image:
            await ctx.send(opis, file=image)
        else:
            await ctx.send(opis + "\n🔸 (Brak obrazu – może to wideo?)")
    else:
        await ctx.send(f"❌ Brak danych dla daty: {date}")


# uruchamianie bota
bot.run(bot_token) 
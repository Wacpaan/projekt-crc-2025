import discord, os, requests
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO
from datetime import datetime, timedelta
import random


env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
bot_token = os.getenv("BOT_TOKEN")
nasa_api_key = os.getenv("NASA_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_MRP(date):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={nasa_api_key}"
    response = requests.get(url)
    data = response.json()

    photos = data.get("photos", [])

    if not photos:
        return "❌ Brak zdjec z tego dnia.", None
    first_photo = photos[0]
    image_url = first_photo["img_src"]
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image = discord.File(image_bytes, filename="image.jpg")

    return f"📷 Zdjęcie z Marsa z dnia {date}:", image

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


    return f"**📝 {title}**\n{explanation}\n{image_url}", image

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

        formatted_text = f"**📝 {title}**\n**📅 {date}**\n{explanation}\n{image_url}"
        return formatted_text, image

    else:
        return "❌ Nie udało się pobrać danych z NASA API.", None


def random_date(start, end):
    """Returns a random date as a string in the format YYYY-MM-DD between the start and end dates."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    rand_date = start + timedelta(days=random_days)
    return rand_date.strftime('%Y-%m-%d')


favorites = {}

def add_to_favorites(user_id, date, title):
    user_favs = favorites.setdefault(user_id, [])
    if (date, title) not in user_favs:
        user_favs.append((date, title))
        return True
    return False

def get_user_favorites(user_id):
    return favorites.get(user_id, [])

@bot.command()
async def MRP(ctx, *, date: str = None): 
    """MRP"""
    opis, image = get_MRP(date)
    if not image:
        await ctx.send(opis)
    else:
        await ctx.send(opis)
        await ctx.send(file = image)

@bot.command()
async def random_MRP(ctx):
        start_date = datetime.strptime('2012-08-06', '%Y-%m-%d')
        end_date = datetime.today()

        date = random_date(start_date, end_date)
        opis, image = get_MRP(date)

        if opis:
            if image:
                await ctx.send(opis, file=image)
            else:
                await ctx.send(opis + "\n🔸 (Brak obrazu – może to wideo?)")
        else:
            await ctx.send(f"❌ Brak danych dla daty: {date}")


@bot.command()
async def hi(ctx):
    """test command"""
    await ctx.send("hi!")

print(f"Token: {bot_token}")

@bot.command()
async def daily(ctx):
    """The daily picture of APOD"""
    daily_apod, image = daily_APOD()
    
    await ctx.send(daily_apod, file=image)

@bot.command()
async def APOD(ctx, *, date: str = None):
    """Astronomy Picture of the day, u can set the date of the picture"""
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

@bot.command()
async def random_APOD(ctx):
    """Random date for APOD comand"""
    start_date = datetime.strptime('1995-06-16', '%Y-%m-%d' )
    end_date = datetime.today()

    date = random_date(start_date, end_date)
    opis, image = get_APDO(date)

    if opis:
        if image:
            await ctx.send(opis, file=image)
        else:
            await ctx.send(opis + "\n🔸 (Brak obrazu – może to wideo?)")
    else:
        await ctx.send(f"❌ Brak danych dla daty: {date}")



@bot.command()
async def add_favorite(ctx, *, date: str):
    """You can add picture do your favorites"""
    opis, _ = get_APDO(date) or get_MRP(date)
    if not opis:
        await ctx.send("❌ Nie znaleziono zdjęcia.")
        return

    title_line = opis.split('\n')[0].replace("**", "").strip()
    title = title_line if title_line else "Brak tytułu"

    added = add_to_favorites(str(ctx.author.id), date, title)
    if added:
        await ctx.send(f"✅ Dodano {date} do ulubionych!")
    else:
        await ctx.send("ℹ️ To zdjęcie już jest w Twoich ulubionych.")


@bot.command()
async def favorite(ctx):
    """Your favorite pictures, along with images"""
    favs = get_user_favorites(str(ctx.author.id))
    if not favs:
        await ctx.send("❗ Nie masz jeszcze żadnych ulubionych.")
        return
    for date, title in favs:
        opis, image = get_APDO(date)

        if opis and image:
            await ctx.send("**📌 Twoje ulubione zdjęcia:**")
            await ctx.send(f"📅 {date} \n{title}\n", file=image)
        elif opis:
            await ctx.send(opis + "\n🔸 (Brak obrazu – może to wideo?)")
        else:
            await ctx.send(f"❌ Nie udało się pobrać danych dla {date}.")


    

# uruchamianie bota
if __name__ == '__main__':
    bot.run(bot_token)
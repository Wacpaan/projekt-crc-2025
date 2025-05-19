import discord, os, requests
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO
from datetime import datetime, timedelta
import random

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
bot_token = os.getenv("BOT_TOKEN")
nasa_api_key = os.getenv("NASA_KEY")

# Set up bot intents and prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Mars Rover Photo retrieval
def get_MRP(date):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={nasa_api_key}"
    response = requests.get(url)
    data = response.json()

    photos = data.get("photos", [])

    if not photos:
        return "❌ No photos available for this date.", None

    first_photo = photos[0]
    image_url = first_photo["img_src"]
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)
    image = discord.File(image_bytes, filename="image.jpg")

    return f"📷 Mars Rover Photo from {date}:", image

# Daily APOD (Astronomy Picture of the Day)
def daily_APOD():
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
    response = requests.get(url)
    data = response.json()

    title = data.get("title", "No title")
    explanation = data.get("explanation", "No description")
    image_url = data.get("url", "No image")
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)
    image = discord.File(image_bytes, filename="image.jpg")

    return f"**📝 {title}**\n{explanation}\n{image_url}", image

# Get APOD for specific date
def get_APOD(date):
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        photo_data = response.json()

        if photo_data.get("media_type") != "image":
            return f"**{photo_data.get('title', 'No title')}**\n{photo_data.get('explanation', 'No description')}\n🔗 Link: {photo_data.get('url')}", None

        title = photo_data.get("title", "No title")
        explanation = photo_data.get("explanation", "No description")
        image_url = photo_data.get("url", "")

        image_response = requests.get(image_url)
        image_bytes = BytesIO(image_response.content)
        image = discord.File(image_bytes, filename="image.jpg")

        formatted_text = f"**📝 {title}**\n**📅 {date}**\n{explanation}\n{image_url}"
        return formatted_text, image
    else:
        return "❌ Failed to retrieve data from NASA API.", None

# Generate random date between two dates
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    rand_date = start + timedelta(days=random_days)
    return rand_date.strftime('%Y-%m-%d')

# Favorites system
favorites = {}

def add_to_favorites(user_id, date, title, source_type):
    user_favs = favorites.setdefault(user_id, [])
    if (date, title, source_type) not in user_favs:
        user_favs.append((date, title, source_type))
        return True
    return False

def get_user_favorites(user_id):
    return favorites.get(user_id, [])

# commands
@bot.command()
async def MRP(ctx, *, date: str = None): 
    """📸 Shows a Mars Rover photo for the given date."""
    if not date:
        today = datetime.today().strftime('%Y-%m-%d')
        await ctx.send(f"❗ Usage: `!MRP <yyyy-mm-dd>`\nExample: `!MRP {today}`")
        return
    
    desc, image = get_MRP(date)
    if not image:
        await ctx.send(desc)
    else:
        await ctx.send(desc)
        await ctx.send(file=image)

@bot.command()
async def random_MRP(ctx):
    """🔀 Displays a random Mars Rover photo since 2012."""
    start_date = datetime.strptime('2012-08-06', '%Y-%m-%d')
    end_date = datetime.today()

    date = random_date(start_date, end_date)
    desc, image = get_MRP(date)

    if desc:
        if image:
            await ctx.send(desc, file=image)
        else:
            await ctx.send(desc + "\n🔸 (No image – maybe it's a video?)")
    else:
        await ctx.send(f"❌ No data available for: {date}")

@bot.command()
async def hi(ctx):
    """👋 Simple test command – bot replies with 'hi!'."""
    await ctx.send("hi!")

@bot.command()
async def daily(ctx):
    """🗓️ Today's Astronomy Picture of the Day (APOD)."""
    daily_apod, image = daily_APOD()
    await ctx.send(daily_apod, file=image)

@bot.command()
async def APOD(ctx, *, date: str = None):
    """📅 Astronomy Picture of the Day for a specific date. Format: YYYY-MM-DD."""
    if not date:
        today = datetime.today().strftime('%Y-%m-%d')
        await ctx.send(f"❗ Usage: `!APOD <yyyy-mm-dd>`\nExample: `!APOD {today}`")
        return

    desc, image = get_APOD(date)

    if desc:
        if image:
            await ctx.send(desc, file=image)
        else:
            await ctx.send(desc + "\n🔸 (No image – maybe it's a video?)")
    else:
        await ctx.send(f"❌ No data available for: {date}")

@bot.command()
async def random_APOD(ctx):
    """🎲 Shows a random Astronomy Picture of the Day."""
    start_date = datetime.strptime('1995-06-16', '%Y-%m-%d')
    end_date = datetime.today()

    date = random_date(start_date, end_date)
    desc, image = get_APOD(date)

    if desc:
        if image:
            await ctx.send(desc, file=image)
        else:
            await ctx.send(desc + "\n🔸 (No image – maybe it's a video?)")
    else:
        await ctx.send(f"❌ No data available for: {date}")




@bot.command()
async def add_favorite(ctx, source: str, *, date: str):
    """Add an APOD or Mars photo to your favorites. Usage: !add_favorite <APOD|MRP> <YYYY-MM-DD>"""
    source = source.upper()

    if source == "APOD":
        desc, _ = get_APOD(date)
        if desc and "No image" not in desc and "Failed" not in desc:
            title_line = desc.split('\n')[0].replace("**", "").strip()
            title = title_line if title_line else "No title"
            added = add_to_favorites(str(ctx.author.id), date, title, "APOD")
        else:
            await ctx.send("❌ Could not find an APOD image for that date.")
            return

    elif source == "MRP":
        desc, _ = get_MRP(date)
        if desc and "No image" not in desc and "Failed" not in desc:
            title = "Mars Rover Photo"
            added = add_to_favorites(str(ctx.author.id), date, title, "MRP")
        else:
            await ctx.send("❌ Could not find a Mars Rover photo for that date.")
            return

    else:
        await ctx.send("❗ Invalid source. Use `APOD` or `MRP`.\nExample: `!add_favorite APOD 2023-08-10`")
        return

    if added:
        await ctx.send(f"✅ Added {date} ({source}) to your favorites!")
    else:
        await ctx.send("ℹ️ That photo is already in your favorites.")


@bot.command()
async def favorite(ctx):
    """View your favorite APOD and Mars photos."""
    favs = get_user_favorites(str(ctx.author.id))
    if not favs:
        await ctx.send("❗ You don't have any favorites yet.")
        return

    await ctx.send("**📌 Your favorite photos:**")
    for date, title, source_type in favs:
        if source_type == "APOD":
            desc, image = get_APOD(date)
        else:
            desc, image = get_MRP(date)

        if desc and image:
            await ctx.send(f"📅 {date} \n🧾 {title} ({source_type})", file=image)
        elif desc:
            await ctx.send(desc + f"\n🔸 ({source_type} – No image?)")
        else:
            await ctx.send(f"❌ Failed to load data for {date} ({source_type}).")

@bot.command()
async def remove_favorite(ctx, source:str, *, date:str):
    favs = get_user_favorites(str(ctx.author.id))
    if not favs:
        await ctx.send("❗ You don't have any favorites yet.")
        return


    source = source.upper()

    for fav in favs:
        fav_date, fav_title, fav_source = fav
        if fav_date == date and fav_source == source:
            favs.remove(fav)
            await ctx.send(f"✅ Removed favorite: {source} on {date}")
            return

    await ctx.send("❗ That favorite wasn't found.")


if __name__ == '__main__':
    bot.run(bot_token)
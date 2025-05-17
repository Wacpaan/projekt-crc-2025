# 🤖 Discord NASA Bot

A Discord bot built with `discord.py` that integrates with NASA APIs to display Astronomy Picture of the Day (APOD) and Mars Rover Photos (MRP). Users can view daily or random space photos and even save favorites!

---

## 🚀 Features

- `!hi` – Test command, bot replies with "hi!"
- `!daily` – Shows today's Astronomy Picture of the Day (APOD).
- `!APOD <YYYY-MM-DD>` – Shows APOD for a specific date.
- `!random_APOD` – Shows a random APOD since 1995.
- `!MRP <YYYY-MM-DD>` – Shows Mars Rover photo from Curiosity for a specific date.
- `!random_MRP` – Shows a random Mars Rover photo since 2012.
- `!add_favorite <APOD|MRP> <YYYY-MM-DD>` – Adds a photo to your personal favorites.
- `!favorite` – Displays all your saved favorite photos.

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/Wacpaan/space-bot
cd nasa-discord-bot

2. Create a virtual environment (optional)

python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

3. Install dependencies

pip install -r requirements.txt

4. Create a .env file

Create a .env file in the project root and add:

BOT_TOKEN=your_discord_token_here
NASA_KEY=your_nasa_api_key_here

You can get a free NASA API key from: https://api.nasa.gov
▶️ Running the bot

python src/app.y
🧪 Testing

Unit tests are written with pytest and use unittest.mock to simulate external API calls.

To run the tests:

pytest

✅ All 6 test cases are expected to pass.
📁 Project Structure

project-crc-2025/
├── src/
│   └── bot.py         # Main bot logic
├── tests/
│   └── test_unit.py       # Unit tests
├── .env                   # API keys (not committed)
├── requirements.txt       # Dependencies
├── README.md              # You're here!

📌 Notes

    APOD images go back to 1995-06-16

    Mars Rover photos are available from 2012-08-06 (Curiosity landing)

    Video media (from NASA) will show as a link instead of an image

📜 License

This project is for educational purposes. Feel free to modify or extend it!
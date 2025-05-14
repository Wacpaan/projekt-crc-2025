import sys
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from io import BytesIO
from src.app import bot
from src.app import daily_APOD


# Dodanie katalogu src do ścieżki importu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/app')))

def test_bot_initialization():
    assert bot.command_prefix == '!'
    assert bot.intents.message_content is True


@pytest.mark.asyncio
async def test_hi_command():
    # sztuczne tworzenie ctx
    mock_ctx = AsyncMock()
    #wywoalnie komendy
    await bot.get_command("hi").callback(mock_ctx)
    # sprawdzanie czy bot odpowiedzial hi
    mock_ctx.send.assert_called_once_with("hi!")

@patch("src.app.requests.get")  # poprawiona ścieżka
def test_daily_apod(mock_get):
    # Mock odpowiedzi z API
    mock_response_api = MagicMock()
    mock_response_api.json.return_value = {
        "title": "Test Title",
        "explanation": "Test Explanation",
        "url": "http://example.com/image.jpg"
    }
    # Mock odpowiedzi z pobierania obrazka
    mock_response_image = MagicMock()
    mock_response_image.content = b"fake image content"

    # Dwa kolejne wywołania requests.get
    mock_get.side_effect = [mock_response_api, mock_response_image]

    # Wywołanie funkcji daily_APOD()
    result_text, result_file = daily_APOD()

    # Sprawdzenie wyników
    assert "Test Title" in result_text  
    assert "Test Explanation" in result_text  
    assert isinstance(result_file, discord.File)  
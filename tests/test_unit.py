import sys
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from io import BytesIO
from src.app import bot
from src.app import daily_APOD
from src.app import random_date
from datetime import datetime

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

@patch("src.app.requests.get")  
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

def test_random_date_range():
    start = datetime(2020, 1, 1)
    end = datetime(2020, 12, 31)
    date = random_date(start, end)
    assert start.strftime('%Y-%m-%d') <= date <= end.strftime('%Y-%m-%d')


@pytest.mark.asyncio
@patch("src.app.requests.get")
async def test_command_apod_date(mock_get):
    mock_response_api = MagicMock()
    mock_response_api.status_code = 200
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


    mock_ctx = AsyncMock()
    await bot.get_command("APOD").callback(mock_ctx, date=datetime.today())
    assert mock_ctx.send.call_count >= 1
    args, kwargs = mock_ctx.send.call_args
    assert "Test Title" in args[0]

    file_arg = kwargs.get("file")
    if file_arg is not None:
        assert isinstance(file_arg, discord.File)

@pytest.mark.asyncio
@patch("src.app.requests.get")
async def test_command_mrp_date(mock_get):
    mock_response_api = MagicMock()
    mock_response_api.status_code = 200
    mock_response_api.json.return_value = {
        "photos": [
                {
                    "img_src": "http://example.com/image.jpg",
                    "earth_date": "2015-03-21",
                    "camera": { "full_name": "Mock Camera" },
                    "rover": { "name": "Mock Rover" }
                }
            ]
        }

        # Mock odpowiedzi z pobierania obrazka
    mock_response_image = MagicMock()
    mock_response_image.content = b"fake image content"
    mock_get.side_effect = [mock_response_api, mock_response_image]


    mock_ctx = AsyncMock()
    await bot.get_command("MRP").callback(mock_ctx, date=datetime(2015, 3, 21))
    
    first_send_call = mock_ctx.send.call_args_list[0]
    assert "Mars Rover Photo" in first_send_call.args[0]
    assert "2015-03-21" in first_send_call.args[0]

    # Sprawdzenie drugiego .send() — powinien zawierać plik
    file_send_call = next(call for call in mock_ctx.send.call_args_list if 'file' in call.kwargs)
    assert isinstance(file_send_call.kwargs['file'], discord.File)

    
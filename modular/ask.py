import aiohttp
import asyncio
from bs4 import BeautifulSoup
from gpytranslate import Translator
from pyrogram import filters
from pyrogram.types import Message
from Mix import *

__modles__ = "ask"
__help__ = "ask"

async def get_duckduckgo_answer(query):
    url = f"https://duckduckgo.com/html/?q={'+'.join(query.split())}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, "html.parser")
                answer = soup.find("a", class_="result__snippet")
                if answer:
                    return answer.text.strip()
    return "Maaf, tidak dapat menemukan jawaban untuk pertanyaan tersebut."

async def translate_text(text, target_language="id"):
    translator = Translator()
    translated_text = await translator.translate(text, target_lang=target_language)
    return translated_text

@ky.ubot("ask", sudo=True)
async def ask_command(_, message: Message):
    command_args = message.text.split(maxsplit=1)
    proses = await message.reply(f"Sedang berpikir ...")
    if len(command_args) == 2:
        query = command_args[1]
        answer = await get_duckduckgo_answer(query)
        translated_answer = await translate_text(answer)
        response = f"Pertanyaan: {query}\n\nJawaban:\n{translated_answer}"
        await message.reply_text(response)
        await proses.delete()
    else:
        await message.reply_text(
            "Format perintah salah. Gunakan /ask pertanyaan untuk mencari jawaban."
        )
        await proses.delete()

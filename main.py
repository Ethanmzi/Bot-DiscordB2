# main.py

import asyncio
import os
import time

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from storage import Storage
from storage import DATA_FILE  # juste pour info

# Chargement des variables d'environnement
load_dotenv()

# Création du storage (chargement des données)
storage = Storage(DATA_FILE)
storage.load()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# on attache le storage au bot pour que les cogs puissent y accéder
bot.storage = storage

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    autosave.start()

@tasks.loop(seconds=30)
async def autosave():
    # sauvegarde automatique toutes les 30 secondes
    bot.storage.save()

@bot.listen("on_message")
async def log_commands(message):
    """
    Listener qui enregistre toutes les commandes dans l'historique
    + compteur de commandes.
    """
    if message.author.bot:
        return

    if message.content.startswith("!"):
        user_id = str(message.author.id)
        hist = bot.storage.get_history_for(user_id)
        hist.push(message.content)
        bot.storage.inc_command_count(user_id)


async def main():
    # Chargement des cogs
    async with bot:
        await bot.load_extension("cogs.history")
        await bot.load_extension("cogs.dialog")
        await bot.load_extension("cogs.extra")

        TOKEN = os.getenv("DISCORD_TOKEN")
        if not TOKEN:
            raise ValueError("DISCORD_TOKEN non trouvé dans les variables d'environnement")
        await bot.start(TOKEN)
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

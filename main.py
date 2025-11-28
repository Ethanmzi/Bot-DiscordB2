# main.py

import asyncio
import time

import discord
from discord.ext import commands, tasks

from storage import Storage
from storage import DATA_FILE  # juste pour info

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


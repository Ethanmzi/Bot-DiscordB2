# cogs/extra.py

import time
import random
from discord.ext import commands
from storage import Storage


class ExtraCog(commands.Cog):
    def __init__(self, bot, storage: Storage):
        self.bot = bot
        self.storage = storage
        self.start_time = time.time()

    @commands.command()
    async def stats(self, ctx):
        """
        Montre combien de commandes tu as envoyées au bot.
        """
        user_id = str(ctx.author.id)
        count = self.storage.command_counts.get(user_id, 0)
        await ctx.send(f"Tu as envoyé **{count}** commandes au bot.")

    @commands.command()
    async def export(self, ctx):
        """
        Forcer une sauvegarde des données (fichier JSON).
        """
        self.storage.save()
        await ctx.send("Données sauvegardées dans `data.json` (export JSON).")

    @commands.command()
    async def ping(self, ctx):
        """
        Ping + latence (fonctionnalité bonus).
        """
        before = time.time()
        msg = await ctx.send("Pong ?")
        after = time.time()
        ms = int((after - before) * 1000)
        await msg.edit(content=f"Pong ! ({ms} ms)")

    @commands.command()
    async def roll(self, ctx, maximum: int = 100):
        """
        Lance un dé entre 1 et maximum (par défaut 100).
        """
        if maximum <= 1:
            maximum = 2
        value = random.randint(1, maximum)
        await ctx.send(f"🎲 Tu as fait **{value}** sur {maximum}.")


    @commands.command()
    async def mood(self, ctx):
        """
        Propose une activité en fonction de l'humeur de l'utilisateur.
        """
        suggestions = [
            "Regarde un tuto sur un nouveau langage pendant 20 minutes.",
            "Fais une pause café et débranche un peu ☕",
            "Teste une petite kata de code sur internet.",
            "Range un peu ton bureau et relance ensuite le bot 😆",
            "Lis un article sur un sujet tech qui t'intéresse.",
        ]
        choix = random.choice(suggestions)
        await ctx.send(f"Humeur captée... Je te propose :\n> {choix}")


    @commands.command()
    async def helpme(self, ctx):
        """
        Affiche la liste des commandes du bot avec une petite description.
        """
        text = (
            "**Commandes disponibles :**\n"
            "`!start` : lance la discussion pour choisir un langage de programmation.\n"
            "`!reset` : recommence la discussion depuis le début.\n"
            "`!speak_about <sujet>` : vérifie si le sujet existe dans l'arbre.\n"
            "`!last` : affiche ta dernière commande.\n"
            "`!history` : affiche ton historique de commandes (max 20).\n"
            "`!clear_history` : vide ton historique.\n"
            "`!stats` : affiche combien de commandes tu as envoyées.\n"
            "`!export` : force la sauvegarde des données dans data.json.\n"
            "`!ping` : vérifie la latence du bot.\n"
            "`!roll [max]` : lance un dé entre 1 et max (par défaut 100).\n"
            "`!mood` : propose une activité en fonction de ton humeur..\n"
        )
        await ctx.send(text)




async def setup(bot):
    storage = bot.storage
    await bot.add_cog(ExtraCog(bot, storage))

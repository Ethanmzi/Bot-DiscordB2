# cogs/history.py

from discord.ext import commands
from storage import Storage


class HistoryCog(commands.Cog):
    def __init__(self, bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command()
    async def last(self, ctx):
        """
        Affiche la dernière commande de l'utilisateur.
        """
        user_id = str(ctx.author.id)
        hist = self.storage.get_history_for(user_id)
        cmds = hist.to_list()
        if not cmds:
            await ctx.send("Tu n'as encore envoyé aucune commande.")
        else:
            await ctx.send(f"Dernière commande : `{cmds[0]}`")

    @commands.command()
    async def history(self, ctx):
        """
        Affiche toutes les commandes de l'utilisateur (limité à 20).
        """
        user_id = str(ctx.author.id)
        hist = self.storage.get_history_for(user_id)
        cmds = hist.to_list()
        if not cmds:
            await ctx.send("Historique vide pour toi.")
        else:
            txt = "\n".join(cmds[:20])
            await ctx.send(f"Tes commandes (max 20 dernières) :\n{txt}")

    @commands.command()
    async def clear_history(self, ctx):
        """
        Vide l'historique de l'utilisateur.
        """
        user_id = str(ctx.author.id)
        hist = self.storage.get_history_for(user_id)
        hist.clear()
        await ctx.send("Ton historique a été vidé 👍")


async def setup(bot):
    # on récupère le storage mis sur le bot (cf main.py)
    storage = bot.storage
    await bot.add_cog(HistoryCog(bot, storage))

# cogs/dialog.py

from discord.ext import commands
from storage import Storage


class DialogCog(commands.Cog):
    def __init__(self, bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name="start")
    async def start_command(self, ctx):
        """
        Lance la conversation avec l'arbre.
        """
        user_id = str(ctx.author.id)
        self.storage.sessions[user_id] = self.storage.tree_root
        await ctx.send(self.storage.tree_root.question)


    @commands.command()
    async def reset(self, ctx):
        """
        Reset la discussion depuis la racine.
        """
        user_id = str(ctx.author.id)
        self.storage.sessions[user_id] = self.storage.tree_root
        await ctx.send("On recommence depuis le début !")
        await ctx.send(self.storage.tree_root.question)

    @commands.command(name="speak_about")
    async def speak_about(self, ctx, *, topic: str):
        """
        Vérifie si un sujet existe dans l'arbre.
        """
        if self.storage.tree_root is None:
            await ctx.send("L'arbre n'est pas initialisé.")
            return

        exists = self.storage.tree_root.find_topic(topic)
        if exists:
            await ctx.send(f"Oui, je peux parler de `{topic}` ✅")
        else:
            await ctx.send(f"Non, je n'ai pas de sujet `{topic}` dans mon arbre ❌")



    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Gère les réponses de l'utilisateur dans la conversation
        (uniquement si ce n'est pas une commande).
        """
        if message.author.bot:
            return

        # si ça commence par '!' on laisse les autres commandes gérer
        if message.content.startswith("!"):
            return

        user_id = str(message.author.id)
        if user_id not in self.storage.sessions:
            return  # l'utilisateur n'est pas en mode discussion

        node = self.storage.sessions[user_id]
        content = message.content.lower().strip()

        # Racine : debutant / avance
        if node.key == "root":
            if content == "debutant":
                # trouver le child "debutant"
                for child in node.children:
                    if child.key == "debutant":
                        self.storage.sessions[user_id] = child
                        await message.channel.send(child.question)
                        return
                await message.channel.send("Erreur interne: pas de noeud 'debutant' dans l'arbre.")
                return
            elif content == "avance":
                for child in node.children:
                    if child.key == "avance":
                        self.storage.sessions[user_id] = child
                        await message.channel.send(child.question)
                        return
                await message.channel.send("Erreur interne: pas de noeud 'avance' dans l'arbre.")
                return
            else:
                await message.channel.send("Répond juste par `debutant` ou `avance` stp 😅")
                return

        # Débutant : web / script
        elif node.key == "debutant":
            if content == "web":
                final_node = node.children[0]
                self.storage.sessions[user_id] = final_node
                await message.channel.send(final_node.result)
                del self.storage.sessions[user_id]
                return
            elif content == "script":
                final_node = node.children[1]
                self.storage.sessions[user_id] = final_node
                await message.channel.send(final_node.result)
                del self.storage.sessions[user_id]
                return
            else:
                await message.channel.send("Répond `web` ou `script` 😉")
                return

        # Avancé : mobile / backend / data
        elif node.key == "avance":
            if content == "mobile":
                final_node = node.children[0]
                self.storage.sessions[user_id] = final_node
                await message.channel.send(final_node.result)
                del self.storage.sessions[user_id]
                return
            elif content == "backend":
                final_node = node.children[1]
                self.storage.sessions[user_id] = final_node
                await message.channel.send(final_node.result)
                del self.storage.sessions[user_id]
                return
            elif content == "data":
                final_node = node.children[2]
                self.storage.sessions[user_id] = final_node
                await message.channel.send(final_node.result)
                del self.storage.sessions[user_id]
                return
            else:
                await message.channel.send("Répond `mobile`, `backend` ou `data` 😉")
                return




async def setup(bot):
    storage = bot.storage
    await bot.add_cog(DialogCog(bot, storage))

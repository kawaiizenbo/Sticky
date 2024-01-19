import discord

from discord.ext import commands
from cogs.debug import DebugCommands
from cogs.reaction_listener import ReactionListener

description = """Zeeby Sticky Bot for IBM Personal Computer and compatibles."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(description=description, intents=intents)

bot.add_cog(DebugCommands(bot))
bot.add_cog(ReactionListener(bot))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

print("ZeebyStickyBot init")

bot.run(open("token.txt", "r").read())

import discord

from config import cfg
from discord.ext import commands

class ReactionListener(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        msg = channel.fetch_message(payload.message_id)
        emoji = payload.emoji
        #if cfg[str(guild.id)]["channels"][str(msg.id)]["override_emoji"] != None:
        #    emoji = cfg[str(guild.id)]["channels"][str(msg.id)]["override_emoji"]
        await channel.send(emoji.name)
        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        return
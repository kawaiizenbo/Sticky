import discord, emoji

from config import cfg
from discord.ext import commands

class ReactionListener(commands.Cog):
    sent:dict = { }
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        # define parameters
        guild:discord.Guild = self.bot.get_guild(payload.guild_id)
        channel:discord.TextChannel = guild.get_channel(payload.channel_id)
        msg:discord.Message = await channel.fetch_message(payload.message_id)
        em = emoji.emojize(cfg["guilds"][str(guild.id)]["emoji"])
        threshold = cfg["guilds"][str(guild.id)]["threshold"]
        board_channel:discord.TextChannel = guild.get_channel(cfg["guilds"][str(guild.id)]["board_channel_id"])

        try:
            if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["emoji"] != None:
                em = emoji.emojize(cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["emoji"])
        except : 
            # channel must not be in config, ignore the message
            return
        
        if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["threshold"] != None:
                threshold = cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["threshold"]
        
        if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["board_channel_id"] != None:
                board_channel = cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["board_channel_id"]
        
        if em != payload.emoji.name:
            # emoji didnt match, ignore message
            return
        
        if str(msg.id) in self.sent:
            # already sent this, dont do it again
            return
        
        count = 0
        for reaction in msg.reactions:
            if reaction.emoji == em:
                count+=1

        if count == threshold:
            embed = discord.Embed(
                color = cfg["guilds"][str(guild.id)]["colour"]
            )
            embed.set_author(name=msg.author.display_name, icon_url=msg.author.display_avatar.url)
            embed.description = msg.content
            embed.timestamp = msg.created_at
            if len(msg.attachments) > 0:
                embed.set_image(url=msg.attachments[0].url)
            # this probably wont play nice with nqn but that bot sucks anyway
            sent_msg = await board_channel.send(content = msg.jump_url, embed = embed)
            self.sent[str(msg.id)] = str(sent_msg.id)
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        # define parameters
        guild:discord.Guild = self.bot.get_guild(payload.guild_id)
        channel:discord.TextChannel = guild.get_channel(payload.channel_id)
        msg:discord.Message = await channel.fetch_message(payload.message_id)
        em = emoji.emojize(cfg["guilds"][str(guild.id)]["emoji"])
        threshold = cfg["guilds"][str(guild.id)]["threshold"]
        board_channel:discord.TextChannel = guild.get_channel(cfg["guilds"][str(guild.id)]["board_channel_id"])

        try:
            if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["emoji"] != None:
                em = emoji.emojize(cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["emoji"])
        except : 
            # channel must not be in config, ignore the message
            return
        
        if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["threshold"] != None:
                threshold = cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["threshold"]
        
        if cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["board_channel_id"] != None:
                board_channel = cfg["guilds"][str(guild.id)]["channels"][str(channel.id)]["board_channel_id"]
        
        if em != payload.emoji.name:
            # emoji didnt match, ignore message
            return

        if str(msg.id) not in self.sent:
            # didnt send this, dont try to delete
            return
        
        count = 0
        for reaction in msg.reactions:
            if reaction.emoji == em:
                count+=1

        if count < threshold:
            to_delete = await board_channel.fetch_message(int(self.sent[str(msg.id)]))
            await to_delete.delete()
            self.sent.pop(str(msg.id))

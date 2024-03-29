import discord, datetime, time, platform

from discord.commands import slash_command
from discord.ext import commands
from config import cfg

class DebugCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime
        startTime = time.time()

    @slash_command(name="about")
    async def about(self, ctx):
        """Get bot info."""
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(
            color = cfg["guilds"][str(ctx.guild.id)]["colour"],
            title = "Bot info",
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.display_avatar)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Latency", value=round(self.bot.latency*1000, 1))
        embed.add_field(name="Pycord Version", value=discord.__version__)
        embed.add_field(name="Host OS", value=f"{platform.system()} {platform.release()}")
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="Bot Source", value="https://github.com/kawaiizenbo/ZeebyStickyBot", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        await ctx.respond(embed = embed, ephemeral=False)

import config
import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from Functions.DBController import insert_user_scam

async def setup(bot):
    await bot.add_cog(Closed(bot))

class Closed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/posts.sqlite")

    
    @app_commands.command(name="close-post", description="Close a post. VIP Only")
    @app_commands.checks.has_role(config.VIP_ROLE_ID)
    async def closed_post(self, ctx):
        if ctx.channel != config.VIP_HIRING_CHANNEL_ID:
            return await ctx.send("Only use this command in the VIP Channels")
        

        #fetch the last message in the channel to close it
        user_message = await ctx.channel.history().find(lambda m: m.author == ctx.author)
        if not user_message:
            return await ctx.send('You haven\'t posted any message in this channel.')
        
        embed = user_message.embeds[0] if user_message.embeds else None
        if embed:
            embed.title = f"**CLOSED** {embed.title}"
            embed.description = f"*{embed.description}*"
            embed.set_footer(text="Closed by the author")
            await user_message.edit(embed=embed)
            await ctx.send('Your post has been marked as closed.')
        else:
            await ctx.send('No embed found in your last message. This command is meant for posts with embeds.')

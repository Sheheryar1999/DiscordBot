import config
import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from Functions.DBController import insert_user_scam

async def setup(bot):
    await bot.add_cog(Scams(bot))


class Scams(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/posts.sqlite")

    @app_commands.command(name="scam", description="Alert about a potential scammer")
    @app_commands.checks.has_permissions(administrator=True)
    async def scam_alert(self, interaction: discord.Interaction, user: discord.Member, reason: str, profile_link: str):

        insert_user_scam(user.id, reason)
        channel_id = config.SCAM_WARNING_CHANNEL_ID 
        log_channel = interaction.guild.get_channel(int(channel_id))

        scam_embed = discord.Embed(
            title="Scam Alert",
            color=discord.Color.red()
        )
        
        scam_embed.add_field(name="User:", value=f"{user.mention} (`{user.id}`)", inline=False)
        scam_embed.add_field(name="Description:", value=reason, inline=False)
        scam_embed.add_field(name="Profile Link:", value=profile_link, inline=False)

        await interaction.response.send_message(embed=scam_embed)

        if log_channel:
            await log_channel.send(embed=scam_embed)
            print("Yeah its a scam aight")
        else:
            print("Error: Someone Done Fucked Up")

    @app_commands.command(name="dwc", description="Deal with Caution")
    @app_commands.checks.has_permissions(administrator=True)
    async def deal_with_caution(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        channel_id = config.DWS_WARNING_CHANNEL_ID 
        log_channel = interaction.guild.get_channel(int(channel_id))
        dwc_embed = discord.Embed(
        title="Deal With Caution",
        color=discord.Color.red()
        )

        dwc_embed.add_field(name="User:", value=f"{user.mention} (`{user.id}`)", inline=False)
        dwc_embed.add_field(name="Description:", value=reason, inline=False)
        await interaction.response.send_message(embed=dwc_embed)

        if log_channel:
            await log_channel.send(embed=dwc_embed)
            print("This User is sus")
        else:
            print("Error: Someone Done Fucked Up")



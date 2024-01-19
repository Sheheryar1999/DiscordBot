import os
import config
import sqlite3
import discord
from Functions.DBController import init_function
from discord.ext import commands
from discord import app_commands
from Interface.BumpView import BumpView
from Interface.GenerateEmbedView import EmbedView
from Interface.PostApprovalView import PostApprovalView
from Interface.JobPostView import PostView, ForHirePostView, PaidJobPostView, CommissionJobPostView

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents=intents,
            application_id=config.APPLICATION_ID,
            activity=discord.Activity(type=discord.ActivityType.watching, name="community")
        )

    async def setup_hook(self):

        self.add_view(BumpView())
        self.add_view(PostView())
        self.add_view(EmbedView())
        self.add_view(PaidJobPostView())
        self.add_view(ForHirePostView())
        self.add_view(CommissionJobPostView())
        self.add_view(PostApprovalView())

        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension('Commands.{}'.format(filename[:-3]))
                print("Loaded {}".format(filename))

            if filename.startswith('__'):
                pass

        # for filename in os.listdir("./Events"):
        #     if filename.endswith('.py'):
        #         await self.load_extension('Events.{}'.format(filename[:-3]))
        #         print("Loaded {}".format(filename))

        #     if filename.startswith('__'):
        #         pass

        for filename in os.listdir("./Tasks"):
            if filename.endswith('.py'):
                await self.load_extension('Tasks.{}'.format(filename[:-3]))
                print("Loaded {}".format(filename))

            if filename.startswith('__'):
                pass

        await bot.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    print("{} is online! Latency: {}ms".format(bot.user.name, round(bot.latency * 1000)))

@bot.event
async def on_command_error(ctx, error):
    print("Error:  Command aint working")


@bot.command(name="reload")
async def its_reload(ctx: commands.Context, folder: str, cog: str):
    await ctx.message.delete()
    try:
        await bot.reload_extension(f"{folder}.{cog}")
        await ctx.send("🔁 **{}.py** successfully reloaded!".format(cog))
    except:
        await ctx.send("⚠ Unable to reload **{}**".format(cog))


@app_commands.command(name="message", description="Send a message to anyone")
async def send_message(self, user: discord.Member, *,  message: str):
    try:
        await user.send(message)
        print(f'Message sent to {user.mention}\'s DM successfully.')
    except discord.Forbidden:
        print('Error: I don\'t have permission to send DMs to that user.')
    except Exception as e:
        print(f'An error occurred: {e}')


bot.run(config.TOKEN)
# Author: Chris Lallo
# Description: Source code for Skybot (Discord management bot)

# Import dependencies
import os.path
import sys
import re
import discord
from discord import Intents
from discord.ext import commands

# Adjust path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import command and helper modules
from cogs.role_management import RoleManagementCog
from cogs.member_management import MemberManagementCog
from cogs.game_management import GameManagementCog
from cogs.blackjack import BlackjackManagementCog
from cogs.help import CustomHelpCommand
from helpers.funcs import *

# Setup client
BOT_TOKEN = get_token()
intents = Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    activity = discord.Game(name="Chat .help for help!")
    await bot.add_cog(RoleManagementCog(bot))
    await bot.add_cog(MemberManagementCog(bot))
    await bot.add_cog(GameManagementCog(bot))
    await bot.add_cog(BlackjackManagementCog(bot))
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_command_error(ctx, error):
    # Send an error message when a command is not found
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description=f"Command not found: `{ctx.message.content}`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    # Send an error message when an author is missing permissions
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description=f"You don't have the permissions to run this command",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingRequiredArgument):
        help_command = bot.get_command("help")
        if help_command:
            await help_command(ctx)
        else:
            print("Error occurred getting help command")

bot.run(BOT_TOKEN)

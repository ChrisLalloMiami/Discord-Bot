# Author: Chris Lallo
# Description: Class for defining the Blackjack command cog

# Import dependencies
import discord
from discord.ext import commands

# Import command and helper modules
from helpers.funcs import *
from helpers.constants import *

class BlackjackManagementCog(commands.Cog, name="Blackjack"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="action [bet]")
    async def blackjack(self, ctx, *args: str):
        '''
        Play a game of blackjack with Skybot
        '''
        if ctx.channel.name.lower() != COMMAND_CHANNEL:
            return
        
        embed = discord.Embed(
            title="Error",
            description="Please specify at least one role.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

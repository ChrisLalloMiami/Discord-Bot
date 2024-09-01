# Author: Chris Lallo
# Description: Class for defining the Blackjack command cog

# Import dependencies
import discord
from discord.ext import commands
import yaml

# Import command and helper modules
from helpers.funcs import *
from helpers.database_funcs import *
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
        
        # Look for player database. If not there, set one up
        player_database_path = get_user_data_filepath(str(ctx.author.id))
        if not os.path.exists(player_database_path):
            create_new_database(player_database_path)
            embed = discord.Embed(
                title="Profile setup complete",
                description=f"Your profile is now setup. Your starting balance is {STARTING_CURRENCY} SkyBucks",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        
        # If database exists, see if game data is setup
        with open(player_database_path, "r+") as file:
            player_data = yaml.safe_load(file)
            if player_data["active_games"].get("Blackjack", None) is None:
                update_database(player_database_path)
                embed = discord.Embed(
                    title="Player database updated",
                    description="Your database was out of date but has been updated",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)

            # Database exists and is up-to-date
            

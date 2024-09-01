# Author: Chris Lallo
# Description: Class for defining the game management command cog

# Import dependencies
import discord
from discord.ext import commands
import yaml

# Import command and helper modules
from helpers.funcs import *
from helpers.database_funcs import *
from helpers.constants import *

class GameManagementCog(commands.Cog, name="Games"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="")
    async def setup(self, ctx):
        '''
        Setup your Skybox game account
        '''
        if ctx.channel.name.lower() != COMMAND_CHANNEL:
            return
        
        # Look for player database or create one
        player_database_path = get_user_data_filepath(str(ctx.author.id))
        print(f"Looking for player database at {player_database_path}")

        # If database exists, read out details and add newly added games
        if os.path.exists(player_database_path):
            print("Player database already existed")
            description = ""
            try:
                data_updated, description = update_database(player_database_path)
                if data_updated:
                    title = "Player database updated"
                else:
                    title = "Profile already setup"

                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            except Exception as e:
                print(e)
                print(e.with_traceback)
        
        # If database doesn't exist, create one
        else:
            print("Player database being created")
            create_new_database(player_database_path)
            embed = discord.Embed(
                title="Profile setup complete",
                description=f"Your starting balance is {STARTING_CURRENCY} SkyBucks",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

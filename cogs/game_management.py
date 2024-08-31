# Author: Chris Lallo
# Description: Class for defining the game management command cog

# Import dependencies
import discord
from discord.ext import commands
import yaml

# Import command and helper modules
from helpers.funcs import *
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
                with open(player_database_path, "r+") as file:
                    # Load file data
                    player_data = yaml.safe_load(file)
                    data_updated = False
                    print("File loaded")

                    description = f"SkyBucks: ${player_data['money']}\n"
                    active_games = ""
                    print("Starting reader loop")

                    # Remove deleted games from database
                    games_to_remove = [game for game in player_data["active_games"] if game not in GAMES]
                    if len(games_to_remove) > 0:
                        data_updated = True

                    for game in games_to_remove:
                        print(f"Removing {game} from database")
                        del player_data["active_games"][game]

                    # List all games and their statuses
                    for game in player_data["active_games"]:
                        if game:
                            active_games += (f"* {game}: {player_data['active_games'].get(game, None)}\n")

                    # Add new games to player's database if not already there
                    print("Starting adder loop")
                    for game in GAMES:
                        if game not in player_data["active_games"]:
                            data_updated = True
                            print(f"Found {game} to add")
                            active_games += (f"* {game}: Inactive\n")
                            player_data["active_games"][game] = "Inactive"
                    
                    print("Writing updated data back to file")
                    file.seek(0)
                    yaml.safe_dump(player_data, file)
                    file.truncate()  # Truncate in case the new content is smaller than the original

                    # If games were found, list them
                    if len(active_games) > 0:
                        description += active_games
                    
                    # Close file and send embed
                    file.close()
                    print("File closed")
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
            with open(player_database_path, "w") as file:
                content = f"money: {STARTING_CURRENCY}\nactive_games:\n{YML_INDENT}"
                for game in GAMES:
                    content += f"{game}: Inactive\n{YML_INDENT}"
                file.write(content)
                file.close()

            embed = discord.Embed(
                title="Profile setup complete",
                description=f"Your starting balance is {STARTING_CURRENCY} SkyBucks",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

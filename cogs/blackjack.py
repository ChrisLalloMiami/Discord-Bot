# Author: Chris Lallo
# Description: Class for defining the Blackjack command cog

# Import dependencies
import discord
from discord.ext import commands
import yaml

from PIL import Image
import requests
from io import BytesIO

# Import command and helper modules
from helpers.funcs import *
from helpers.database_funcs import *
from helpers.constants import *

# Define list for tracking gameplay

time_since_last_play = None
cards = {
    "Clubs" : {
        "Ace"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_ace.png",
        "Two"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_2.png",
        "Three" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_3.png",
        "Four"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_4.png",
        "Five"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_5.png",
        "Six"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_6.png",
        "Seven" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_7.png",
        "Eight" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_8.png",
        "Nine"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_9.png",
        "Ten"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_10.png",
        "Jack"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_jack.png",
        "Queen" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_queen.png",
        "King"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_king.png"
    },

    "Spades" : {
        "Ace"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/other/png_96_dpi/spades_ace_simple.png",
        "Two"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_2.png",
        "Three" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_3.png",
        "Four"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_4.png",
        "Five"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_5.png",
        "Six"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_6.png",
        "Seven" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_7.png",
        "Eight" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_8.png",
        "Nine"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_9.png",
        "Ten"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_10.png",
        "Jack"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_jack.png",
        "Queen" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_queen.png",
        "King"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_king.png"
    },

    "Diamonds" : {
        "Ace"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_ace.png",
        "Two"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_2.png",
        "Three" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_3.png",
        "Four"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_4.png",
        "Five"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_5.png",
        "Six"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_6.png",
        "Seven" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_7.png",
        "Eight" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_8.png",
        "Nine"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_9.png",
        "Ten"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_10.png",
        "Jack"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_jack.png",
        "Queen" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_queen.png",
        "King"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/diamonds_king.png"
    },

    "Hearts" : {
        "Ace"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_ace.png",
        "Two"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_2.png",
        "Three" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_3.png",
        "Four"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_4.png",
        "Five"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_5.png",
        "Six"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_6.png",
        "Seven" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_7.png",
        "Eight" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_8.png",
        "Nine"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_9.png",
        "Ten"   : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_10.png",
        "Jack"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_jack.png",
        "Queen" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_queen.png",
        "King"  : "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/hearts_king.png"
    }
}

player_cards = {}
dealer_cards = {}

class BlackjackManagementCog(commands.Cog, name="Blackjack"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="action [bet]")
    async def blackjack(self, ctx, *args):
        '''
        Play a game of blackjack with Skybot
        '''
        if ctx.channel.name.lower() != COMMAND_CHANNEL:
            return
        
        data_updated = False

        # Look for player database. If not there, set one up
        player_database_path = get_user_data_filepath(str(ctx.author.id))
        if not os.path.exists(player_database_path):
            create_new_database(player_database_path)
            data_updated = True
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
                data_updated = True
                embed = discord.Embed(
                    title="Player database updated",
                    description="Your database was out of date but has been updated",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)

            # Database exists and is up-to-date. Check command

            # If no changes were made to database and args were not provided
            if not args and not data_updated:
                embed = discord.Embed(
                    title="Error",
                    description="To start a game of Blackjack, say `.blackjack start [BET_AMOUNT]`",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            action = str.lower(args[0])
            bet = 0
            if action == "start":
                # Check bet amount
                try:
                    bet = int(args[1])
                    if bet <= 0:
                        raise Exception
                except Exception as e:
                    embed = discord.Embed(
                        title="Error",
                        description="Please enter a valid integer bet amount greater than zero",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return

                embed = discord.Embed(
                    title="Starting",
                    description=f"Your game of blackjack is now starting with a bet of {int(args[1])}",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                images = ["https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_ace.png",
                          "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/clubs_2.png",
                          "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_queen.png",
                          "https://tekeye.uk/playing_cards/images/svg_playing_cards/fronts/png_96_dpi/spades_9.png"]
                embeds = []
                adjusted_images = [Image.open(BytesIO(requests.get(url).content)) for url in images]
                width, height = adjusted_images[0].size
                total_width = width * len(adjusted_images)
                combined_image = Image.new("RGB", (total_width, height))

                x_offset = 0
                for img in adjusted_images:
                    combined_image.paste(img, (x_offset, 0))
                    x_offset += width
                
                combined_image.save("combined.png")

                file = discord.File("combined.png", filename="combined.png")
                embed = discord.Embed(
                    title="Your hand",
                    color=discord.Color.blue()
                )
                embed.set_image(url="attachment://combined.png")
                await ctx.send(file=file, embed=embed)
                
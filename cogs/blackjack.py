# Author: Chris Lallo
# Description: Class for defining the Blackjack command cog

# Import dependencies
import discord
from discord.ext import commands
import yaml

from PIL import Image
import requests
from io import BytesIO
import random
import re

# Import command and helper modules
from helpers.funcs import *
from helpers.database_funcs import *
from helpers.constants import *

# Define list for tracking gameplay

time_since_last_play = None
cards = {
    "Hidden" : "https://tekeye.uk/playing_cards/images/svg_playing_cards/backs/png_96_dpi/blue.png",

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

active_games = {}

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
                # Check if player has an ongoing game
                if str(ctx.author.id) in active_games:
                    embed = discord.Embed(
                        title="Error",
                        description="You already have an active game of Blackjack",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
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
                    description=f"Your game of blackjack is now starting with a bet of ${int(args[1])}",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

                # Core game logic

                # Deal player's and dealer's cards
                try:
                    pick_card(str(ctx.author.id), "player")
                    pick_card(str(ctx.author.id), "dealer")
                    pick_card(str(ctx.author.id), "player")
                    pick_card(str(ctx.author.id), "dealer")

                    player_score_options, dealer_score_options = check_scores(str(ctx.author.id))
                        
                    title = ""
                    if player_score_options[0] == player_score_options[1]:
                        title = f"Your hand (Sum: {player_score_options[0]})"
                    elif player_score_options[0] == 21 or player_score_options[1] == 21:
                        title = "Your hand (Sum: 21)"
                    else:
                        title = f"Your hand (Sum: {player_score_options[0]} or {player_score_options[1]})"

                    # Construct cards images
                    player_cards_path = splice_card_images(active_games[str(ctx.author.id)]["player_cards"], str(ctx.author.id))
                    file = discord.File(player_cards_path, filename="combined.png")
                    embed = discord.Embed(
                        title=title,
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=f"attachment://combined.png")
                    await ctx.send(file=file, embed=embed)

                    dealer_cards_path = splice_card_images([cards["Hidden"]] + active_games[str(ctx.author.id)]["dealer_cards"][:-1], str(ctx.author.id))
                    file = discord.File(dealer_cards_path, filename="combined.png")
                    embed = discord.Embed(
                        title="Dealer's hand",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=f"attachment://combined.png")
                    await ctx.send(file=file, embed=embed)

                    # Check for win or push
                    if player_score_options[0] == 21 or player_score_options[1] == 21:
                        if dealer_score_options[0] == 21 or dealer_score_options[1] == 21:
                            embed = discord.Embed(
                                title="Push",
                                description="You and the dealer were both dealt Blackjack",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return
                        else:
                            embed = discord.Embed(
                                title="Player Wins",
                                description="You were dealt Blackjack",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return
                except Exception as e:
                    print(e)
                    print(e.with_traceback)
            
            if action == "hit":
                # Check if player has an ongoing game
                if str(ctx.author.id) not in active_games:
                    embed = discord.Embed(
                        title="Error",
                        description="You do not have an active game of Blackjack",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
                try:
                    pick_card(str(ctx.author.id), "player")
                    player_score_options, dealer_score_options = check_scores(str(ctx.author.id))

                    title = ""
                    if player_score_options[0] == player_score_options[1]:
                        title = f"Your hand (Sum: {player_score_options[0]})"
                    elif player_score_options[0] == 21 or player_score_options[1] == 21:
                        title = "Your hand (Sum: 21)"
                    else:
                        if player_score_options[1] > 21:
                            title = f"Your hand (Sum: {player_score_options[0]})"
                        elif player_score_options[0] > 21:
                            title = f"Your hand (Sum: {player_score_options[1]})"
                        else:
                            title = f"Your hand (Sum: {player_score_options[0]} or {player_score_options[1]})"

                    # Construct cards images
                    player_cards_path = splice_card_images(active_games[str(ctx.author.id)]["player_cards"], str(ctx.author.id))
                    file = discord.File(player_cards_path, filename="combined.png")
                    embed = discord.Embed(
                        title=title,
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=f"attachment://combined.png")
                    await ctx.send(file=file, embed=embed)

                    dealer_cards_path = splice_card_images([cards["Hidden"]] + active_games[str(ctx.author.id)]["dealer_cards"][:-1], str(ctx.author.id))
                    file = discord.File(dealer_cards_path, filename="combined.png")
                    embed = discord.Embed(
                        title="Dealer's hand",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=f"attachment://combined.png")
                    await ctx.send(file=file, embed=embed)

                    # Check for win or push
                    if player_score_options[0] == 21 or player_score_options[1] == 21:
                        if dealer_score_options[0] == 21 or dealer_score_options[1] == 21:
                            embed = discord.Embed(
                                title="Push",
                                description="You and the dealer were both dealt Blackjack",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return
                        else:
                            embed = discord.Embed(
                                title="Player Wins",
                                description="You were dealt Blackjack",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return
                    elif player_score_options[0] > 21 and player_score_options[1] > 21:
                        embed = discord.Embed(
                            title="Player Loses",
                            description="You busted",
                            color=discord.Color.blue()
                        )
                        await ctx.send(embed=embed)
                        # Delete player's game database
                        del active_games[str(ctx.author.id)]
                        return
                except Exception as e:
                    print(e)
                    print(e.with_traceback)
            
            if action == "stand":
                # Check if player has an ongoing game
                if str(ctx.author.id) not in active_games:
                    embed = discord.Embed(
                        title="Error",
                        description="You do not have an active game of Blackjack",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
                try:
                    # Setup initial titles
                    player_score_options, dealer_score_options = check_scores(str(ctx.author.id))
                    player_title = ""
                    player_score = 0
                    if player_score_options[1] < 21:
                        player_title = f"Your hand (Sum: {player_score_options[1]})"
                        player_score = player_score_options[1]
                    else:
                        player_title = f"Your hand (Sum: {player_score_options[0]})"
                        player_score = player_score_options[0]

                    while True:
                        player_score_options, dealer_score_options = check_scores(str(ctx.author.id))
                        dealer_title = ""
                        if dealer_score_options[0] == dealer_score_options[1]:
                            dealer_title = f"Dealer's hand (Sum: {dealer_score_options[0]})"
                        elif dealer_score_options[0] == 21 or dealer_score_options[1] == 21:
                            dealer_title = "Dealer's hand (Sum: 21)"
                        else:
                            if dealer_score_options[1] > 21:
                                dealer_title = f"Dealer's hand (Sum: {dealer_score_options[0]})"
                            elif dealer_score_options[0] > 21:
                                dealer_title = f"Dealer's hand (Sum: {dealer_score_options[1]})"
                            else:
                                dealer_title = f"Dealer's hand (Sum: {dealer_score_options[0]} or {dealer_score_options[1]})"

                        # Show current cards, including revealing dealer's hidden card
                        player_cards_path = splice_card_images(active_games[str(ctx.author.id)]["player_cards"], str(ctx.author.id))
                        file = discord.File(player_cards_path, filename="combined.png")
                        embed = discord.Embed(
                            title=player_title,
                            color=discord.Color.blue()
                        )
                        embed.set_image(url=f"attachment://combined.png")
                        await ctx.send(file=file, embed=embed)

                        dealer_cards_path = splice_card_images(active_games[str(ctx.author.id)]["dealer_cards"], str(ctx.author.id))
                        file = discord.File(dealer_cards_path, filename="combined.png")
                        embed = discord.Embed(
                            title=dealer_title,
                            color=discord.Color.blue()
                        )
                        embed.set_image(url=f"attachment://combined.png")
                        await ctx.send(file=file, embed=embed)
                        
                        # Handle dealer bust
                        if dealer_score_options[0] > 21 and dealer_score_options[1] > 21:
                            embed = discord.Embed(
                                title="Player Wins",
                                description="Dealer busted",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return
                        
                        # Handle dealer blackjack
                        if dealer_score_options[0] == 21 or dealer_score_options[1] == 21:
                            embed = discord.Embed(
                                title="Player loses",
                                description="Dealer got Blackjack",
                                color=discord.Color.blue()
                            )
                            await ctx.send(embed=embed)
                            # Delete player's game database
                            del active_games[str(ctx.author.id)]
                            return

                        # Check if dealer must stand
                        dealer_score = 0
                        if (dealer_score_options[0] >= 17 and dealer_score_options[0] < 21) \
                            or (dealer_score_options[1] >= 17 and dealer_score_options[1] < 21):
                            # Get best option
                            if dealer_score_options[1] < 21:
                                dealer_score = dealer_score_options[1]
                            else:
                                dealer_score = dealer_score_options[0]
                            
                            # Compare with player
                            if dealer_score == player_score:
                                embed = discord.Embed(
                                    title="Push",
                                    description="You and the dealer ended with the same score",
                                    color=discord.Color.blue()
                                )
                                await ctx.send(embed=embed)
                                # Delete player's game database
                                del active_games[str(ctx.author.id)]
                                return
                            elif dealer_score > player_score:
                                embed = discord.Embed(
                                    title="Player loses",
                                    description="The dealer had a higher score than you",
                                    color=discord.Color.blue()
                                )
                                await ctx.send(embed=embed)
                                # Delete player's game database
                                del active_games[str(ctx.author.id)]
                                return
                            else:
                                embed = discord.Embed(
                                    title="Player wins",
                                    description="You had a higher score than the dealer",
                                    color=discord.Color.blue()
                                )
                                await ctx.send(embed=embed)
                                # Delete player's game database
                                del active_games[str(ctx.author.id)]
                                return
                        # Dealer doesn't need to stand. Deal another card
                        else:
                            pick_card(str(ctx.author.id), "dealer")
                            continue
                except Exception as e:
                    print(e)
                    print(e.with_traceback)

def check_scores(user_id: str):
    '''
    Checks the scores of the player and dealer, given the player's user_id
    in a string to locate their database entry. Returns 2-entry lists for
    each, containing the 2 possible scores for each

    ### Parameters

    * **user_id**: The user's user_id in a string

    ### Returns

    * **player_score_options**: A 2-entry list with the player's possible scores
    * **dealer_score_options**: A 2-entry list with the dealer's possible scores
    '''
    player_cards = active_games[user_id]["player_cards"]
    dealer_cards = active_games[user_id]["dealer_cards"]
    player_score_options = [0, 0]
    dealer_score_options = [0, 0]

    # Check player cards
    for image_url in player_cards:
        pval, pval_off = get_card_value(get_card_rank(image_url))
        # Not an ace
        if pval_off == 0:
            # Add to both possibilities
            player_score_options[0] += pval
            player_score_options[1] += pval
        # Is an ace
        else:
            # Add to both possibilities
            player_score_options[0] += pval
            player_score_options[1] += pval_off
    
     # Check dealer cards
    for image_url in dealer_cards:
        dval, dval_off = get_card_value(get_card_rank(image_url))
        # Not an ace
        if dval_off == 0:
            # Add to both possibilities
            dealer_score_options[0] += dval
            dealer_score_options[1] += dval
        # Is an ace
        else:
            # Add to both possibilities
            dealer_score_options[0] += dval
            dealer_score_options[1] += dval_off
    
    return player_score_options, dealer_score_options
    


def get_card_value(card_rank: str) -> tuple:
    '''
    Determines a card's value given its rank. Returns its value in the first
    entry of a tuple (because the input of an ace results in the return 1, 11)

    ### Parameters

    * **card_rank**: The rank of the card of which to find the value

    ### Returns

    * **card_value**: The value of the card
    '''
    match str.lower(card_rank):
        case "1":
            return 1, 0
        case "2":
            return 2, 0
        case "3":
            return 3, 0
        case "4":
            return 4, 0
        case "5":
            return 5, 0
        case "6":
            return 6, 0
        case "7":
            return 7, 0
        case "8":
            return 8, 0
        case "9":
            return 9, 0
        case "10":
            return 10, 0
        case "jack":
            return 10, 0
        case "queen":
            return 10, 0
        case "king":
            return 10, 0
        case "ace":
            return 1, 11

def get_card_rank(image_url: str):
    '''
    Gets the card value, given its image_url

    ### Parameters

    * **image_url**: The URL of the card's image

    ### Returns

    * **value**: The card's value
    '''
    pattern = r'/[a-z]+_([a-z0-9]+)(?:_simple)?\.png'
    matched = re.search(pattern, image_url)
    
    if matched:
        return matched.group(1).strip()
    else:
        print("ERROR: Failed to match card rank pattern")

def pick_card(user_id: str, destination: str):
    '''
    Picks a random card from the `cards` dictionary and returns
    its image URL

    ### Parameters

    * **user_id**: The user's user_id in a string
    * **destination**: The list in which to insert the picked card, either
    player or dealer

    ### Returns

    * **image_url**: The URL of the card's image
    '''
    # Setup player's game storage if necessary
    if not user_id in active_games:
        active_games[user_id] = {
            "player_cards" : [],
            "dealer_cards" : [],
            "player_sum"   : 0,
            "dealer_sum"   : 0
        }
    
    # Pick random cards
    while True:
        suit = random.choice(list(cards.keys()))
        if suit == "Hidden":
            continue
        rank = random.choice(list(cards[suit].keys()))
        image_url = cards[suit][rank]

        # Check if card is already in play. If so, pick another
        if image_url in active_games[user_id]["player_cards"] \
            or image_url in active_games[user_id]["dealer_cards"]:
            continue
        else:
            if destination == "player":
                active_games[user_id]["player_cards"].append(image_url)
            else:
                active_games[user_id]["dealer_cards"].append(image_url)
            return image_url

def splice_card_images(cards: list, user_id: str):
    '''
    Given a list of card image URLs, splices the images into one and
    saves the resulting image to the user's data directory. Returns the
    path to the new image

    ### Parameters

    * **cards**: A list of card image URLs
    * **user_id**: The user's user_id in a string

    ### Returns

    * **cards_path**: The path to the generated image
    '''
    adjusted_images = [Image.open(BytesIO(requests.get(url).content)) for url in cards]

    width, height = adjusted_images[0].size
    total_width = width * len(adjusted_images)
    combined_image = Image.new("RGB", (total_width, height))
    x_offset = 0

    for img in adjusted_images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += width
    
    cards_path = os.path.join(get_user_data_directory(user_id), "combined.png")
    combined_image.save(cards_path)
    return cards_path

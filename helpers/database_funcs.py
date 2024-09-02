# Author: Chris Lallo
# Description: Helper functions for database

# Import dependencies
import discord
import os
import yaml

# Import constants
from helpers.constants import *

def get_user_data_filepath(user_id: str):
    '''
    Returns a potential path to a database belonging to a player
    with the given user_id. If the player database directory does
    not exist, one is created

    ### Parameters

    * **user_id**: the user_id of the player, for whom the database is being searched
    '''
    player_dir = os.path.join(PLAYER_GAME_DATA_DIR, f"user_{user_id}")
    if not os.path.exists(player_dir):
        os.mkdir(player_dir)
    return os.path.join(player_dir, f"user_{user_id}.yml")

def get_user_data_directory(user_id: str):
    '''
    Returns the path to the given player's data directory, creating
    it if needed

    ### Parameters

    * **user_id**: the user_id of the player, for whom the database is being searched
    '''
    player_dir = os.path.join(PLAYER_GAME_DATA_DIR, f"user_{user_id}")
    if not os.path.exists(player_dir):
        os.mkdir(player_dir)
    return player_dir

def create_new_database(player_database_path: str):
    '''
    Creates a new player database at the given path, populated with
    default values for all given games

    ### Parameters

    * **player_database_path**: a path to the player database to update
    '''
    with open(player_database_path, "w") as file:
        content = f"money: {STARTING_CURRENCY}\nactive_games:\n{YML_INDENT}"
        for game in GAMES:
            content += f"{game}: Inactive\n{YML_INDENT}"
        file.write(content)
        file.close()

def update_database(player_database_path: str):
    '''
    Updates the player database at the given path, adding new games
    and deleting old games as necessary

    ### Parameters

    * **player_database_path**: a path to the player database to update

    ### Returns

    * **data_updated**: a boolean for whether or not the database was updated
    * **description**: a description of the updated database, for use in notifiers
    '''
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
        return data_updated, description

# Author: Chris Lallo
# Description: Helper functions

# Import dependencies
import discord
import os

# Import constants
from helpers.constants import *


def get_user_data_filepath(user_id: str):
    '''
    Returns a potential path to a directory belonging to a player
    with the given user_id
    '''
    return os.path.join(PLAYER_GAME_DATA_DIR, f"user_{user_id}.yml")

def get_token():
    '''
    Finds and returns the bot token
    '''
    try:
        with open("secret.txt", 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Error: secret.txt could not be opened")

def is_valid_role(ctx, role_name):
    '''
    Check if the role is below the BUFFER role
    '''
    buffer = discord.utils.get(ctx.guild.roles, name=BUFFER_NAME)
    requestedRole = None
    for role in ctx.guild.roles:
        if str.lower(role.name) == str.lower(role_name):
            requestedRole = role
            break
    if requestedRole is None:
        print("ERROR: Role not found")
        return
    if buffer is None:
        print("ERROR: BUFFER role not found")
        return
    return requestedRole.position < buffer.position

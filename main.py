import discord
from discord import Intents
from discord.ext import commands

# CONSTANTS
COMMAND_CHANNEL = "bot-commands"
BOT_TOKEN = ""

try:
    with open("secret.txt", 'r') as file:
        line = file.readline().strip()
        BOT_TOKEN = line
except FileNotFoundError:
    print("Error: secret.txt could not be opened")

# Setup client
intents = Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def cmds(ctx):
    if ctx.channel.name.lower() == COMMAND_CHANNEL:
        embed = discord.Embed(
            title="Skybot Help",
            description="Hello, I'm Skybot! Here's a list of helpful information for using me:",
            color=discord.Color.blue()
        )

        embed.add_field(name="Role Management", value=(
            "For adding or removing roles, use the `.role` and `.unrole` commands. "
            "These commands can only be used to obtain class-related, permissionless roles of the format ABC123.\n\n"
            "To add a role, say `.role ABC123`. "
            "Note that multiple roles can be specified in a space-delimited list, like `.role ABC123 XYZ456`.\n\n"
            "Similarly, roles can be removed with the `.unrole` command, like `.unrole ABC123` or `.unrole ABC123 XYZ456`. "
            "Additionally, all class-related roles can be removed at once with `.unrole all`."
        ))

        # Send the embed as a message
        await ctx.send(embed=embed)

@bot.command()
async def role(ctx, *roles):
    if ctx.channel.name.lower() != COMMAND_CHANNEL:
        return

    if not roles:
        embed = discord.Embed(
            title="Error",
            description="Please specify at least one role.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    added_roles = []
    not_found_roles = []
    invalid_roles = []

    for role_name in roles:
        if not is_valid_role(role_name):
            invalid_roles.append(role_name)
        else:
            normalized_role_name = role_name.upper()  # Normalize role name to uppercase
            role = discord.utils.get(ctx.guild.roles, name=normalized_role_name)
            if role:
                if role not in ctx.author.roles:
                    await ctx.author.add_roles(role)
                    added_roles.append(role.name)  # Use actual role name in confirmation
            else:
                not_found_roles.append(role_name)

    if added_roles:
        embed = discord.Embed(
            title="Success",
            description=f"Role(s) {', '.join(added_roles)} successfully added.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    if not_found_roles:
        embed = discord.Embed(
            title="Error",
            description=f"Role(s) {', '.join(not_found_roles)} not found. If you would like this role added, visit https://discord.com/channels/1165430643203776674/1184910477273346218",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    if invalid_roles:
        embed = discord.Embed(
            title="Error",
            description="Invalid role format. Roles must be in the form ABC123.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
async def unrole(ctx, *roles):
    if ctx.channel.name.lower() != COMMAND_CHANNEL:
        return

    if not roles:
        embed = discord.Embed(
            title="Error",
            description="Please specify at least one role.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    removed_roles = []
    not_found_roles = []
    invalid_roles = []

    for role_name in roles:
        if not is_valid_role(role_name):
            invalid_roles.append(role_name)
        else:
            normalized_role_name = role_name.upper()  # Normalize role name to uppercase
            role = discord.utils.get(ctx.guild.roles, name=normalized_role_name)
            if role:
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
                    removed_roles.append(role.name)  # Use actual role name in confirmation
            else:
                not_found_roles.append(role_name)

    if removed_roles:
        embed = discord.Embed(
            title="Success",
            description=f"Role(s) {', '.join(removed_roles)} successfully removed.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    if not_found_roles:
        embed = discord.Embed(
            title="Error",
            description=f"Role(s) {', '.join(not_found_roles)} not found. If you would like this role added, visit https://discord.com/channels/1165430643203776674/1184910477273346218",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    if invalid_roles:
        embed = discord.Embed(
            title="Error",
            description="Invalid role format. Roles must be in the form ABC123.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

def is_valid_role(role_name):
    '''
    Check if the role name matches the required pattern (3 letters followed by 3 numbers)
    '''
    return len(role_name) == 6 and role_name[:3].isalpha() and role_name[3:].isdigit()

# Run the bot with your token
bot.run(BOT_TOKEN)
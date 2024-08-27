import os.path
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import discord
from discord import Intents
from discord.ext import commands
# from cogs.role_management import RoleManagementCog

# CONSTANTS
COMMAND_CHANNEL = "bot-commands"
BUFFER_NAME = "BUFFER"
BOT_TOKEN = ""

try:
    with open("secret.txt", 'r') as file:
        line = file.readline().strip()
        BOT_TOKEN = line
except FileNotFoundError:
    print("Error: secret.txt could not be opened")

# Custom Help Command
class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Bot Commands",
            description="Here is a list of available commands:",
            color=discord.Color.blue()
        )

        for cog, commands_list in mapping.items():
            if cog is not None and len(commands_list) > 0:
                category_name = cog.qualified_name
                command_signatures = [self.get_command_signature(command) for command in commands_list]
                if command_signatures:
                    embed.add_field(name=category_name, value="\n".join(command_signatures), inline=False)

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Command: {command.name}",
            description=command.help or "No description provided",
            color=discord.Color.blue()
        )
        embed.add_field(name="Usage", value=f"`{self.get_command_signature(command)}`", inline=False)
        await self.context.send(embed=embed)

# Setup client
intents = Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    activity = discord.Game(name="Chat .help for help!")
    await bot.add_cog(RoleManagementCog(bot))
    await bot.change_presence(status=discord.Status.online, activity=activity)


class RoleManagementCog(commands.Cog, name="Role Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="[role1] [role2] ...")
    async def role(self, ctx, *roles):
        "Add a role to yourself"
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
        owned_roles = []

        for role_name in roles:
            requestedRole = None
            for role in ctx.guild.roles:
                if str.lower(role.name) == str.lower(role_name):
                    requestedRole = role
                    break
            if not requestedRole:
                not_found_roles.append(role_name)
                continue
            if not is_valid_role(ctx, role_name):
                invalid_roles.append(requestedRole.name)
                continue
            if requestedRole not in ctx.author.roles:
                await ctx.author.add_roles(requestedRole)
                added_roles.append(requestedRole.name)  # Use actual role name in confirmation
            else:
                owned_roles.append(requestedRole.name)

        if added_roles:
            embed = discord.Embed(
                title="Success",
                description=f"{', '.join(added_roles)} successfully added.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        if not_found_roles:
            embed = discord.Embed(
                title="Error",
                description=f"{', '.join(not_found_roles)} not found. If you would like this role added, visit https://discord.com/channels/1165430643203776674/1184910477273346218",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

        if invalid_roles:
            embed = discord.Embed(
                title="Error",
                description=f"No permissions to interact with {', '.join(invalid_roles)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        
        if owned_roles:
            embed = discord.Embed(
                title="Error",
                description=f"{', '.join(owned_roles)} already claimed.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(usage="[role1] [role2] ... OR all")
    async def unrole(self, ctx, *roles):
        """Remove a role from yourself"""
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
        
        if roles[0].lower() == "all":
            matching_roles = [role for role in ctx.author.roles if is_valid_role(ctx, role.name)]
            for role in matching_roles:
                if role.name != "@everyone":
                    await ctx.author.remove_roles(role)
            embed = discord.Embed(
                title="Success",
                description="All applicable roles successfully removed.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

        removed_roles = []
        not_found_roles = []
        invalid_roles = []
        unowned_roles = []

        for role_name in roles:
            requestedRole = None
            for role in ctx.guild.roles:
                if str.lower(role.name) == str.lower(role_name):
                    requestedRole = role
                    break
            if not requestedRole:
                not_found_roles.append(role_name)
                continue
            if not is_valid_role(ctx, role_name):
                invalid_roles.append(role_name)
                continue
            if requestedRole in ctx.author.roles:
                await ctx.author.remove_roles(requestedRole)
                removed_roles.append(requestedRole.name)  # Use actual role name in confirmation
            else:
                unowned_roles.append(requestedRole.name)

        if removed_roles:
            embed = discord.Embed(
                title="Success",
                description=f"{', '.join(removed_roles)} successfully removed.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        if not_found_roles:
            embed = discord.Embed(
                title="Error",
                description=f"{', '.join(not_found_roles)} not found. If you would like this role added, visit https://discord.com/channels/1165430643203776674/1184910477273346218",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

        if invalid_roles:
            embed = discord.Embed(
                title="Error",
                description=f"No permissions to interact with {', '.join(invalid_roles)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        
        if unowned_roles:
            embed = discord.Embed(
                title="Error",
                description=f"You don't have {', '.join(unowned_roles)}!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command(usage="[Category]")
    async def roles(self, ctx, role_type: str = None):
        """See the list of available roles"""
        if ctx.channel.name.lower() != COMMAND_CHANNEL:
            return
        
        roles = []
        buffer = discord.utils.get(ctx.guild.roles, name=BUFFER_NAME)
        for role in ctx.guild.roles:
            if buffer is None:
                print("ERROR: BUFFER role not found")
                return
            if role.position < buffer.position and role.name != "@everyone":
                roles.append(role)
        
        pattern = re.compile(r'^([A-Za-z]+)\d+$')
        categories = {
            "Misc": []
        }

        # Categorize roles
        for role in roles:
            match = pattern.match(role.name)
            if match:
                prefix = match.group(1)
                if prefix not in categories:
                    categories[prefix] = []
                categories[prefix].append(role)
            else:
                categories["Misc"].append(role)


        if role_type:
            role_type = role_type.upper()
            if role_type not in categories:
                if role_type == "MISC":
                    role_type = "Misc"
                else:
                    await ctx.send(f"No roles found for type: {role_type}")
                    return
            categories = {role_type: categories.get(role_type, [])}
        else:
            category_list = ", ".join(categories.keys())
            embed = discord.Embed(
                title="Error",
                description=f"Please choose a valid course category: {category_list}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Create a single embed
        embed = discord.Embed(
            title=f"Claimable {role_type} Roles",
            color=discord.Color.blue()
        )

        # Add fields for each category
        for category, roles_list in categories.items():
            if roles_list:
                roles_description = "\n".join(f"• {role}" for role in roles_list)
                embed.add_field(name=category, value=roles_description, inline=False)
        
        # Send the embed
        await ctx.send(embed=embed)

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Send a custom error message when the command is not found
        embed = discord.Embed(
            title="Error",
            description=f"Command not found: `{ctx.message.content}`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Run the bot with your token
bot.run(BOT_TOKEN)
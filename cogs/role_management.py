import discord
from discord.ext import commands

COMMAND_CHANNEL = "bot-commands"
BUFFER_NAME = "BUFFER"

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

class RoleManagementCog(commands.Cog, name="Role Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="[role1] [role2] ...")
    async def role(ctx, *roles):
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
    async def unrole(ctx, *roles):
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
            # Remove all roles that match the specified format (3 letters followed by 3 numbers)
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
            
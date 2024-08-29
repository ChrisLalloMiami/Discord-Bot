# Author: Chris Lallo
# Description: Class for defining the role management command cog

# Import dependencies
import discord
from discord.ext import commands
import re

# Import command and helper modules
from helpers.funcs import *

class RoleManagementCog(commands.Cog, name="Role Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="role1 [role2] ...")
    async def role(self, ctx, *roles):
        '''
        Add a role to yourself
        '''
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

    @commands.command(usage="role1 [role2] ... OR all")
    async def unrole(self, ctx, *roles):
        '''
        Remove a role from yourself
        '''
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
    
    @commands.command(usage="category")
    async def roles(self, ctx, role_type: str = None):
        '''
        See the list of available roles
        '''
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

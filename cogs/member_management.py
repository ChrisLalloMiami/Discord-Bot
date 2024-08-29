# Author: Chris Lallo
# Description: Class for defining the member management command cog

# Import dependencies
import discord
from discord.ext import commands
import re

# Import command and helper modules
from helpers.funcs import *
from helpers.constants import *

class MemberManagementCog(commands.Cog, name="Member Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="@user [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        '''
        Kick a user from the server
        '''
        # Don't let user kick themselves
        if user == ctx.author:
            embed = discord.Embed(
                title="Error",
                description="You cannot kick yourself",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        elif discord.utils.get(user.roles, name=ADMIN_NAME) is not None:
            embed = discord.Embed(
                title="Error",
                description="Cannot kick another admin",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Successful kick
        try:
            await user.kick(reason=reason)
            description = None
            if reason is not None:
                description = f"{user.mention} has been kicked for: {reason}"
            else:
                description = f"{user.mention} has been kicked"
            embed = discord.Embed(
                title="Success",
                description=description,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return
        # Cannot kick someone with higher privileges
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="Cannot kick this user due to elevated permissions",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        except discord.HTTPException:
            embed = discord.Embed(
                title="Error",
                description="Failed to kick the user due to a network error",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
    @commands.command(usage="@user [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason=None):
        '''
        Ban a user from the server
        '''
        # Don't let user ban themselves
        if user == ctx.author:
            embed = discord.Embed(
                title="Error",
                description="You cannot ban yourself",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        elif discord.utils.get(user.roles, name=ADMIN_NAME) is not None:
            embed = discord.Embed(
                title="Error",
                description="Cannot ban another admin",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Successful ban
        try:
            await user.ban(reason=reason)
            description = None
            if reason is not None:
                description = f"{user.mention} has been banned for: {reason}"
            else:
                description = f"{user.mention} has been banned"
            embed = discord.Embed(
                title="Success",
                description=description,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return
        # Cannot ban someone with higher privileges
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="Cannot ban this user due to elevated permissions",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        except discord.HTTPException:
            embed = discord.Embed(
                title="Error",
                description="Failed to ban the user due to a network error",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

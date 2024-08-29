# Author: Chris Lallo
# Description: Class for defining the bot's help command

# Import dependencies
import discord
from discord.ext import commands

# Define custom help command class
class CustomHelpCommand(commands.HelpCommand):
    # Break down message
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

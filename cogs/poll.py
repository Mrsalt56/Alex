import discord
from discord import app_commands
from discord.ext import commands
import json

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Bot Initialization
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=["!"], intents=intents)

@bot.event
async def on_ready():
    """Syncs the bot's slash commands on startup."""
    try:
        await bot.tree.sync()
        print(f'Logged in as {bot.user} | Slash commands synced!')
    except Exception as e:
        print(f"Error syncing commands: {e}")

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Create a poll with a title and an optional description.")
    @app_commands.describe(title="The title of the poll", description="An optional description for the poll")
    async def poll(self, interaction: discord.Interaction, title: str, description: str = "No description provided"):
        """Slash command to create a poll"""
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Color.purple()
        )
        embed.set_footer(text=f"Poll created by {interaction.user.name}")

        message = await interaction.channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

        await interaction.response.send_message("Poll created!", ephemeral=True)

async def setup(bot):
    """Add the Poll cog to the bot"""
    await bot.add_cog(Poll(bot))

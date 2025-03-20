import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("AutoRole is online!")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        connection = sqlite3.connect("./cogs/autorole.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Guild WHERE guild_id = ?", (member.guild.id,))
        
        result = cursor.fetchone()

        if result:
            auto_role_id = result[1]

            if auto_role_id:
                await member.add_roles(member.guild.get_role(auto_role_id))

    @app_commands.command(name="set_auto_role", description="Sets an automatic join role for this server.")
    async def set_auto_role(self, interaction: discord.Interaction, role: discord.Role):
        connection = sqlite3.connect("./cogs/autorole.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE Guild SET auto_role_id = ? WHERE guild_id = ?", (role.id, interaction.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"Automatic join role set to {role.name}.")

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
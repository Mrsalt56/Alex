import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1346995937435979856

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands ready!")

    async def check_roles(self, interaction: discord.Interaction) -> bool:
        allowed_roles = {"Twitch mod", "💻 | Mini Mod", "⚜️ | M.O.D"}
        return any(role.name in allowed_roles for role in interaction.user.roles)

    @app_commands.command(name="clear", description="Deletes a specified amount of messages from the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        if not await self.check_roles(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if amount < 1:
            await interaction.channel.send(f"{interaction.user.mention}, please specify a value greater than one.")
            return

        deleted_messages = await interaction.channel.purge(limit=amount)
        await interaction.channel.send(f"{interaction.user.mention} has deleted {len(deleted_messages)} message(s).")

    @app_commands.command(name="kick", description="Kicks a specified member.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        if not await self.check_roles(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.guild.kick(member)
        await interaction.response.send_message(f"Success! You have kicked {member.mention}!", ephemeral=True)

    @app_commands.command(name="ban", description="Bans a specified member.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        if not await self.check_roles(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.guild.ban(member)
        await interaction.response.send_message(f"Success! You have banned {member.mention}!", ephemeral=True)

    @app_commands.command(name="unban", description="Unbans a specified user by user ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        if not await self.check_roles(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Success! You have unbanned {user.name}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot))

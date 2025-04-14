import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Spammer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spam", description="Spam one of the chosen users in DMs")
    @app_commands.describe(member="The user to spam (must be allowed)", times="How many times", message="The message to send")
    async def spam(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        times: int = 5,
        message: str = "Hello!"
    ):
        vip_role_name = "🏆| V.I.P"
        allowed_user_ids = {1028724015969341520,1172317753378615427}

        # Role check
        if vip_role_name not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message("🚫 You must have the VIP role to use this command.", ephemeral=True)
            return

        # Target check
        if member.id not in allowed_user_ids:
            await interaction.response.send_message("🚫 You can only spam the chosen ones.", ephemeral=True)
            return

        if times > 10000:
            await interaction.response.send_message("🚫 Max spam limit is 1k messages.", ephemeral=True)
            return

        await interaction.response.send_message(f"💣 Spamming {member.mention} {times} times...", ephemeral=True)

        for _ in range(times):
            try:
                await member.send(message)
                await asyncio.sleep(0.5)
            except discord.Forbidden:
                await interaction.followup.send("❌ Cannot send DMs to this user.", ephemeral=True)
                break

async def setup(bot):
    await bot.add_cog(Spammer(bot))


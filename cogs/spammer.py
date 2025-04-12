import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Spammer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spam", description="Spam a specific user in DMs")
    @app_commands.describe(member="The user to spam (must be the chosen one)", times="How many times", message="The message to send")
    async def spam(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        times: int = 5,
        message: str = "Hello!"
    ):
        vip_role_name = "🏆| V.I.P"
        allowed_user_id = {1028724015969341520, 706346550078603350}

        if vip_role_name not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message("🚫 You must have the VIP role to use this command.", ephemeral=True)
            return

        if member.id != allowed_user_id:
            await interaction.response.send_message("🚫 You can only spam the chosen one stupid.", ephemeral=True)
            return

        if times > 1000:
            await interaction.response.send_message("🚫 Max spam limit is 1000 messages.", ephemeral=True)
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

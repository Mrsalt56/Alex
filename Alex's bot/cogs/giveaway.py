import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}

    @app_commands.command(name="start_giveaway", description="Start a giveaway with a specified duration and prize.")
    async def start_giveaway(self, interaction: discord.Interaction, duration: int, prize: str):
        """Starts a giveaway with the given duration (in seconds) and prize."""
        embed = discord.Embed(title="🎉 Giveaway! 🎉", description=f"Prize: {prize}\nReact with 🎉 to enter!", color=discord.Color.blue())
        embed.set_footer(text=f"Ends in {duration} seconds.")
        giveaway_message = await interaction.channel.send(embed=embed)
        await giveaway_message.add_reaction("🎉")
        
        self.active_giveaways[giveaway_message.id] = (interaction.channel.id, prize)
        
        await interaction.response.send_message(f"Giveaway started for {prize}! Ends in {duration} seconds.", ephemeral=True)
        
        await asyncio.sleep(duration)
        await self.end_giveaway(interaction, giveaway_message.id)

    async def end_giveaway(self, interaction: discord.Interaction, message_id: int):
        if message_id not in self.active_giveaways:
            return
        
        channel_id, prize = self.active_giveaways.pop(message_id)
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        
        for reaction in message.reactions:
            if reaction.emoji == "🎉":
                users = []
                async for user in reaction.users():
                    if user != self.bot.user:
                        users.append(user)
                
                if users:
                    winner = random.choice(users)
                    await channel.send(f"🎉 Congratulations {winner.mention}! You won {prize}!")
                else:
                    await channel.send("No valid entries, no winner was selected.")
                return
        
        await channel.send("No reactions detected, giveaway canceled.")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.tree.synced:
            self.bot.tree.copy_global_to(guild=discord.Object(id=1157708242194022412))
            await self.bot.tree.sync(guild=discord.Object(id=1157708242194022412))
            print("Slash commands synced.")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))


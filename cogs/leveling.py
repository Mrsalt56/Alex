import math
import random
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.milestone_roles = {5: 1186334101117079622, 10: 234567890123456789, 15: 345678901234567890, 
                                20: 456789012345678901, 30: 567890123456789012, 40: 678901234567890123, 
                                50: 789012345678901234, 100: 890123456789012345}  # Replace with actual role IDs

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling is online!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)",
                           (guild_id, user_id, cur_level, xp, level_up_xp))
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += random.randint(1, 25)

            if xp >= level_up_xp:
                cur_level += 1
                new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)

                await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")
                
                if cur_level in self.milestone_roles:
                    role_id = self.milestone_roles[cur_level]
                    role = message.guild.get_role(role_id)
                    if role:
                        await message.author.add_roles(role)
                        await message.channel.send(f"{message.author.mention} has been given the **{role.name}** role!")
                    else:
                        await message.channel.send(f"Role with ID **{role_id}** not found. Please ensure it exists.")

                cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?",
                               (cur_level, xp, new_level_up_xp, guild_id, user_id))

            cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))

        connection.commit()
        connection.close()

    @app_commands.command(name="level", description="Sends the level card for a given user.")
    async def level(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        member_id = member.id
        guild_id = interaction.guild.id

        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message(f"{member.name} currently does not have a level.")
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]
            achieved_milestones = [lvl for lvl in self.milestone_roles.keys() if lvl <= level]

            if achieved_milestones:
                highest_milestone = max(achieved_milestones)
                rank_role = interaction.guild.get_role(self.milestone_roles[highest_milestone])
                rank_message = f"Current Rank: {rank_role.name}" if rank_role else "Current Rank: Unknown"
            else:
                rank_message = "No milestone rank achieved yet."

            await interaction.response.send_message(
                f"Level Statistics for {member.name}:\nLevel: {level}\nXP: {xp}\nXP to Level Up: {level_up_xp}\n{rank_message}"
            )

        connection.close()

async def setup(bot):
    await bot.add_cog(LevelSys(bot))


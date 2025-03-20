import discord
from discord.ext import commands

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_name = "📊 SERVER STATS 📊"
        self.channels = {
            "all_members": "👥 All Members: {}",
            "humans": "👤 Members: {}",
            "bots": "🤖 Bots: {}"
        }

    async def update_stats(self, guild):
        """Creates or updates voice channels with server stats"""
        category = discord.utils.get(guild.categories, name=self.category_name)

        if not category:
            category = await guild.create_category(self.category_name)

        all_members = guild.member_count
        human_members = len([m for m in guild.members if not m.bot])
        bot_members = all_members - human_members

        stats_data = {
            "all_members": all_members,
            "humans": human_members,
            "bots": bot_members
        }

        for key, name in self.channels.items():
            channel_name = name.format(stats_data[key])
            existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)

            if not existing_channel:
                # Check if a channel with the old name exists and rename it
                old_channel = discord.utils.get(guild.voice_channels, name__startswith=self.channels[key].split(":")[0])
                if old_channel:
                    await old_channel.edit(name=channel_name)
                else:
                    await guild.create_voice_channel(channel_name, category=category)

    @commands.Cog.listener()
    async def on_ready(self):
        """Update stats for all guilds when the bot starts"""
        for guild in self.bot.guilds:
            await self.update_stats(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Update stats when a member joins"""
        await self.update_stats(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Update stats when a member leaves"""
        await self.update_stats(member.guild)

async def setup(bot):
    await bot.add_cog(ServerStats(bot))

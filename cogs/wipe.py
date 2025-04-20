import discord
from discord.ext import commands

class Wipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wipe')
    @commands.has_permissions(administrator=True)
    async def wipe(self, ctx):
        confirm_msg = await ctx.send("⚠️ Are you sure you want to **wipe the server**? Type `CONFIRM` within 15 seconds to proceed.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content == "CONFIRM"

        try:
            confirm = await self.bot.wait_for('message', timeout=15.0, check=check)
        except:
            return await ctx.send("❌ Wipe cancelled. You didn't confirm in time.")

        await ctx.send("🧹 Wiping server...")

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except Exception as e:
                print(f"Could not delete channel {channel}: {e}")

        for role in ctx.guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                except Exception as e:
                    print(f"Could not delete role {role}: {e}")

        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
            except Exception as e:
                print(f"Could not delete emoji {emoji}: {e}")
              
        try:
            new_channel = await ctx.guild.create_text_channel("general")
            await new_channel.send("✅ Server has been wiped clean.")
        except Exception as e:
            print(f"Could not create channel: {e}")

async def setup(bot):
    await bot.add_cog(Wipe(bot))

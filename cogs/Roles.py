import discord
from discord.ext import commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None 
        self.emoji_to_role = {
            "⚔️": 1186323833691582525,
            "🧸": 1186323959470366871,
            "🤝": 1186324182154346597,
            "🏆": 1186324231647141908,
            "🫂": 1186324329395388446,
            "👀": 1186324421892378634,
            "⌨️": 1186331021881380935,
            "🎮": 1186331073278378124,
            "🧩": 1186331119071793312,
            "📱": 1186331121579999233,
            "💙": 1186305412836884482,
            "🤍": 1186305577710784562,
            "❤️": 1186305704512983090,
            "💚": 1186305824663011378,
            "💛": 1186305893806133298,
            "🤎": 1186305994603642910,
            "🧡": 1186306081266356395,
            "💜": 1186307132174381056,
            "🖤": 1186306183506702447,
            "🟢": 1186314011248164894,
            "🟤": 1186314351758540840,
            "⚪": 1186314380749574284,
            "🟡": 1186314601558716416,
            "🔵": 1186314734530740356,
            "🟣": 1186314819708670014,
            "🔴": 1186314900037980211,
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.message_id:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_id = self.emoji_to_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.message_id:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_id = self.emoji_to_role.get(str(payload.emoji))
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.remove_roles(role)

    @commands.command()
    async def send_reaction_embed(self, ctx):
        embed = discord.Embed(
            title="Types of Brawlhalla Players",
            description="This is where people can figure out the type of brawlhalla player you are such as if you are competitive, love to do free for all, mostly just does random modes, etc! This will divide the type of players and if people see a connection it will be way more easier for yall to play!""‎\n ⚔️ ・Competitive\n 🧸 ・Casual\n 🤝 ・Socializers\n 🏆 ・Teachers\n 🫂 ・Anything Goes\n 👀 ・Here To Watch\n\nReact to get the role!",
            color=discord.Color.blue(),
            )

        message = await ctx.send(embed=embed)
        await message.add_reaction("⚔️")
        await message.add_reaction("🧸")
        await message.add_reaction("🤝")
        await message.add_reaction("🏆")
        await message.add_reaction("🫂")
        await message.add_reaction("👀")

        embed = discord.Embed(
            title="Consoles",
            description="‎\n⌨️・PC\n🎮・PS/XBOX\n🧩・Nintendo Switch\n📱・Mobile\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )


        message = await ctx.send(embed=embed)
        await message.add_reaction("⌨️")
        await message.add_reaction("🎮")
        await message.add_reaction("🧩")
        await message.add_reaction("📱")
        
        embed = discord.Embed(
            title="Brawlhalla Server Region",
            description="This is where you pick the server region that suits best for you when playing Brawlhalla! I know sometimes regions like US-W doesn't go well with going against a player like all the way in EU, but this is able to help players know what they are going to fight, fellow people from the region to friend, and even better if you ever 1v1 me, I will switch the server region for those selected players!""‎\n💙・Region US-E\n🤍・Region US-W\n❤️・Region Brazil\n💚・Region Europe\n💛・Region Southern Africa\n🤎・Region Middle East\n🧡・Region SE Asia\n💜・Region Japan\n🖤・Region Australia\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )


        message = await ctx.send(embed=embed)
        await message.add_reaction("💙")
        await message.add_reaction("🤍")
        await message.add_reaction("❤️")
        await message.add_reaction("💚")
        await message.add_reaction("💛")
        await message.add_reaction("🤎")
        await message.add_reaction("🧡")
        await message.add_reaction("💜")
        await message.add_reaction("🖤")
        
        
        embed = discord.Embed(
            title="Brawlhalla Rank",
            description="This is where you are able to select the rank that you are in brawlhalla! All the way from Tin to Valhallan. This might be helpful in meeting people who are higher ranked that you can grab a partner from, asking for help/advice, 1v1s, 2v2s, etc!""‎\n🟢・Rank Tin\n🟤・Rank Bronze\n⚪・Rank Silver\n🟡・Rank Gold\n🔵・Rank Platnium\n🟣・Rank Diamond\n🔴・Rank Valhallan\n\nReact below to get your role!",
            color=discord.Color.blue(),
        )


        message = await ctx.send(embed=embed)
        await message.add_reaction("🟢")
        await message.add_reaction("🟤")
        await message.add_reaction("⚪")
        await message.add_reaction("🟡")
        await message.add_reaction("🔵")
        await message.add_reaction("🟣")
        await message.add_reaction("🔴")
        
        self.message_id = message.id

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))

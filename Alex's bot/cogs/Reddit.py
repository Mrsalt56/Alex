import discord
from discord import app_commands
from discord.ext import commands
from random import choice
import asyncpraw as praw

class Reddit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id="kGBY8cTDauoGHT5s8FguwQ",
            client_secret="61N1wLkuA22WDiDHAtXVDmOBJw16og",
            user_agent="script:Randommeme:v1.0 (by u/Mrsalt56)"
        )
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready!")
    
    @app_commands.command(name="meme", description="Fetches a random meme from r/memes")
    async def meme(self, interaction: discord.Interaction):
        subreddit = await self.reddit.subreddit("memes")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if (not post.over_18 and post.author is not None and 
                any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"])):
                author_name = post.author.name if post.author else "N/A"
                posts_list.append((post.url, author_name))

        if posts_list:
            random_post = choice(posts_list)
            meme_embed = discord.Embed(
                title="Random Meme",
                description="Here’s a meme from r/memes!",
                color=discord.Color.random()
            )
            meme_embed.set_author(name=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Post by {random_post[1]}")
            
            await interaction.response.send_message(embed=meme_embed)
        else:
            await interaction.response.send_message("Unable to fetch posts, try again later.", ephemeral=True)
    
    async def cog_unload(self):
        await self.reddit.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Reddit(bot))

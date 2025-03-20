import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop_mode = "off"
        self.currently_playing = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")
        await bot.tree.sync()
    
    async def join_voice(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You need to be in a voice channel!", ephemeral=True)
            return None
        vc = await interaction.user.voice.channel.connect()
        return vc

    @app_commands.command(name="join", description="Join a voice channel")
    async def join(self, interaction: discord.Interaction):
        await self.join_voice(interaction)
        await interaction.response.send_message("Joined voice channel!")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            self.queue.clear()
            await interaction.response.send_message("Disconnected!")
        else:
            await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)

    @app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        vc = interaction.guild.voice_client
        if not vc:
            vc = await self.join_voice(interaction)
            if not vc:
                return

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True,
            'extract_flat': False,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]

            url = info['url']
            title = info.get('title', 'Unknown Title')

        self.queue.append((title, url))

        if not vc.is_playing():
            await self.play_next(vc)

        await interaction.followup.send(f"Added to queue: {title}")

    async def play_next(self, vc):
        if self.queue:
            title, url = self.queue.pop(0)
            self.currently_playing = title

            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }

            vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: self.bot.loop.create_task(self.play_next(vc)))

    @app_commands.command(name="pause", description="Pause the current song")
    async def pause(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("Paused music.")

    @app_commands.command(name="resume", description="Resume the paused song")
    async def resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("Resumed music.")

    @app_commands.command(name="stop", description="Stop the current song")
    async def stop(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc:
            vc.stop()
            self.queue.clear()
            await interaction.response.send_message("Stopped playback.")

    @app_commands.command(name="queue", description="Show the current song queue")
    async def queue(self, interaction: discord.Interaction):
        if not self.queue:
            await interaction.response.send_message("Queue is empty!", ephemeral=True)
            return

        queue_str = "\n".join([f"{i+1}. {track[0]}" for i, track in enumerate(self.queue)])
        await interaction.response.send_message(f"Current Queue:\n{queue_str}")

async def setup(bot):
    await bot.add_cog(Music(bot))



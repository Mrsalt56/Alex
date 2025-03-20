import discord
from discord.ext import commands, tasks
import aiohttp

TWITCH_CLIENT_ID = "hlqe6fqv7p3l49xf3tz4k1fdplvwul"  # Replace with your actual Client ID
TWITCH_CLIENT_SECRET = "2o4rqr7imzb0nhw3v6vqyf02wg2cel"  # Replace with your actual Client Secret
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_STREAMS_URL = "https://api.twitch.tv/helix/streams"

class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.streamers = {"mrsalt56": False, "alexplaysyt2": False, "t0tal_toxivity": False}  # Initialize as a dictionary
        self.access_token = "p7s10fkp9gchahw5npin4k9eiv3nrx"  # Use the provided OAuth token
        self.check_twitch.start()  # Start the task after defining it

    async def get_access_token(self):
        """Fetch a new Twitch access token (if needed)."""
        async with aiohttp.ClientSession() as session:
            async with session.post(TWITCH_TOKEN_URL, data={
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_CLIENT_SECRET,
                "grant_type": "client_credentials"
            }) as resp:
                data = await resp.json()
                if "access_token" in data:
                    self.access_token = data["access_token"]
                    print(f"New Twitch Access Token: {self.access_token}")
                else:
                    print(f"Failed to get Twitch access token: {data}")

    async def check_stream_status(self, streamer):
        """Check if a streamer is live."""
        if not self.access_token:
            await self.get_access_token()
        
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {"user_login": streamer}
        async with aiohttp.ClientSession() as session:
            async with session.get(TWITCH_STREAMS_URL, headers=headers, params=params) as resp:
                data = await resp.json()
                print(f"Twitch API Response for {streamer}: {data}")  # Debugging line
                return bool(data.get("data"))

    @tasks.loop(minutes=5)
    async def check_twitch(self):
        """Periodic task to check stream status for all streamers."""
        if not self.access_token:
            await self.get_access_token()

        for streamer in self.streamers.keys():
            is_live = await self.check_stream_status(streamer)
            print(f"{streamer} live status: {is_live}")  # Debugging line

            if is_live and not self.streamers[streamer]:
                self.streamers[streamer] = True
                channel = self.bot.get_channel(1186468805082370130)  # Replace with your channel ID
                if channel:
                    await channel.send(f"@everyone {streamer} is now LIVE! Check them out at https://www.twitch.tv/{streamer}")
            elif not is_live:
                self.streamers[streamer] = False

    @commands.command()
    async def add_streamer(self, ctx, streamer: str):
        """Add a new streamer to the watch list."""
        if streamer.lower() not in self.streamers:
            self.streamers[streamer.lower()] = False
            await ctx.send(f"Added {streamer} to the watch list.")
        else:
            await ctx.send(f"{streamer} is already in the watch list.")

    @commands.command()
    async def remove_streamer(self, ctx, streamer: str):
        """Remove a streamer from the watch list."""
        if streamer.lower() in self.streamers:
            del self.streamers[streamer.lower()]
            await ctx.send(f"Removed {streamer} from the watch list.")
        else:
            await ctx.send(f"{streamer} is not in the watch list.")

async def setup(bot):
    """Setup the TwitchNotifier cog."""
    await bot.add_cog(TwitchNotifier(bot))

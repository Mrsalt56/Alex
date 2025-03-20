import discord
from discord.ext import commands
from discord.ui import Button, View

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_ticket(self, ctx):
        """Creates a ticket system with a button for users to create a ticket"""
        button = Button(label="Create Ticket", style=discord.ButtonStyle.green)

        async def button_callback(interaction):
            tickets_category = discord.utils.get(ctx.guild.categories, name="tickets")
            if not tickets_category:
                await interaction.response.send_message("The 'tickets' category does not exist. Please create it first.", ephemeral=True)
                return

            existing_ticket = discord.utils.get(ctx.guild.text_channels, name=f'ticket-{interaction.user.name}')
            if existing_ticket:
                await interaction.response.send_message("You already have an open ticket!", ephemeral=True)
                return

            mini_mod_role = discord.utils.get(ctx.guild.roles, name="💻 | Mini Mod")
            mod_role = discord.utils.get(ctx.guild.roles, name="⚜️ | M.O.D")

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),  
                interaction.user: discord.PermissionOverwrite(view_channel=True),
            }

            if mini_mod_role:
                overwrites[mini_mod_role] = discord.PermissionOverwrite(view_channel=True)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True)


            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{interaction.user.name}', category=tickets_category, overwrites=overwrites)

            await ticket_channel.send(f'Hello {interaction.user.mention}, how can we assist you today?')

            await interaction.response.send_message(f"Your ticket has been created in the {ticket_channel.mention} channel.", ephemeral=True)

        button.callback = button_callback

        view = View()
        view.add_item(button)

        await ctx.send("Click the button below to create a support ticket.", view=view)

    @commands.command()
    async def close_ticket(self, ctx):
        """Closes the user's ticket channel"""
        if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name.startswith('ticket-'):
            if ctx.channel.name == f'ticket-{ctx.author.name}' or any(role.name in ["💻 | Mini Mod", "⚜️ | M.O.D"] for role in ctx.author.roles):
                await ctx.channel.delete()
                await ctx.send("Your ticket has been closed.", delete_after=5)
            else:
                await ctx.send("You don't have permission to close this ticket.", ephemeral=True)
        else:
            await ctx.send("This is not a valid ticket channel.")

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))






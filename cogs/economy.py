import discord
from discord.ext import commands , tasks
from discord import app_commands
import json
import os
import datetime
import random
import asyncio
import time

SHOP_ITEMS = {   
    "Toys": {"price": 500, "description": "Have fun"},
    "Bike": {"price": 1000, "description": "Travel safe"},
    "Car": {"price": 15000, "description": "Better than a bike"},
    "House": {"price": 30000, "description": "Have fun"},
    "Plane": {"price": 50000, "description": "Travel safe"},
    "Lucky Cat": {"price": 10000, "description": "A lucky cat that boosts your earnings when working and gambling."},
    "Four-Leaf Clover": {"price": 11000, "description": "A four-leaf clover that increases your luck in gambling."},
    "Dragon": {"price": 12000, "description": "A dragon that boosts both your work earnings and gambling winnings."},
    "Lucky Apple": {"price": 5000, "description": "A lucky apple that boosts your luck for 1 to 20 minutes."},
    "Golden Banana": {"price": 6000, "description": "A golden banana that boosts your luck for 1 to 20 minutes."},
    "Magic Pear": {"price": 10000, "description": "A magic pear that boosts your luck for 1 to 20 minutes."},
    "color_role": {"price": 1000, "description": "A custom color role"},
    "custom_name": {"price": 2000, "description": "A custom name"},
}

STOCKS = {
    "TechCorp": {"price": 500, "description": "A leading tech company.", "volatility": 0.05}, 
    "GreenEnergy": {"price": 800, "description": "A green energy company.", "volatility": 0.07},  
    "BioPharm": {"price": 1200, "description": "A biotechnology firm.", "volatility": 0.1}, 
}

REAL_ESTATE = {
    "Small Apartment": {"price": 10000, "income": 100},  
    "Mansion": {"price": 50000, "income": 500}, 
    "Beachfront Property": {"price": 100000, "income": 1000}, 
}

BUSINESSES = {
    "Coffee Shop": {"price": 20000, "income": 200},
    "Restaurant": {"price": 50000, "income": 500},  
    "Tech Startup": {"price": 100000, "income": 1000}, 
}

def calculate_tax(self, player_id):
        tax_rate = 0.1
        wealth = self.players[player_id]['wealth']
        businesses = self.players[player_id].get('businesses', 0)
        properties = self.players[player_id].get('properties', 0)       
        total_assets = wealth + (businesses * 1000) + (properties * 500)
        tax = total_assets * tax_rate
        return tax

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'db/economy.json'
        self.load_data()
        self.work_cooldowns = {}
        self.trade_requests = {}
        self.stocks = {} 
        self.real_estate = {}  
        self.businesses = {}
        self.lottery_tickets = []
        self.collect_taxes.start()
        self.players = {}
        self.REQUEST_CHANNEL_ID = 1350889815473651825
        
       
    def load_data(self):
        if not os.path.exists('db'):
            os.makedirs('db')

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
                if not isinstance(self.data.get("users"), dict):
                    self.data["users"] = {}
        else:
            self.data = {"users": {}}
            self.save_data()

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    @app_commands.command(name="balance", description="Check your current balance.")
    async def balance(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        user_data = self.data["users"][user_id]
        bandit_bucks = user_data.get("bandit_bucks", 0)

        await interaction.response.send_message(f"{interaction.user.name}, you currently have __**{bandit_bucks}**__ Bandit Bucks!")

    @app_commands.command(name="register", description="Register a new account.")
    async def register(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id in self.data["users"]:
            await interaction.response.send_message("You already have an account.", ephemeral=True)
            return

        self.data["users"][user_id] = {
            "username": str(interaction.user),
            "registered_at": str(datetime.datetime.utcnow()),
            "last_claimed_daily": "",
            "last_claimed_weekly": "",
            "bandit_bucks": 0,
            "inventory": []
        }
        self.save_data()

        await interaction.response.send_message(f"Successfully registered {interaction.user.mention}!")

    @app_commands.command(name="daily", description="Claim daily reward.")
    async def daily(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        user_data = self.data["users"][user_id]

        if user_data["last_claimed_daily"] == today_str:
            await interaction.response.send_message("You have already claimed your daily reward today.", ephemeral=True)
            return

        user_data["last_claimed_daily"] = today_str
        user_data["bandit_bucks"] += 50
        self.save_data()

        await interaction.response.send_message(f"You have claimed your daily reward of 50 Bandit Bucks, {interaction.user.mention}!")

    @app_commands.command(name="work", description="Work to earn a random amount of Bandit Bucks.")
    async def work(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        now = datetime.datetime.utcnow()

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        last_work_time = self.work_cooldowns.get(user_id)
        if last_work_time and (now - last_work_time).total_seconds() < 600:
            remaining_time = 600 - (now - last_work_time).total_seconds()
            await interaction.response.send_message(f"You need to wait {int(remaining_time // 60)} minutes and {int(remaining_time % 60)} seconds before working again.", ephemeral=True)
            return

        user_data = self.data["users"][user_id]
        luck_boost = 1.0  
        luck_duration = 0  

        for pet in user_data["inventory"]:
            if pet == "Lucky Cat":
                luck_boost = 1.2  
            elif pet == "Dragon":
                luck_boost = 1.5  
            elif pet in ["Lucky Apple", "Golden Banana", "Magic Pear"]:
                luck_boost = 1.5
                luck_duration = random.randint(1, 20)  

        earnings = random.randint(100, 600) * luck_boost
        self.data["users"][user_id]["bandit_bucks"] += int(earnings)
        self.work_cooldowns[user_id] = now
        self.save_data()

        if luck_duration > 0:
            await interaction.response.send_message(f"You worked hard and earned {int(earnings)} Bandit Bucks! Your luck boost lasts for {luck_duration} minutes.")
        else:
            await interaction.response.send_message(f"You worked hard and earned {int(earnings)} Bandit Bucks!")

    @app_commands.command(name="shop", description="View the shop and buy items.")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Shop",
            description="Welcome to the shop! Here are the items you can buy:",
            color=discord.Color.gold()
        )

        for item, details in SHOP_ITEMS.items():
            embed.add_field(
                name=item.capitalize(),
                value=f"Price: {details['price']} Bandit Bucks\nDescription: {details['description']}",
                inline=False
            )

        embed.set_footer(text="Use /buy <item> to purchase an item.")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Buy an item from the shop.")
    async def buy(self, interaction: discord.Interaction, item: str):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message(
                "You need to register first. Use the `/register` command.", ephemeral=True
            )
            return

        if item not in SHOP_ITEMS:
            await interaction.response.send_message(
                "This item does not exist in the shop.", ephemeral=True
            )
            return

        user_data = self.data["users"][user_id]
        item_price = SHOP_ITEMS[item]["price"]

        if user_data["bandit_bucks"] < item_price:
            await interaction.response.send_message(
                f"❌ You do not have enough Bandit Bucks to buy **{item.capitalize()}**. You need **{item_price} BB**.",
                ephemeral=True,
            )
            return

        user_data["bandit_bucks"] -= item_price
        user_data.setdefault("inventory", []).append(item)
        self.save_data()

        request_channel = self.bot.get_channel(self.REQUEST_CHANNEL_ID)
        if request_channel:
            await request_channel.send(
                f"📢 **Purchase Alert** 📢\n{interaction.user.mention} has bought **{item.capitalize()}** for **{item_price} Bandit Bucks**!"
            )
        else:
            await interaction.response.send_message("⚠️ Error: Request channel not found!")

        await interaction.response.send_message(
            f"✅ You have successfully bought **{item.capitalize()}** for **{item_price} Bandit Bucks**!"
        )

    @app_commands.command(name="inventory", description="Check your inventory.")
    async def inventory(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return
        
        inventory = self.data["users"][user_id].get("inventory", [])
        if not inventory:
            await interaction.response.send_message("Your inventory is empty.")
        else:
            item_counts = {item: inventory.count(item) for item in set(inventory)}
            inventory_list = "\n".join([f"{item.capitalize()}: {count}" for item, count in item_counts.items()])
            await interaction.response.send_message(f"Your inventory:\n{inventory_list}")

    @app_commands.command(name="gamble", description="Gamble to win or lose Bandit Bucks!")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        user_data = self.data["users"][user_id]
        current_balance = user_data["bandit_bucks"]

        if amount <= 0:
            await interaction.response.send_message("You must gamble a positive amount.", ephemeral=True)
            return

        if amount > current_balance:
            await interaction.response.send_message(f"You do not have enough Bandit Bucks to gamble {amount}.", ephemeral=True)
            return

        luck_boost = 1.0  
        luck_duration = 0  

        for pet in user_data["inventory"]:
            if pet == "Four-Leaf Clover":
                luck_boost = 1.3  
            elif pet == "Dragon":
                luck_boost = 1.5 
            elif pet in ["Lucky Apple", "Golden Banana", "Magic Pear"]:
                luck_boost = 1.5 
                luck_duration = random.randint(1, 20)

        win = random.choice([True, False])

        if win:
            winnings = amount * 2 * luck_boost
            user_data["bandit_bucks"] += int(winnings)
            self.save_data()

            if luck_duration > 0:
                await interaction.response.send_message(f"Congratulations {interaction.user.mention}! You won {int(winnings)} Bandit Bucks! Your luck boost lasted for {luck_duration} minutes.")
            else:
                await interaction.response.send_message(f"Congratulations {interaction.user.mention}! You won {int(winnings)} Bandit Bucks!")
        else:
            user_data["bandit_bucks"] -= amount
            self.save_data()

            if luck_duration > 0:
                await interaction.response.send_message(f"Sorry {interaction.user.mention}, you lost {amount} Bandit Bucks. Better luck next time! Your luck boost lasted for {luck_duration} minutes.")
            else:
                await interaction.response.send_message(f"Sorry {interaction.user.mention}, you lost {amount} Bandit Bucks. Better luck next time!")

            
    @app_commands.command(name="trade", description="Send a trade request to another user.")
    async def trade(self, interaction: discord.Interaction, target_user: discord.User, amount: int, item: str = None):
        user_id = str(interaction.user.id)
        target_user_id = str(target_user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        if target_user_id not in self.data["users"]:
            await interaction.response.send_message(f"{target_user.mention} needs to register first. Use the `register` command.", ephemeral=True)
            return

        if amount <= 0:
            await interaction.response.send_message("You must trade a positive amount of Bandit Bucks.", ephemeral=True)
            return

        if item and item not in SHOP_ITEMS:
            await interaction.response.send_message("This item does not exist in the shop.", ephemeral=True)
            return

        user_data = self.data["users"][user_id]
        target_user_data = self.data["users"][target_user_id]

        if amount > user_data["bandit_bucks"]:
            await interaction.response.send_message(f"You don't have enough Bandit Bucks to trade {amount}.", ephemeral=True)
            return

        self.trade_requests[user_id] = {
            "target": target_user_id,
            "amount": amount,
            "item": item
        }

        await interaction.response.send_message(f"Trade request sent to {target_user.mention}.\n"
                                                f"Trade {amount} Bandit Bucks" + (f" and {item}" if item else "") + ".")

        try:
            await target_user.send(f"{interaction.user.mention} has sent you a trade request.\n"
                                   f"Trade {amount} Bandit Bucks" + (f" and {item}" if item else "") + ".\n"
                                   "Use `/accept_trade` to accept or `/decline_trade` to decline.")
        except discord.Forbidden:
            await interaction.response.send_message(f"Couldn't notify {target_user.mention}. They have DMs disabled.", ephemeral=True)

    @app_commands.command(name="accept_trade", description="Accept a trade request.")
    async def accept_trade(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.trade_requests:
            await interaction.response.send_message("You don't have any trade requests pending.", ephemeral=True)
            return

        trade_request = self.trade_requests[user_id]
        target_user_id = trade_request["target"]
        amount = trade_request["amount"]
        item = trade_request["item"]

        target_user_data = self.data["users"][target_user_id]
        user_data = self.data["users"][user_id]

        if amount > target_user_data["bandit_bucks"]:
            await interaction.response.send_message(f"{target_user_id} doesn't have enough Bandit Bucks for the trade.", ephemeral=True)
            return

        if item and item not in target_user_data["inventory"]:
            await interaction.response.send_message(f"{target_user_id} doesn't have {item} in their inventory.", ephemeral=True)
            return

        user_data["bandit_bucks"] += amount
        target_user_data["bandit_bucks"] -= amount

        if item:
            target_user_data["inventory"].remove(item)
            user_data["inventory"].append(item)

        del self.trade_requests[user_id]

        self.save_data()

        await interaction.response.send_message(f"Trade successful! {interaction.user.mention} and {target_user_id} have completed their trade.")

    @app_commands.command(name="decline_trade", description="Decline a trade request.")
    async def decline_trade(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.trade_requests:
            await interaction.response.send_message("You don't have any trade requests pending.", ephemeral=True)
            return

        del self.trade_requests[user_id]
        await interaction.response.send_message("Trade request declined.")
        
    @app_commands.command(name="stocks", description="View the stocks you can invest in.")
    async def stocks(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Stocks",
            description="Here are the stocks available for investment:",
            color=discord.Color.blue()
        )

        for stock, details in STOCKS.items():
            embed.add_field(
                name=stock,
                value=f"Price: {details['price']} Bandit Bucks\nDescription: {details['description']}\nVolatility: {details['volatility'] * 100}%",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy_stock", description="Invest in a stock.")
    async def buy_stock(self, interaction: discord.Interaction, stock: str, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        if stock not in STOCKS:
            await interaction.response.send_message("This stock does not exist.", ephemeral=True)
            return

        stock_price = STOCKS[stock]["price"]
        total_cost = stock_price * amount

        user_data = self.data["users"][user_id]
        if user_data["bandit_bucks"] < total_cost:
            await interaction.response.send_message(f"You don't have enough Bandit Bucks to invest in {stock}.", ephemeral=True)
            return

        user_data["bandit_bucks"] -= total_cost
        if user_id not in self.stocks:
            self.stocks[user_id] = {}

        if stock in self.stocks[user_id]:
            self.stocks[user_id][stock] += amount
        else:
            self.stocks[user_id][stock] = amount

        self.save_data()

        await interaction.response.send_message(f"You have successfully invested {amount} in {stock}!")
        
    @app_commands.command(name="sell_stock", description="Sell your stocks for Bandit Bucks.")
    async def sell_stock(self, interaction: discord.Interaction, stock: str, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.stocks or stock not in self.stocks[user_id]:
            await interaction.response.send_message("You don't own this stock.", ephemeral=True)
            return

        if self.stocks[user_id][stock] < amount:
            await interaction.response.send_message("You don't have enough shares to sell.", ephemeral=True)
            return

        stock_price = STOCKS[stock]["price"] 
        total_earnings = stock_price * amount

        self.stocks[user_id][stock] -= amount
        if self.stocks[user_id][stock] == 0:
            del self.stocks[user_id][stock]

        self.data["users"][user_id]["bandit_bucks"] += total_earnings

        await interaction.response.send_message(f"You have successfully sold {amount} shares of {stock} for {total_earnings} Bandit Bucks!")


    @app_commands.command(name="real_estate", description="View properties you can buy.")
    async def real_estate(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Real Estate",
            description="Here are the properties you can buy:",
            color=discord.Color.green()
        )

        for property, details in REAL_ESTATE.items():
            embed.add_field(
                name=property,
                value=f"Price: {details['price']} Bandit Bucks\nIncome: {details['income']} Bandit Bucks per cycle",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy_property", description="Buy a property.")
    async def buy_property(self, interaction: discord.Interaction, property: str):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        if property not in REAL_ESTATE:
            await interaction.response.send_message("This property does not exist.", ephemeral=True)
            return

        property_price = REAL_ESTATE[property]["price"]
        user_data = self.data["users"][user_id]

        if user_data["bandit_bucks"] < property_price:
            await interaction.response.send_message(f"You don't have enough Bandit Bucks to buy {property}.", ephemeral=True)
            return

        user_data["bandit_bucks"] -= property_price
        if user_id not in self.real_estate:
            self.real_estate[user_id] = []

        self.real_estate[user_id].append(property)
        self.save_data()

        await interaction.response.send_message(f"You have successfully bought {property}!")

    @app_commands.command(name="businesses", description="View businesses you can start.")
    async def businesses(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Businesses",
            description="Here are the businesses you can start:",
            color=discord.Color.purple()
        )

        for business, details in BUSINESSES.items():
            embed.add_field(
                name=business,
                value=f"Price: {details['price']} Bandit Bucks\nIncome: {details['income']} Bandit Bucks per cycle",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="start_business", description="Start a business.")
    async def start_business(self, interaction: discord.Interaction, business: str):
        user_id = str(interaction.user.id)

        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return

        if business not in BUSINESSES:
            await interaction.response.send_message("This business does not exist.", ephemeral=True)
            return

        business_price = BUSINESSES[business]["price"]
        user_data = self.data["users"][user_id]

        if user_data["bandit_bucks"] < business_price:
            await interaction.response.send_message(f"You don't have enough Bandit Bucks to start {business}.", ephemeral=True)
            return

        user_data["bandit_bucks"] -= business_price
        if user_id not in self.businesses:
            self.businesses[user_id] = []

        self.businesses[user_id].append(business)
        self.save_data()

        await interaction.response.send_message(f"You have successfully started {business}!")

    @app_commands.command(name="buy_ticket", description="Buy a ticket for the lottery!")
    async def buy_ticket(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        if user_id not in self.data["users"]:
            await interaction.response.send_message("You need to register first. Use the `register` command.", ephemeral=True)
            return
        
        user_data = self.data["users"][user_id]
        ticket_price = 500 

        if user_data["bandit_bucks"] < ticket_price:
            await interaction.response.send_message("You don't have enough Bandit Bucks to buy a ticket.", ephemeral=True)
            return

        user_data["bandit_bucks"] -= ticket_price
        self.lottery_tickets.append(user_id)
        self.save_data()

        await interaction.response.send_message(f"{interaction.user.mention} has successfully bought a lottery ticket!")

    @app_commands.command(name="draw_lottery", description="Draw the lottery and pick a winner!")
    async def draw_lottery(self, interaction: discord.Interaction):
        has_role = any(role.name in ['⚜️ | M.O.D', '💻 | Mini Mod'] for role in interaction.user.roles)
        
        if not has_role:
            await interaction.response.send_message("You don't have permission to draw the lottery.", ephemeral=True)
            return

        if len(self.lottery_tickets) == 0:
            await interaction.response.send_message("No one has bought a ticket for the lottery yet.", ephemeral=True)
            return

        winner_id = random.choice(self.lottery_tickets)
        winner = self.bot.get_user(int(winner_id))

        prize = random.choice([1000, 5000, 10000])  
        winner_data = self.data["users"][winner_id]
        winner_data["bandit_bucks"] += prize

        self.lottery_tickets = []
        self.save_data()

        await interaction.response.send_message(f"Congratulations {winner.mention}! You won {prize} Bandit Bucks in the lottery! 🎉")

    @app_commands.command(name="lottery_participants", description="Check the list of people who bought tickets for the lottery.")
    async def lottery_participants(self, interaction: discord.Interaction):
        if not self.lottery_tickets:
            await interaction.response.send_message("No one has bought a ticket for the lottery yet.", ephemeral=True)
        else:
            participants = [self.bot.get_user(int(user_id)).mention for user_id in self.lottery_tickets]
            await interaction.response.send_message(f"Current lottery participants:\n" + "\n".join(participants))
            
    @app_commands.command()
    async def tax(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        if player_id not in self.players:
            self.players[player_id] = {'wealth': 1000}
        tax = self.calculate_tax(player_id)
        await interaction.response.send_message(f"The Tax Collector is here! You owe {tax} in taxes.")
    
    def calculate_tax(self, player_id):
        return self.players.get(player_id, {}).get('wealth', 1000) * 0.1 
   
    @tasks.loop(hours=10) 
    async def collect_taxes(self):
        for player_id in self.players:
            tax = self.calculate_tax(player_id)
            if self.players[player_id]['wealth'] >= tax:
                self.players[player_id]['wealth'] -= tax
                user = await self.bot.fetch_user(player_id)
                await user.send(f"The Tax Collector has taken {tax} from your account.")
            else:
                penalty = self.players[player_id]['wealth'] * 0.5
                self.players[player_id]['wealth'] -= penalty
                user = await self.bot.fetch_user(player_id)
                await user.send(f"You didn't have enough money to pay your taxes. A penalty of {penalty} was applied.")

    @collect_taxes.before_loop
    async def before_collect_taxes(self):
        await self.bot.wait_until_ready()
        
async def setup(bot):
    await bot.add_cog(Economy(bot))


import random
import discord
from discord.ext import commands
import pyfiglet
import unicodedata
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-", intents=intents)

WORDS = ["python", "discord", "developer", "hangman", "bot", "gaming", "challenge", "puzzle"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @discord.app_commands.command(name="coolrate", description="Find out how cool you are!")
    async def coolrate(self, interaction: discord.Interaction):
        embed = discord.Embed(title="CoolRate", 
                              description=f"You are {random.randrange(101)}% Cool {interaction.user.mention}", 
                              color=discord.Color.random())
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="gayrate", description="Find out how gay you are!")
    async def gayrate(self, interaction: discord.Interaction):
        embed = discord.Embed(title="GayRate", 
                              description=f"You are {random.randrange(101)}% Gay {interaction.user.mention}", 
                              color=discord.Color.random())
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="pprate", description="Check your PP size!")
    async def pprate(self, interaction: discord.Interaction):
        pp_list = ["8=D", "8==D", "8===D", "8====D", "8=====D", "8======D", "8=======D", "8========D"]
        embed = discord.Embed(title="PP Rate", description=f"Your pp {random.choice(pp_list)}")
        await interaction.response.send_message(embed=embed)
        
    @discord.app_commands.command(name="coinflip", description="Flips a coin and returns heads or tails.")
    async def coinflip(self, interaction: discord.Interaction):
        """Flips a coin and returns heads or tails."""
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"🪙 The coin landed on **{result}**!")
        
    @discord.app_commands.command(name="8ball", description="Ask the magic 8-ball a question.")
    async def _8ball(self, ctx: discord.Interaction, question: str):
        """Magic 8-ball command"""
        responses = [
            "Yes.",
            "No.",
            "Maybe.",
            "Ask again later.",
            "Definitely not.",
            "Absolutely!",
            "I'm not sure.",
            "Most likely.",
            "Try again.",
            "It's a secret.",
        ]
        
        answer = random.choice(responses)
        await ctx.response.send_message(f"Question: {question}\nAnswer: {answer}")

    @discord.app_commands.command(name="joke", description="Tells a random joke.")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't programmers like nature? It has too many bugs.",
            "I told a joke about a pencil. It had no point.",
            "What do you call fake spaghetti? An impasta!"
        ]
        selected_joke = random.choice(jokes)
        await interaction.response.send_message(selected_joke)
        
    @discord.app_commands.command(name="quote", description="Get a random inspirational quote")
    async def quote(self, interaction: discord.Interaction):
        quotes = [
            "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
            "Do what you can, with what you have, where you are. - Theodore Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "You miss 100% of the shots you don’t take. - Wayne Gretzky",
            "It does not matter how slowly you go as long as you do not stop. - Confucius"
        ]
        random_quote = random.choice(quotes)
        await interaction.response.send_message(random_quote)
        
    @discord.app_commands.command(name="hug", description="Give someone a virtual hug!")
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        """Sends a hug to a mentioned user."""
        if member == interaction.user:
            await interaction.response.send_message("You can't hug yourself, but here's a hug from me! 🤗")
        else:
            await interaction.response.send_message(f"{interaction.user.mention} gives {member.mention} a big hug! 🤗")
            
    @discord.app_commands.command(name="roll", description="Roll a dice with a specified number of sides.")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        """Rolls a dice with the specified number of sides (default is 6)."""
        if sides < 2:
            await interaction.response.send_message("The dice must have at least 2 sides!", ephemeral=True)
            return
        
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 You rolled a {result} on a {sides}-sided dice!")
        
    @discord.app_commands.command(name="rps", description="Play Rock, Paper, Scissors!")
    async def rps(self, interaction: discord.Interaction, choice: str):
        """Rock, Paper, Scissors game using a slash command"""
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        
        if choice.lower() not in choices:
            await interaction.response.send_message("Invalid choice! Please choose rock, paper, or scissors.", ephemeral=True)
            return
        
        result = self.determine_winner(choice.lower(), bot_choice)

        response = (
            f"**You chose:** {choice.capitalize()}\n"
            f"**I chose:** {bot_choice.capitalize()}\n\n"
            f"**Result:** {result}"
        )

        await interaction.response.send_message(response)

    def determine_winner(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return "It's a tie! 🤝"
        if (user_choice == "rock" and bot_choice == "scissors") or \
           (user_choice == "paper" and bot_choice == "rock") or \
           (user_choice == "scissors" and bot_choice == "paper"):
            return "You win! 🎉"
        return "I win! 😈"
    
    @discord.app_commands.command(name="slap", description="Slap another user playfully!")
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        """A fun slap command to 'attack' another user!"""
        slap_messages = [
            f"{interaction.user.mention} slaps {member.mention} with a giant fish! 🐟",
            f"{interaction.user.mention} smacks {member.mention} across the face! 👋",
            f"{interaction.user.mention} delivers a legendary slap to {member.mention}! 🔥",
            f"{interaction.user.mention} throws a slipper at {member.mention}! 🥿",
            f"{interaction.user.mention} bonks {member.mention} on the head! 🏏",
        ]
        
        response = random.choice(slap_messages)
        await interaction.response.send_message(response)
        
    @discord.app_commands.command(name="reverse", description="Reverse the given text.")
    async def reverse(self, interaction: discord.Interaction, text: str):
        """Reverses the input text and sends it back."""
        reversed_text = text[::-1]
        await interaction.response.send_message(f"🔄 **Reversed:** {reversed_text}")
        
    @discord.app_commands.command(name="compliment", description="Send a nice compliment to someone!")
    async def compliment(self, interaction: discord.Interaction, member: discord.Member):
        """Sends a random compliment to the mentioned user."""
        compliments = [
            f"{member.mention}, you light up the room like the sun! ☀️",
            f"{member.mention}, you're an amazing person with a heart of gold! 💛",
            f"{member.mention}, your kindness makes the world a better place! 🌎",
            f"{member.mention}, you have a smile that can brighten anyone's day! 😄",
            f"{member.mention}, you are incredibly talented and inspiring! ✨",
            f"{member.mention}, your positive energy is truly contagious! 🔥",
            f"{member.mention}, you are a wonderful friend and a joy to be around! ❤️",
        ]

        response = random.choice(compliments)
        await interaction.response.send_message(response)
        
    @discord.app_commands.command(name="fortune", description="Receive a random fortune!")
    async def fortune(self, interaction: discord.Interaction):
        """Sends a random fortune message."""
        fortunes = [
            "🌟 Good things are coming your way!",
            "🍀 Luck will be on your side very soon.",
            "✨ An exciting opportunity awaits you.",
            "💡 A brilliant idea will come to you today.",
            "❤️ Love and happiness will find you unexpectedly.",
            "🎉 A celebration is in your near future.",
            "🧘‍♂️ Peace and clarity will fill your mind soon.",
            "💰 Financial success is just around the corner.",
            "🚀 Take the leap—great rewards await!",
            "🔮 The universe has big plans for you. Stay positive!"
        ]

        response = random.choice(fortunes)
        await interaction.response.send_message(response)
        
    @discord.app_commands.command(name="ascii", description="Convert text into ASCII art.")
    async def ascii(self, interaction: discord.Interaction, text: str):
        """Converts input text into ASCII art using pyfiglet."""
        if len(text) > 300:
            await interaction.response.send_message("⚠️ Please enter text with 20 characters or less.", ephemeral=True)
            return

        ascii_art = pyfiglet.figlet_format(text)
        
        if len(ascii_art) > 1900:
            ascii_art = ascii_art[:1900] + "\n⚠️ Output was truncated."

        await interaction.response.send_message(f"```\n{ascii_art}\n```")
        
    @discord.app_commands.command(name="randomfact", description="Get a random fact!")
    async def randomfact(self, interaction: discord.Interaction):
        """Sends a random fact to the user."""
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old and still perfectly edible.",
            "Octopuses have three hearts, two pump blood to the gills, while the third pumps it to the rest of the body.",
            "Bananas are berries, but strawberries aren’t. In botanical terms, a berry is a fruit that comes from one flower with one ovary.",
            "A group of flamingos is called a 'flamboyance.'",
            "Cows have best friends and get stressed when they are separated.",
            "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of iron in the heat.",
            "Sharks have been around longer than trees. Sharks have existed for around 400 million years, while trees have existed for around 350 million years.",
            "The unicorn is Scotland's national animal.",
            "The shortest commercial flight in the world is in Scotland, lasting only 57 seconds between the Westray and Papa Westray islands."
        ]

        fact = random.choice(facts)
        await interaction.response.send_message(f"Here's a random fact for you: {fact}")

    @discord.app_commands.command(name="fliptext", description="Flip the given text upside down!")
    async def fliptext(self, interaction: discord.Interaction, text: str):
        """Flips the input text upside down using Unicode characters."""
        flipped_text = self.flip(text)
        
        if len(flipped_text) > 2000:
            flipped_text = flipped_text[:1900] + "\n⚠️ Output was truncated."
        
        await interaction.response.send_message(f"**Flipped Text:**\n{flipped_text}")

    def flip(self, text):
        """Flip the given text upside down using Unicode characters."""
        flip_table = {
            'a': 'ɒ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ', 'i': 'ı', 'j': 'ɾ', 'k': 'ʞ',
            'l': '⅄', 'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 
            'w': 'ʍ', 'x': 'x', 'y': 'ʎ', 'z': 'z', 'A': 'ɒ', 'B': 'q', 'C': 'ɔ', 'D': 'p', 'E': 'ǝ', 'F': 'ɟ', 'G': 'ƃ', 
            'H': 'ɥ', 'I': 'ı', 'J': 'ɾ', 'K': 'ʞ', 'L': '⅄', 'M': 'ɯ', 'N': 'u', 'O': 'o', 'P': 'd', 'Q': 'b', 'R': 'ɹ', 
            'S': 's', 'T': 'ʇ', 'U': 'n', 'V': 'ʌ', 'W': 'ʍ', 'X': 'x', 'Y': 'ʎ', 'Z': 'z', ' ': ' ', '!': '¡', '"': '„', 
            '#': '#', '$': 'ƨ', '%': '⅞', '&': '⅋', "'": ',', '(': ')', ')': '(', '*': '⋆', '+': '⊕', ',': '˙', '-': '−', 
            '.': '˙', '/': '⅄', ':': '˘', ';': '˘', '<': '>', '=': '≡', '>': '<', '?': '¿', '@': '@', '[': ']', '\\': '∩', 
            ']': '[', '^': 'ʇ', '_': '‾', '`': '˙', '{': '}', '|': '|', '}': '{', '~': '⌒'
        }

        flipped_text = ''.join([flip_table.get(c, c) for c in text[::-1]])
        return flipped_text

    @discord.app_commands.command(name="avatar", description="Get the avatar of a user.")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """Fetches the avatar of the mentioned user or the requester if no user is mentioned."""
        member = member or interaction.user

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=avatar_url)

        await interaction.response.send_message(embed=embed)
        
    @discord.app_commands.command(name="riddle", description="Get a random riddle to solve!")
    async def riddle(self, interaction: discord.Interaction):
        """Sends a random riddle to the user."""
        riddles = [
            {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "An echo"},
            {"question": "You see a house with two doors, one is locked and one is open. Which door do you choose?", "answer": "The open door"},
            {"question": "The more of this there is, the less you see. What is it?", "answer": "Darkness"},
            {"question": "What has keys but can't open locks?", "answer": "A piano"},
            {"question": "What is so fragile that saying its name breaks it?", "answer": "Silence"},
            {"question": "What can travel around the world while staying in the corner?", "answer": "A stamp"},
            {"question": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "A candle"},
            {"question": "What can be cracked, made, told, and played?", "answer": "A joke"},
        ]

        riddle = random.choice(riddles)
        question = riddle["question"]
        answer = riddle["answer"]

        await interaction.response.send_message(f"**Riddle:** {question}\nType in chat to answer!")

        def check(message):
            return message.content.lower() == answer.lower() and message.author == interaction.user

        try:
            await self.bot.wait_for("message", check=check, timeout=30) 
            await interaction.followup.send(f"🎉 Correct! The answer was: {answer}")
        except:
            await interaction.followup.send(f"Oops! Time's up. The correct answer was: {answer}")

    @discord.app_commands.command(name="whoami", description="Get information about yourself!")
    async def whoami(self, interaction: discord.Interaction):
        """Provides basic information about the user."""
        user = interaction.user
        username = user.name
        discriminator = user.discriminator
        user_id = user.id
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        embed = discord.Embed(title=f"Information about {username}", color=discord.Color.green())
        embed.add_field(name="Username", value=username, inline=True)
        embed.add_field(name="Discriminator", value=f"#{discriminator}", inline=True)
        embed.add_field(name="User ID", value=user_id, inline=True)
        embed.set_thumbnail(url=avatar_url)

        await interaction.response.send_message(embed=embed)
        
    @discord.app_commands.command(name="guessnumber", description="Guess a number between 1 and 100!")
    async def guessnumber(self, interaction: discord.Interaction):
        """Starts a new guessing game."""
        user = interaction.user
        if user.id in self.games:
            await interaction.response.send_message("You already have an ongoing game! Finish that one first.")
            return

        number = random.randint(1, 100)
        self.games[user.id] = {"number": number, "attempts": 0}

        await interaction.response.send_message("I've picked a number between 1 and 100. Start guessing!")

    @discord.app_commands.command(name="guess", description="Guess a number between 1 and 100!")
    async def guess(self, interaction: discord.Interaction, number: int):
        """Handles the user's guess."""
        user = interaction.user

        if user.id not in self.games:
            await interaction.response.send_message("You don't have an ongoing game. Start a new game using `/guessnumber`.")
            return

        game = self.games[user.id]
        target_number = game["number"]
        game["attempts"] += 1

        if number < target_number:
            await interaction.response.send_message("Your guess is too low! Try again.")
        elif number > target_number:
            await interaction.response.send_message("Your guess is too high! Try again.")
        else:
            attempts = game["attempts"]
            await interaction.response.send_message(f"🎉 Congratulations! You guessed the correct number {target_number} in {attempts} attempts!")
            del self.games[user.id]

    @discord.app_commands.command(name="dadjoke", description="Get a random dad joke!")
    async def dadjoke(self, interaction: discord.Interaction):
        """Returns a random dad joke."""
        jokes = [
            "Why don't skeletons fight each other? They don't have the guts.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don’t eggs tell jokes? They’d crack each other up.",
            "I only know 25 letters of the alphabet. I don’t know y.",
            "I used to play piano by ear, but now I use my hands.",
            "I’m reading a book on anti-gravity. It’s impossible to put down.",
            "Why can’t you hear a pterodactyl go to the bathroom? Because the ‘P’ is silent.",
            "I don’t trust stairs because they’re always up to something.",
            "What do you call fake spaghetti? An impasta."
        ]

        joke = random.choice(jokes)

        await interaction.response.send_message(joke)
        
    @discord.app_commands.command(name="dicegame", description="Roll a dice or multiple dice!")
    async def dicegame(self, interaction: discord.Interaction, dice: str):
        """Rolls the specified dice (e.g., 1d6, 2d20, etc.)."""
        
        if 'd' not in dice:
            await interaction.response.send_message("Invalid format. Please use the format NdX, where N is the number of dice and X is the type (e.g., 1d6).")
            return
        
        try:
            num_dice, dice_sides = dice.lower().split('d')
            num_dice = int(num_dice)  
            dice_sides = int(dice_sides)  

            if num_dice <= 0 or dice_sides <= 0:
                raise ValueError

        except ValueError:
            await interaction.response.send_message("Invalid format. Please use the format NdX (e.g., 2d6), where N is the number of dice and X is the type (e.g., 6 sides).")
            return

        rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
        total = sum(rolls)

        roll_results = ', '.join(str(roll) for roll in rolls)
        embed = discord.Embed(title=f"{interaction.user.name}'s Dice Roll", color=discord.Color.green())
        embed.add_field(name="Dice Rolled", value=f"{dice}", inline=False)
        embed.add_field(name="Results", value=roll_results, inline=False)
        embed.add_field(name="Total", value=str(total), inline=False)

        await interaction.response.send_message(embed=embed)
        
    @discord.app_commands.command(name="affirmation", description="Receive a positive affirmation!")
    async def affirmation(self, interaction: discord.Interaction):
        """Sends a positive affirmation to the user."""

        affirmations = [
            "You are amazing, just the way you are!",
            "Believe in yourself. You are capable of great things!",
            "You are enough, just as you are.",
            "Every day is a new opportunity to shine.",
            "You are worthy of all the good things that come your way.",
            "Keep going, you're doing great!",
            "Your potential is limitless. Keep reaching for the stars!",
            "You have the strength to overcome anything.",
            "Don't be afraid to stand out. You are unique and special.",
            "You are deserving of love and happiness."
        ]
        
        affirmation = random.choice(affirmations)

        await interaction.response.send_message(affirmation)
        
    @discord.app_commands.command(name="fakenews", description="Get a random fake news headline!")
    async def fakenews(self, interaction: discord.Interaction):
        """Generates a random fake news headline."""
        
        fake_news = [
            "Breaking: Scientists Discover That Pizza Is Actually Good for You!",
            "Local Man Discovers He Has Superpowers After Eating Spicy Nachos.",
            "New Study Shows That Sleeping 12 Hours a Day Boosts Productivity.",
            "Breaking: Aliens Land on Earth, Demand Free Wi-Fi and Avocado Toast.",
            "World's Largest Ice Cream Cone Discovered in Antarctica.",
            "Scientists Announce That Cats Are Secretly Running the World.",
            "Sharks Now Capable of Playing Chess, Challenging Humans to a Tournament.",
            "Experts Say the Moon Is Actually Just a Giant Light Bulb.",
            "Billionaire Announces Plans to Build a Rollercoaster to Mars.",
            "Breaking: Earth to Be Replaced by Giant Ball of Cheese for the Next Millennium."
        ]

        headline = random.choice(fake_news)

        await interaction.response.send_message(f"📰 **Fake News**: {headline}")

    @discord.app_commands.command(name="mindread", description="Let me read your mind!")
    async def mindread(self, interaction: discord.Interaction):
        """Pretends to read the user's mind and gives a random humorous response."""

        mind_readings = [
            "I see... you're thinking about pizza right now, aren't you?",
            "Hmm... I sense you're wondering what to have for lunch today.",
            "I can feel your mind... you're definitely thinking about your next vacation!",
            "You're thinking about that one embarrassing moment from years ago, aren't you?",
            "I know what you're thinking... 'Is it time for a snack yet?'",
            "Your mind is whispering... 'I hope the bot says something funny.'",
            "I sense... you're secretly planning to take a nap right now.",
            "You're probably wondering why you opened this command. Well, now you know!",
            "You are wondering if the bot can actually read minds, aren't you?",
            "You're thinking about the weather... but also wondering how to ask about it."
        ]

        response = random.choice(mind_readings)

        await interaction.response.send_message(f"🧠 **Mind Reader:** {response}")

    @discord.app_commands.command(name="love", description="Send a positive and loving message!")
    async def love(self, interaction: discord.Interaction):
        """Sends a random loving message to the user."""

        love_messages = [
            "You are loved more than you know!",
            "Sending you all the love and positive vibes today! 💖",
            "You bring so much light into the world, don't forget that! ✨",
            "The world is better with you in it! Keep shining. 🌟",
            "Your kindness and heart make the world a better place. ❤️",
            "You are worthy of all the love in the universe! 💫",
            "Here's a reminder: You are amazing, and you are loved! 🥰",
            "Sending you hugs, love, and all things positive! 🤗💖",
            "You are cherished, valued, and appreciated more than you realize! 💖",
            "Remember, you are a star, and the world is lucky to have you. 🌠"
        ]

        message = random.choice(love_messages)

        await interaction.response.send_message(f"💖 **Love Message:** {message}")

    @discord.app_commands.command(name="shortstory", description="Receive a random short story!")
    async def shortstory(self, interaction: discord.Interaction):
        """Sends a random short story to the user."""

        short_stories = [
            "Once upon a time, in a faraway kingdom, there was a small dragon who didn't know how to fly. Every day, he tried and tried, but no matter how hard he flapped his wings, he couldn’t take off. One day, he met a wise owl who told him, 'Flying is not about strength, it's about belief in yourself.' The little dragon believed in himself, flapped his wings with all his might, and soared into the sky, realizing that with belief, anything is possible.",
            "A young girl named Lily lived by the sea. Every morning, she would walk along the beach and collect seashells. One day, she found a golden shell that shimmered in the sunlight. As she picked it up, the sea whispered, 'This is a special shell. It will grant one wish.' Lily thought for a moment and wished for a world full of kindness. From that day forward, she spread kindness wherever she went, and soon, the world became a much brighter place.",
            "In a bustling town, there was a little bakery that made the most delicious cupcakes. The baker, an elderly man named Mr. Jolly, was always smiling and sharing his cupcakes with everyone. One day, a young boy asked him, 'Mr. Jolly, how do you make the cupcakes taste so good?' Mr. Jolly replied, 'It's not just the ingredients, my boy. It's the love I put into every cupcake.' The boy smiled, understanding that it’s the small things that make the world so sweet.",
            "There once lived a curious kitten named Oliver who loved exploring. One day, he wandered into a forest and found a mysterious glowing stone. As he touched it, the stone began to speak, 'You have a kind heart, young kitten. You will find treasures not in gold, but in kindness.' Oliver returned home, and every time he helped someone, he found small treasures in his heart, realizing that kindness was the greatest treasure of all.",
            "The stars shone brightly one night as a small boy named Leo lay on the grass, gazing at the sky. 'I wonder what it's like up there among the stars,' he thought. A gentle voice whispered from the wind, 'The stars are always watching over you, Leo. Every wish you make is a star in the making.' Leo smiled, closed his eyes, and made a wish. That night, the stars shined just a little brighter, as if they were fulfilling his dreams."
        ]

        story = random.choice(short_stories)

        await interaction.response.send_message(f"📖 **Short Story:**\n\n{story}")
        
    def display_word(self, word, guessed_letters):
        """Replaces unguessed letters with underscores."""
        return " ".join([letter if letter in guessed_letters else "_" for letter in word])

    @discord.app_commands.command(name="hangman", description="Start a game of Hangman!")
    async def hangman(self, interaction: discord.Interaction):
        """Starts a Hangman game for the user."""

        if interaction.user.id in self.games:
            await interaction.response.send_message("You're already playing a game!", ephemeral=True)
            return

        word = random.choice(WORDS).lower()
        guessed_letters = set()
        attempts = 6
        self.games[interaction.user.id] = {"word": word, "attempts": attempts, "guessed": guessed_letters}

        await interaction.response.send_message(f"🎮 **Hangman Game Started!**\n\nWord: `{self.display_word(word, guessed_letters)}`\nAttempts left: `{attempts}`\n\nGuess a letter by typing it in the chat!")

        game_active = True

        def check(m):
            return m.author == interaction.user and len(m.content) == 1 and m.content.isalpha()

        while game_active and attempts > 0:
            try:
                guess_msg = await self.bot.wait_for("message", check=check, timeout=30)
                guess = guess_msg.content.lower()

                if guess in guessed_letters:
                    await interaction.followup.send("❗ You already guessed that letter!", ephemeral=True)
                    continue

                guessed_letters.add(guess)

                if guess not in word:
                    attempts -= 1
                    await interaction.followup.send(f"❌ Wrong guess! `{guess}` is not in the word.\nAttempts left: `{attempts}`")
                else:
                    await interaction.followup.send(f"✅ Good guess! `{guess}` is in the word!")

                current_display = self.display_word(word, guessed_letters)
                await interaction.followup.send(f"Word: `{current_display}`")

                if "_" not in current_display:
                    await interaction.followup.send(f"🎉 **Congratulations {interaction.user.mention}, you guessed the word!**")
                    game_active = False

            except asyncio.TimeoutError:
                await interaction.followup.send("⌛ **Game Over!** You took too long to respond.")
                game_active = False

        if attempts == 0:
            await interaction.followup.send(f"💀 **Game Over!** The word was `{word}`.")

        del self.games[interaction.user.id]

async def setup(bot: commands.Bot):
        
 @bot.event
 async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
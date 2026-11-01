import discord
from discord.ext import commands, tasks
import datetime
import random

# Define required bot intents
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to read message content

# Initialize the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration settings
CHANNEL_ID = 123456789012345678  # Target Discord channel ID
ROLE_ID = 123456789012345678     # Role ID to ping when asking a question
INACTIVITY_MINUTES = 60          # Time threshold in minutes before triggering a prompt

# List of engagement questions
QUESTIONS = [
    "What’s a total unpopular opinion you have about a well-known game, movie, or franchise?",
    "If you could only play a single video game for the rest of your life, which one survives the longest?",
    "Which video game emotionally wrecked you the most or totally disappointed you in the end?",
    "What is the most annoying cliché in modern games or shows that immediately pulls you out?",
    "What feature from old games or consoles do you miss the most in modern gaming?",
    "Which YouTuber, streamer, or influencer that everyone hypes up gets completely on your nerves?",
    "Which game has an absolute masterpiece story, but gameplay so trashy that it's hard to play?",
    "Which video game has the most toxic community you've ever experienced?",
    "What is the worst update or patch that completely ruined a game you loved?",
    "Which board or card game has almost caused an all-out crisis in your friend group?",
    "Which real-life animal would instantly become terrifying and dangerous if it could suddenly speak human language?",
    "If you could choose any fictional game or movie universe to grow up in, where are you moving?",
    "If you were invisible for 24 hours, what is the very first thing you would do?",
    "If you had a superpower that is completely useless or embarrassing in everyday life, what would it be?",
    "If you could swap bodies with a famous person (dead or alive) for one day, who would it be?",
    "If you had to choose between constant, endless freezing or a permanent heatwave, what are you picking?",
    "If you could invent something that instantly revolutionizes your daily routine, what would it do?",
    "If you were stranded on a desert island and could only take three items (no electronics), what are they?",
    "Which fictional character would be the absolute worst neighbor to have in real life?",
    "If you could tell your younger self from 5 years ago exactly one sentence, what would it be?",
    "What was the most absurd excuse you've ever used to get out of going somewhere?",
    "If you could instantly delete one thing from modern internet culture and social media, what would it be?",
    "What is the absolute nastiest food combo you secretly love eating even though everyone thinks it's gross?",
    "What was the most embarrassing situation you've ever gotten into due to a technical glitch (e.g., open mic)?",
    "Which music or movie classic do you think is completely overrated?",
    "If you had to live in a different decade (e.g., 80s, 90s) starting tomorrow forever, which one do you pick?",
    "What is one thing feel-good everyone on earth can do that you just can't get the hang of?",
    "What is the best fast-food meal you can possibly grab anywhere at 3 AM?",
    "What was your weirdest, funniest, or most embarrassing memory from school?",
    "Which app on your smartphone steals the most of your time even though you secretly hate it?",
    "Which video game has the absolute best soundtrack of all time in your opinion?",
    "What is the best quote or most memorable line from a movie that you use way too often in daily life?",
    "Which book that you were forced to read in school did you secretly think was actually great (or absolute torture)?",
    "What is the most useless school subject you ever had to learn and never needed again?",
    "What is your absolute secret 'guilty pleasure' you'd never admit to in chat?",
    "What is by far the worst movie you've ever sat through all the way to the end?",
    "Which internet trend from recent years do you think was the biggest and dumbest nonsense?",
    "What is the best feeling in the world after an extremely hard, exhausting day?",
    "Which game or movie franchise should have just stopped after Part 1?",
    "Which historical event would you have loved to watch for an hour from a safe distance?",
    "If you could change one thing about yourself instantly with a snap of your fingers, what would it be?",
    "What is the most expensive or utterly useless gadget you've ever wasted your money on?",
    "Who in this server do you think would die first in a zombie apocalypse?",
    "What is the most annoying sound in the world that instantly drives you up the wall?",
    "If you could only use a single spice or sauce for the rest of your life, which one?",
    "What was the most outrageous bargain or best deal you've ever pulled off?",
    "Which real-life law or rule would you abolish immediately if you could?",
    "What is the weirdest hobby you've ever heard of that someone actually practices?",
    "If you could level up any skill in life instantly to absolute maximum, which one do you pick?",
    "What drives you up the wall in daily life even though it's totally trivial?"
]

# History buffer to track the last 5 asked questions and prevent duplicates
recent_questions = []

# Event: Executed once when the bot successfully logs in and connects to Discord
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    # Start the background task loop if it is not already running
    if not check_inactivity.is_running():
        check_inactivity.start()

# Background Task: Runs automatically every 300 seconds (5 minutes)
@tasks.loop(seconds=300)
async def check_inactivity():
    global recent_questions
    
    # Fetch the target channel object using the specified ID
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Could not find channel with ID {CHANNEL_ID}!")
        return

    # Retrieve the latest 10 messages from the channel history
    messages = [msg async for msg in channel.history(limit=10)]
    if not messages:
        return

    # Grab the single most recent message
    last_message = messages[0]

    # Prevent response loops if the bot itself sent the last message
    if last_message.author == bot.user:
        return

    # Calculate time difference between current UTC time and the last message timestamp
    now = datetime.datetime.now(datetime.timezone.utc)
    time_diff = now - last_message.created_at

    print(f"Last message was sent {time_diff.total_seconds():.1f} seconds ago.")

    # Check if the inactivity duration (in seconds) exceeds the configured limit
    if time_diff.total_seconds() > (INACTIVITY_MINUTES * 60):
        # Filter out questions that were asked recently
        available_questions = [q for q in QUESTIONS if q not in recent_questions]
        
        # Fallback to the full question list if all questions are currently filtered
        if not available_questions:
            available_questions = QUESTIONS

        # Select a random question from the available list
        question = random.choice(available_questions)

        # Append the new question to the recent history buffer
        recent_questions.append(question)
        
        # Keep only the last 5 entries in the history buffer
        if len(recent_questions) > 5:
            recent_questions.pop(0)

        # Send the question to the Discord channel along with the role mention
        await channel.send(f"<@&{ROLE_ID}> 💬 **Question:** {question}")

# Start the bot execution
bot.run("YOUR_DISCORD_BOT_TOKEN_HERE")

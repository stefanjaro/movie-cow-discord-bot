# bot.py
import os
import random
import math
import discord
from discord.ext import commands
from dotenv import load_dotenv
from omdb_movie_search import get_movie_details, search_for_movie
from omdb_movie_search import compile_movie_details_response_to_string, compile_movie_search_response_to_string

# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHARACTER_LIMIT = 2000

bot = commands.Bot(command_prefix='moo')

def split_long_response(response):
    """
    For messages longer than 2000 characters, split them by section first
    and then by characters next if some of the sections are still too long
    """
    # split by section
    response_split = response.split("\n\n")

    # for storing the verified response sections
    verified_response_split = []

    for response_section in response_split:
        # if each response section is less than the character limit, append to verified response split
        if len(response_section) < CHARACTER_LIMIT:
            verified_response_split.append(response_section)
        
        # if it's more, break the response sections that are longer than 2000 chars
        else:
            # figure out how many times we need to split it to get each part below 2000 and then split it by splicing
            times_to_split = math.ceil(len(response_section) / CHARACTER_LIMIT)
            split_response_section = [response_section[x * CHARACTER_LIMIT : (x+1) * CHARACTER_LIMIT].strip() for x in range(times_to_split)]

            # the spoiler tags won't work when they're split so replace the double pipes and click to reveal in case they're in any of them
            split_response_section = [x.replace("||", "").strip() for x in split_response_section]
            split_response_section = [x.replace("(Click to Reveal)", "").strip() for x in split_response_section]

            # store the entire split section
            verified_response_split.extend(split_response_section)

    return verified_response_split

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} has connected to Discord!\n'
        f'Guild Details: {guild.name} (id: {guild.id})'
    )

@bot.command(name="name", help='Returns movie information given a movie name. Type mooname <movie name>')
async def movie_details_with_name(ctx, *args): 
    # form search string
    search_string = " ".join(args)
    
    # get api response
    api_response = get_movie_details(movie_title=search_string).json()

    # if there's an api response, parse through it
    if api_response:
        # if we haven't resceived a response return an error
        if api_response["Response"] == "False":
            response = api_response["Error"]
        else:
            response = compile_movie_details_response_to_string(api_response)
    else:
        response = "Contact the Developer. Tell him the API is having issues."
  
    # make sure the length of the response is less than discord's character limit
    if len(response) < CHARACTER_LIMIT:
        await ctx.send(response)

    # if it's greater split the response and reply in chunks
    else:
        # split and verify lengths of sections
        verified_response_split = split_long_response(response)

        # reply in chunks
        for verified_response_section in verified_response_split:
            await ctx.send(verified_response_section)

@bot.command(name="id", help='Returns movie information given an IMDb ID. Type mooname <IMDb ID>')
async def movie_details_with_id(ctx, *args): 
    # form search string
    search_string = " ".join(args)
    
    # get api response
    api_response = get_movie_details(movie_id=search_string).json()

    # if there's an api response, parse through it
    if api_response:
        # if we haven't resceived a response return an error
        if api_response["Response"] == "False":
            response = api_response["Error"]
        else:
            response = compile_movie_details_response_to_string(api_response)
    else:
        response = "Contact the Developer. Tell him the API is having issues."

    # make sure the length of the response is less than discord's character limit
    if len(response) < CHARACTER_LIMIT:
        await ctx.send(response)

    # if it's greater split the response and reply in chunks
    else:
        # split and verify lengths of sections
        verified_response_split = split_long_response(response)

        # reply in chunks
        for verified_response_section in verified_response_split:
            await ctx.send(verified_response_section)

@bot.command(name="search", help='Returns a list of movies given a movie name. Type moosearch <movie name>')
async def movie_search(ctx, *args):
    # form search string
    search_string = " ".join(args)

    # get api response
    api_response = search_for_movie(search_string=search_string).json()

    # if there's an api response, parse through it
    if api_response:
        # if we haven't resceived a response return an error
        if api_response["Response"] == "False":
            response = api_response["Error"]
        else:
            response = compile_movie_search_response_to_string(api_response)
    else:
        response = "Contact the Developer. Tell him the API is having issues."

    await ctx.send(response)

@bot.command(name="joke", help='See for yourself.')
async def easter_egg(ctx):
    """
    Returns a bad joke (easter egg function)
    """
    # list of bad jokes
    bad_jokes = [
        "What is the Sri Lankan version of the Taj Mahal?\n||Swarna Mahal||",
        "What did one Sri Lankan say to the other?\n||I have no idea; I don't speak Sinhala. I'm from an International school.||",
        "What did the farmer say after he lost his tractor?\n||Aiyo, if only the other party was in power!||",
        "A priest, a monk, and a rabbit walk into a blood bank.\nThe rabbit says 'I think I'm a type O.",
        "What's the difference between a woman and a cutting board?\n||A woman is a biological being and a cutting board is an inanimate object.||",
        "Chuck Norris walks into a bar and is treated with respect becaue of he's an acclaimed actor.",
        "What do you call an Asian that flies an aeroplane?\n||A pilot||",
        "Why didn't Sally want to clap her hands?\n||Because she's an independent person and can make her own decisions without needing to provide a reason.||",
        "A horse walks into a bar.\nEverybody is alarmed and leaves. The bartender tries to shoo it away.",
        "What did batman say to robin when they got to the Batmobile?\n||Get in the car||",
        "What's blue in Sri Lanka and smells like red paint?\n||Blue paint in Sri Lanka||"
    ]
    
    # choose a bad joke at random
    response = random.choice(bad_jokes)
    await ctx.send(response)

bot.run(TOKEN)
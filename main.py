import json
import discord
from discord.app import Option
from discord.ext import commands
import wikipediaapi
from youtubesearchpython import VideosSearch
from PyDictionary import PyDictionary
from translate import Translator
import requests
import aiohttp
import asyncio
from config import Config
from databases import Database
import random
import datetime
import uuid


config = Config()
bot = discord.Bot(intents= discord.Intents.all())
database = Database()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif 'spam' not in message.channel.name:
        database.add_experience(message.author.id, 5)
        levelup = database.level_up(message.author.id)
        if levelup:
            await message.channel.send(f"Congratulations {message.author.mention}! You've leveled up!")#bot.send_message(message.channel, f"Congratulations {message.author.mention}! You've leveled up to level " + str(levelup) + "!")

@bot.command(name='ping', guild_ids=[862785948605612052])
async def global_command(ctx):
    await ctx.respond(f"Pong! latency: {round(bot.latency*1000)}ms")

BotCommands = {
    "Fun": 
        {
            "flip": "Flips a coin",
            "dice": "Flips a dice",
            "diceroll <amt: optional>": "Rolls a dice with a certain amount of sides",
            "hug <user>": "Gives a user a hug",
            "slap <user>": "Slaps a user",
            "kiss <user>": "Kisses a user",
            "pat <user>": "Pats a user",
            "advice (Not Working)": "Gives a Random Advice",
            "bored": "Suggests An Activity to do",
            "joke (Server Under maintenance)": "Sends a Random Joke",
            "wikisearch <query>": "Searches your query on wikipedia and gives you the result",
            "youtubesearch <query>": "Searches your query on youtube and gives you the result",
            "shortlink": "Shortens a link",
            "rps": "Play Rock Paper Scissors with the bot",
            "meme": "Sends a random meme",
            "dog": "Sends a random dog image"
        },
    "Economy":
        {
            "balance <user: optional>": "Shows you your balance",
            "give <user>": "Gives a user a certain amount of money from your wallet",
            "withdraw": "Withdraws money from your Bank", 
            "deposit": "Deposits money into your Bank",
            "daily": "Gives you a daily reward",
            "richest": "Shows you the richest users",
        },
    "Leveling": 
        {
            "level": "Shows you your level",
            "leaderboard": "Shows you the top 10 users with highest levels",
        },
    "Moderation":
        {
            "kick": "Kick a Member",
            "ban": "Bans A Member",
            "purge <amt>": "Deletes amt amount of messages",        
            "mute": "Mutes a Member",
            "unmute": "Unmutes a Member"
        },
    "Tags":
        {
            "add_tag": "Adds a tag",
            "tag_search": "Searches for a tag",
            "user_tags": "Shows you all the tags of a user",
            "tag_by_id": "Searches for a tag by id",
        }
}

@bot.command(guild_ids=[862785948605612052])
async def help(ctx, category: Option(str, "Choose Category", choices=["Fun", "Economy", "Leveling", "Moderation", "Tags"], required=False, default=None)):
    if category == None:
        embed = discord.Embed(title="Help", description="Here is a list of Categories", color=discord.Color.blue())
        for section in BotCommands:
            embed.add_field(name=section, value=f"/help category:{section}", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Help", description=f"Here is a list of Commands Under {category} category:", color=discord.Color.blue())
        for section in BotCommands[category]:
            embed.add_field(name=section, value=BotCommands[category][section], inline=False)
        await ctx.send(embed=embed)

#----------------------------------------------Moderation----------------------------------------------
@bot.command(guild_ids=[862785948605612052])
@commands.has_permissions(kick_members=True)
async def kick(ctx,
               name: Option(discord.Member, "Name Of the Member"), *,
               reason: Option(str, "Reason for kick", required=False, default="No Reason Provided")):
    await name.kick(reason=reason)
    embed = discord.Embed(
        title="Member Kicked", description=f"{name.mention} Kicked for reason {reason}", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
@commands.has_permissions(ban_members=True)
async def ban(ctx,
              name: Option(discord.Member, "Name Of the Member"), *,
              reason: Option(str, "Reason for Ban", required=False, default="No Reason Provided")):
    await name.ban(reason=reason)
    embed = discord.Embed(
        title="Member Banned", description=f"{name.mention} Banned for reason {reason}", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
@commands.has_permissions(manage_messages=True)
async def purge(ctx,
                limit: Option(int, "Amount of messages to purge", required=False, default=2)):
    await ctx.channel.purge(limit=limit)


#--------------------------------------------Fun----------------------------------------------------
@bot.command(guild_ids=[862785948605612052])
async def yomomma(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://yomomma-api.herokuapp.com/jokes") as answer:
            answer = await answer.json()
            embed = discord.Embed(
                title=f"Yo Momma", description=answer['joke'], color=discord.Color.blue())
            embed.set_footer(text=f"Asked By {ctx.author}")
            await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def bored(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.boredapi.com/api/activity") as answer:
            answer = await answer.json()
            embed = discord.Embed(title=f"{answer['activity']}", color=discord.Color.blue())
            embed.add_field(name="Type", value=f"{answer['type']}", inline=False)
            embed.add_field(name="Participants",
                            value=f"{answer['participants']}", inline=False)
            embed.add_field(name="Price", value=f"{answer['price']}", inline=False)
            embed.set_footer(text=f"Asked By {ctx.author}")
            await ctx.send(embed=embed)

# @bot.command(guild_ids=[862785948605612052])
# async def joke(ctx):
#     async with aiohttp.ClientSession() as session:
#         async with session.get("https://official-joke-api.appspot.com/jokes/general/random") as answer:
#     # answer = requests.get(
#     #     "https://official-joke-api.appspot.com/jokes/general/random")
#             answer = await answer.json()
#             embed = discord.Embed(title=f"Joke ID {answer[0]['id']}", color=discord.Color.blue())
#             embed.add_field(name="Setup: ", value=answer[0]['setup'])
#             embed.add_field(name="Punchline: ", value=answer[0]['punchline'])
#             embed.set_footer(text=f"Asked By {ctx.author}")
#             await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def wikisearch(ctx, *, word):
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(word)
    pages = page.summary
    embed = discord.Embed(title=word, description=pages, color=discord.Color.blue())
    embed.set_footer(text=f"Source: {page.fullurl}")
    await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def youtubesearch(ctx, *, word):
    embed = discord.Embed(title=f"YouTube Search For {word}", color=discord.Color.blue())
    videosSearch = VideosSearch(word, limit=5)
    res = videosSearch.result()
    for i in res['result']:
        description = ""
        description += f"Channel: {i['channel']['name']}, \n"
        description += f"Views: {i['viewCount']['short']}, \n"
        description += f"Link: [Click Here]({i['link']}) \n"
        embed.add_field(
            name=f"Title: {i['title']}", value=description, inline=False)
    embed.set_footer(text=f"Asked by {ctx.author}")
    await ctx.send(embed=embed)

async def shorten(uri):
    query_params = {
        'access_token': config.BITTLY_ACCESS_TOKEN,
        'longUrl': uri
    }
    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, params=query_params) as response:
            data = await response.json()
            return data['data']['url']

@bot.command(guild_ids=[862785948605612052])
async def shortlink(ctx, link):
    try:
        shortened_link = await shorten(link)
        embed = discord.Embed(title="Link Generated With Bit.ly", color=discord.Color.blue())
        embed.add_field(name="Orignal Link:", value=link, inline=False)
        embed.add_field(name="Shortened Link:",
                        value=shortened_link,
                        inline=False)
        embed.set_footer(
            text=f"Powered By Bit.ly | Requested by {ctx.author}")
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.send("Invalid link")
   
@bot.command(guild_ids=[862785948605612052])
async def hug(ctx, *, name: Option(discord.Member, "Name Of the Member")):
    if name is None:
        await ctx.send(f"{ctx.author.mention} You need to mention someone to hug them")
    else:
        embed = discord.Embed(title=f"{ctx.author.name} hugged {name.name}! Awww!", color=discord.Color.blue())
        gif = await database.get_Randon_GIF("hug")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
        
@bot.command(guild_ids=[862785948605612052])
async def kiss(ctx, *, name: Option(discord.Member, "Name Of the Member")):
    if name is None:
        await ctx.send(f"{ctx.author.mention} You need to mention someone to kiss them")
    else:
        embed = discord.Embed(title=f"{ctx.author.name} Kissed {name.name}! Awww!", color=discord.Color.blue())
        # gif = await database.get_Randon_GIF("kiss")
        # embed.set_image(url=gif)
        await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def slap(ctx, *, name: Option(discord.Member, "Name Of the Member")):
    if name is None: 
        await ctx.send(f"{ctx.author.mention} You need to mention someone to slap them")       
    else:
        embed = discord.Embed(title=f"{ctx.author.name} Slapped {name.name}! Ouch!", color=discord.Color.blue())
        gif = await database.get_Randon_GIF("slap")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def pat(ctx, *, name: Option(discord.Member, "Name Of the Member")):  
    if name is None:
        await ctx.send(f"{ctx.author.mention} You need to mention someone to pat them")
    else:
        embed = discord.Embed(title=f"{ctx.author.name} Patted {name.name}! Good Job!", color=discord.Color.blue())
        gif = await database.get_Randon_GIF("pat")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def rps(ctx, choice: Option(str, "Pick One", choices=["rock", "paper", "scissors"])):
    bot_choice = random.choice(["rock", "paper", "scissors"])
    if choice is None:
        await ctx.send(f"{ctx.author.mention} You need to pick a choice")
    elif choice.lower() == bot_choice:
        await ctx.send(f"{ctx.author.mention} You both picked {choice}! It's a tie!")
    elif choice.lower() == "rock" and bot_choice == "paper":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. I win!")
    elif choice.lower() == "rock" and bot_choice == "scissors":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. You win!")
    elif choice.lower() == "paper" and bot_choice == "rock":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. You win!")
    elif choice.lower() == "paper" and bot_choice == "scissors":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. I win!")
    elif choice.lower() == "scissors" and bot_choice == "rock":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. I win!")
    elif choice.lower() == "scissors" and bot_choice == "paper":
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. You win!")
    else:
        await ctx.send(f"{ctx.author.mention} You picked {choice} and the bot picked {bot_choice}. I win!")

@bot.command(guild_ids=[862785948605612052])
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.herokuapp.com/gimme") as meme:
            meme = await meme.json()
            embed = discord.Embed(title=meme['title'], color=discord.Color.blue(), url=meme['postLink'])
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f"Posted By {meme['author']}")
            await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://dog.ceo/api/breeds/image/random") as dog:
            dog = await dog.json()
            embed = discord.Embed(title="Dog", color=discord.Color.blue(), url=dog['message'])
            embed.set_image(url=dog['message'])
            embed.set_footer(text=f"Posted By {dog['status']}")
            await ctx.send(embed=embed)
            
@bot.command(guild_ids=[862785948605612052])
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as cat:
            cat = await cat.json()
            embed = discord.Embed(title="Cat", color=discord.Color.blue(), url=cat[0]['url'])
            embed.set_image(url=cat[0]['url'])
            await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def flip(ctx):
    random.choice(["Heads", "Tails"])
    if random.choice(["Heads", "Tails"]) == "Heads":
        await ctx.send(f"<:heads:887180976264982588>")
    else:
        await ctx.send(f"<:tails:887180976407588894>")

@bot.command(guild_ids=[862785948605612052])
async def roll(ctx, number: int=6):
    random.randint(1, number)
    await ctx.send(f"{ctx.author.mention} You rolled a {random.randint(1, number)}")        

#---------------------------------------Banking---------------------------------------#
@bot.command(guild_ids=[862785948605612052])
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    bank = database.check_account(user.id)
    embed = discord.Embed(title=f"{user}'s Bank Account", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Wallet", value=f"{bank['wallet']}", inline=False)
    embed.add_field(name="Bank", value=f"{bank['bank']}", inline=False)
    await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def withdraw(ctx, amount: int):
    bank = database.check_account(ctx.author.id)
    if amount > bank['bank']:
        await ctx.send("You don't have enough N8Coins in your bank")
    elif amount <= 0:
        await ctx.send("You can't withdraw 0 or less N8Coins")
    else:
        database.remove_from_bank(ctx.author.id, amount)
        database.add_in_wallet(ctx.author.id, amount)
        await ctx.send(f"You have withdrawn {amount} N8Coins from your bank")
        
@bot.command(guild_ids=[862785948605612052])
async def deposit(ctx, amount: int):
    bank = database.check_account(ctx.author.id)
    if amount > bank['wallet']:
        await ctx.send("You don't have enough N8Coins in your wallet")
    elif amount <= 0:
        await ctx.send("You can't deposit 0 or less N8Coins")
    else:
        database.remove_from_wallet(ctx.author.id, amount)
        database.add_in_bank(ctx.author.id, amount)
        await ctx.send(f"You have deposited {amount} N8Coins to your bank")
        
@bot.command(guild_ids=[862785948605612052])
async def give(ctx, user: discord.Member, amount: int):
    bank = database.check_account(ctx.author.id)
    if amount > bank['bank']:
        await ctx.send("You don't have enough N8Coins in your bank")
    elif amount <= 0:
        await ctx.send("You can't give 0 or less N8Coins")
    else:
        database.add_in_bank(user.id, amount)
        database.remove_from_bank(ctx.author.id, amount)
        await ctx.send(f"You have given {amount} N8Coins to {user.name}")

@bot.command(guild_ids=[862785948605612052])
async def richest(ctx):
    rankings = database.get_Top_Ten_Richest()
    embed = discord.Embed(title="Top 10 Richest Members Of N8Dev's Lounge", color=discord.Color.blue())
    for i in rankings:
        try:
            print(i['_id'])
            embed.add_field(name=f"{bot.get_user(int(i['_id'])).name}", value=f"Bank: {i['bank']}\n Wallet: {i['wallet']}", inline=False)
        except:
            pass
    embed.set_footer(text=f"Rankings Are based on the amount of N8Coins in your Bank")
    await ctx.send(embed=embed)


#---------------------------------------Leveling---------------------------------------#
@bot.command(guild_ids=[862785948605612052])
async def level(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    info = database.get_leveling_info(user.id)
    exp = info['experience']
    lvl=0
    while True:
        if exp < ((50*(lvl**2))+(50*lvl)):
            break
        lvl += 1
    xp = exp-((50*((lvl-1)**2))+(50*(lvl-1))) 
    boxes = int((xp/(200*((1/2)*lvl)))*20)
    rank = database.get_rank(user.id, exp)
    embed = discord.Embed(title=f"{user}'s Leveling Info", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Level", value=f"{lvl}", inline=True)
    embed.add_field(name="Experience", value=f"{exp}", inline=True)
    embed.add_field(name="Rank", value=f"{rank}", inline=True)
    embed.add_field(name="Progress", value=boxes*"<:blue:886866137881673729>"+(20-boxes)*"<:white:886866138062028820>", inline=False)
    await ctx.send(embed=embed)

@bot.command(guild_ids=[862785948605612052])
async def leaderboard(ctx):
    rankings = database.get_Top_Ten_Leveling()
    embed = discord.Embed(title="Top 10 Leveling Rankings", color=discord.Color.blue())
    for i in rankings:
        try:
            print(i['_id'])
            embed.add_field(name=f"{bot.get_user(int(i['_id'])).name}", value=f"Level: {i['level']}\n Experience: {i['experience']}", inline=False)
        except:
            pass
    await ctx.send(embed=embed)
    
#---------------------------------------------tag-------------------------------------------
@bot.command(guild_ids=[862785948605612052])
async def add_tag(ctx, name:str,*, content: str):
    if content == "" or name == "":
        await ctx.send("You need to enter a tag/content")
    elif len(name) > 20:
        await ctx.send("Your tag is too long")
    elif len(content) > 500:
        await ctx.send("Your content is too long")
    else:
        time = datetime.datetime.now()
        data = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "content": content,
            "author": ctx.author.id,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if database.tag_Exist(name):
            await ctx.send(f"Tag {name} already exists")
        else:
            database.add_Tag(data)
            await ctx.send(f"Your tag has been created")
            
@bot.command(guild_ids=[862785948605612052])
async def tag_search(ctx, name:str):
    tags = database.get_Tag_by_name(name)
    if tags is not None:
        embed = discord.Embed(title=f"Tag: {name}", color=discord.Color.blue())
        for i in tags:
            embed.add_field(name=f"{i['name']}", value=f"**ID:** `{i['_id']}` \n**Content:** {i['content']}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Tag {name} does not exist")
        
@bot.command(guild_ids=[862785948605612052])
async def user_tags(ctx, user:discord.Member):
    tags = database.get_Tag_by_Author_ID(user.id)
    embed = discord.Embed(title=f"{user.name}'s Tags", color=discord.Color.blue())
    for i in tags:
        embed.add_field(name=f"{i['name']}", value=f"**ID:** `{i['_id']}` \n**Content:** {i['content']}", inline=False)
    await ctx.send(embed=embed)
    
@bot.command(guild_ids=[862785948605612052])
async def tag_by_id(ctx, id:str):
    tag = database.get_Tag_by_ID(id)
    if tag is not None:
        embed = discord.Embed(title=f"{tag['name']}", color=discord.Color.blue())
        embed.add_field(name="ID", value=f"{tag['_id']}", inline=False)
        embed.add_field(name="Author", value=f"{bot.get_user(int(tag['author'])).name}", inline=False)
        embed.add_field(name="Content", value=f"{tag['content']}", inline=False)
        embed.add_field(name="Created On", value=f"{tag['time']}", inline=False)
        embed.add_field(name="Updated On", value=f"{tag['updated']}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Tag {id} does not exist")

bot.run(config.TOKEN)
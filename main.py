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


config = Config()
bot = discord.Bot()
database = Database()


@bot.command(name='ping', guild_ids=[862785948605612052])
async def global_command(ctx):
    await ctx.respond(f"Pong! latency: {round(bot.latency*1000)}ms")


@bot.command(guild_ids=[862785948605612052])
async def help(ctx):
    embed = discord.Embed(
        title="Help", description="Commands:", color=0x00ff00)
    await ctx.send(embed=embed)


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


@bot.command(guild_ids=[862785948605612052])
async def advice(ctx):
    session = aiohttp.ClientSession()
    async with session.get("https://api.adviceslip.com/advice") as answer:
        answer = answer.text
        answer = json.loads(answer)
        embed = discord.Embed(
            title=f"Advice ID {answer['slip']['id']}", description=answer['slip']['advice'])
        embed.set_footer(text=f"Asked By {ctx.author}")
        await ctx.send(embed=embed)


@bot.command(guild_ids=[862785948605612052])
async def bored(ctx):
    answer = requests.get("https://www.boredapi.com/api/activity")
    answer = answer.json()
    embed = discord.Embed(title=f"{answer['activity']}")
    embed.add_field(name="Type", value=f"{answer['type']}", inline=False)
    embed.add_field(name="Participants",
                    value=f"{answer['participants']}", inline=False)
    embed.add_field(name="Price", value=f"{answer['price']}", inline=False)
    embed.set_footer(text=f"Asked By {ctx.author}")
    await ctx.send(embed=embed)


@bot.command(guild_ids=[862785948605612052])
async def joke(ctx):
    answer = requests.get(
        "https://official-joke-api.appspot.com/jokes/general/random")
    answer = answer.json()
    embed = discord.Embed(title=f"Joke ID {answer[0]['id']}")
    embed.add_field(name="Setup: ", value=answer[0]['setup'])
    embed.add_field(name="Punchline: ", value=answer[0]['punchline'])
    embed.set_footer(text=f"Asked By {ctx.author}")
    await ctx.send(embed=embed)


@bot.command(guild_ids=[862785948605612052])
async def wikisearch(ctx, *, word):
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(word)
    pages = page.summary
    embed = discord.Embed(title=word, description=pages)
    embed.set_footer(text=f"Source: {page.fullurl}")
    await ctx.send(embed=embed)


@bot.command(guild_ids=[862785948605612052])
async def youtubesearch(ctx, *, word):
    embed = discord.Embed(title=f"YouTube Search For {word}")
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
    response = requests.get(endpoint, params=query_params)
    data = response.json()
    return data['data']['url']


@bot.command(guild_ids=[862785948605612052])
async def shortlink(ctx, link):
    try:
        shortened_link = await shorten(link)
        embed = discord.Embed(title="Link Generated With Bit.ly")
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
        
#---------------------------------------Banking---------------------------------------#
@bot.command(guild_ids=[862785948605612052])
async def bank(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    bank = database.check_account(user.id)
    embed = discord.Embed(title=f"{user}'s Bank Account", color=discord.Color.blue())
    embed.add_field(name="Wallet", value=f"{bank['wallet']}", inline=False)
    embed.add_field(name="Bank", value=f"{bank['bank']}", inline=False)
    await ctx.send(embed=embed)

bot.run(config.TOKEN)
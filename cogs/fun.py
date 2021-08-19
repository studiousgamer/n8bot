import discord
from discord.ext import commands
import json
import wikipediaapi
from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build    
from PyDictionary import PyDictionary
from translate import Translator
import re

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def advice(self, ctx):
        answer = await self.bot.session.get("https://api.adviceslip.com/advice")
        answer = await answer.text()
        answer  = json.loads(answer)
        embed =  discord.Embed(title = f"Advice ID {answer['slip']['id']}",description= answer['slip']['advice'],color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.set_footer(text=f"Asked By {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def bored(self, ctx):
        answer = await self.bot.session.get("https://www.boredapi.com/api/activity")
        answer = await answer.json()
        embed = discord.Embed(title=f"{answer['activity']}",color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="Type", value=f"{answer['type']}", inline=False)
        embed.add_field(name="Participants", value=f"{answer['participants']}", inline=False)
        embed.add_field(name="Price", value=f"{answer['price']}", inline=False)
        embed.set_footer(text=f"Asked By {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        answer = await self.bot.session.get("https://official-joke-api.appspot.com/jokes/general/random")
        answer = await answer.json()
        embed =  discord.Embed(title = f"Joke ID {answer[0]['id']}",color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name = "Setup: ", value= answer[0]['setup'])
        embed.add_field(name = "Punchline: ", value= answer[0]['punchline'])
        embed.set_footer(text=f"Asked By {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def wikisearch(self, ctx, *, word):
        wiki = wikipediaapi.Wikipedia("en")
        page = wiki.page(word)
        pages = page.summary
        embed= discord.Embed(title=word, description = pages,color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.set_footer(text=f"Source: {page.fullurl}")
        await ctx.send(embed=embed)

    
    @commands.command()
    async def youtubesearch(self, ctx, *, word):
        embed = discord.Embed(title=f"YouTube Search For {word}",color=self.bot.config.EMBED_COLOR_GENERAL)
        videosSearch = VideosSearch(word, limit = 5)
        res = videosSearch.result()
        for i in range(5):
            description = ""
            description += f"Channel: {res['result'][i]['channel']['name']}, \n"
            description += f"Views: {res['result'][i]['viewCount']['short']}, \n"
            description += f"Link: [Click Here]({res['result'][i]['link']}) \n"
        embed.add_field(name=f"Title: {res['result'][i]['title']}", value= description, inline=False)
        embed.set_footer(text=f"Asked by {ctx.message.author}")
        await ctx.send(embed=embed)

    async def shorten(self, uri):
        query_params = {
            'access_token': self.bot.config.BITTLY_ACCESS_TOKEN,
            'longUrl': uri
        }
        endpoint = 'https://api-ssl.bitly.com/v3/shorten'
        response = await self.bot.session.get(endpoint, params=query_params)
        data = await response.json()
        return data['data']['url']

    @commands.command()
    async def shortlink(self, ctx, link):
        try:
            shortened_link = await self.shorten(link)
            embed = discord.Embed(title="Link Generated With Bit.ly",
                                color=self.bot.config.EMBED_COLOR_GENERAL)
            embed.add_field(name="Orignal Link:", value=link, inline=False)
            embed.add_field(name="Shortened Link:",
                            value= shortened_link,
                            inline=False)
            embed.set_footer(text=f"Powered By Bit.ly | Requested by {ctx.message.author}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("Invalid link")

    @commands.command()
    async def dog(self, ctx):
        response = await self.bot.session.get("https://dog.ceo/api/breeds/image/random")
        response_dict = await response.json()
        await ctx.send(response_dict["message"])

    @commands.command()
    async def cat(self, ctx):
        response = await self.bot.session.get("https://api.thecatapi.com/v1/images/search")
        response_dict = await response.json()
        await ctx.send(response_dict[0]["url"])

    @commands.command(aliases=["n8dev", "Youtube", "N8Dev", "N8dev", "YouTube"])
    async def youtube(self, ctx):
        api_key = self.bot.config.YOUTUBE_API_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.channels().list(part='statistics', id="UCjHNkH_KPvvHCwZEo22EzSg")
        request_2 = youtube.activities().list(part="snippet", channelId="UCjHNkH_KPvvHCwZEo22EzSg")
        request_3 = youtube.activities().list(part="contentDetails", channelId="UCjHNkH_KPvvHCwZEo22EzSg")
        response = request.execute()
        response_2 = request_2.execute()
        response_3 = request_3.execute()
        most_recent_video = response_2["items"][0]["snippet"]["title"]

        embed = discord.Embed(title="N8Dev's Channel", color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="Sub count", value=response["items"][0]["statistics"]["subscriberCount"], inline=False)
        embed.add_field(name="View count", value=response["items"][0]["statistics"]["viewCount"], inline=False)
        embed.add_field(name="Video count", value=response["items"][0]["statistics"]["videoCount"], inline=False)
        embed.add_field(name="Most recent video", value= most_recent_video, inline=False)
        embed.add_field(name="Channel link", value="https://www.youtube.com/N8Dev", inline=False)
        embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AAUvwnhUFFFpyHqZXipXPIC-aBDPJapNCk-AWCEVPein=s88-c-k-c0x00ffffff-no-rj")

        await ctx.send(embed=embed)

    @commands.command()
    async def currencyconvert(self, ctx, base, amount, to):
        MONEY_CONVERSION_URL = f'https://api.exchangerate.host/latest'
        embed = discord.Embed(title="Currency Conversion",color=self.bot.config.EMBED_COLOR_GENERAL)
        response = await self.bot.session.get(f"{MONEY_CONVERSION_URL}?base={base}&amount={amount}&symbols={to}")
        data = await response.json()
        for i in data['rates']:
            embed.add_field(name= i, value=data['rates'][i])
        embed.set_footer(text=f"Executed By {ctx.message.author}")
        await ctx.send(embed=embed)

    def sort(self, meaning):
        final = ''
        try:
            num = 0
            noun = meaning['Noun']
            final += "Noun: \n"
            for men in noun:
                num += 1
                final += f"{num}: {men}\n"
        except:
            pass
        try:
            num = 0
            Verb = meaning['Verb']
            final += f"Verb: \n"
            for men in Verb:
                num += 1
                final += f"{num}: {men}\n"
        except:
            pass
        try:
            num = 0
            Adverb = meaning['Adverb']
            final += f"Adverb: \n"
            for men in Adverb:
                num += 1
                final += f"{num}: {men}\n"
        except:
            pass
        try:
            num = 0
            Adjective = meaning['Adjective']
            final += f"Adjective: \n"
            for men in Adjective:
                num += 1
                final += f"{num}: {men}\n"
        except:
            pass
        return final


    @commands.command()
    async def meaning(self, ctx, word):
        dictionary=PyDictionary()
        mean = dictionary.meaning(word)
        embed=discord.Embed(title=f"Meaning Of {word}", description=self.sort(mean),color=self.bot.config.EMBED_COLOR_GENERAL)
        await ctx.send(embed =embed)

    @commands.command()
    async def synonym(self, ctx, word):
        dictionary=PyDictionary()
        embed=discord.Embed(title=f"Synonym of {word}", description=word,color=self.bot.config.EMBED_COLOR_GENERAL)
        mean = dictionary.synonym(word)
        if mean is None:
            await ctx.send("No synonyms found")
            return
        no = 0
        for i in mean:
            no += 1
            embed.add_field(name=f"Result {no}", value=i, inline=False)
        await ctx.send(embed =embed)

    @commands.command()
    async def antonym(self, ctx, word):
        dictionary=PyDictionary()
        embed=discord.Embed(title=f"Antonym of {word}", description=word,color=self.bot.config.EMBED_COLOR_GENERAL)
        mean = dictionary.antonym(word)
        no = 0
        if mean is None:
            await ctx.send("No antonyms found")
            return
            
        for i in mean:
            no += 1
            embed.add_field(name=f"Result {no}", value=i, inline=False)
        await ctx.send(embed =embed)

    @commands.command()
    async def translate(self, ctx, from_lang, to_lang, *, sentence):
        translator= Translator(from_lang=from_lang,to_lang=to_lang)
        translation = translator.translate(sentence)
        embed= discord.Embed(title ="Translation",color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="From Lnguage", value = f"{from_lang}", inline=False)
        embed.add_field(name="To Lnguage", value = f"{to_lang}", inline=False)
        embed.add_field(name="Translation", value = f"{translation}", inline=False)
        embed.set_footer(text=f"Executed by {ctx.message.author}")
        await ctx.send(embed =embed)
    
    @commands.command()
    async def emojify(self, ctx, *, text):
        emojified = ''
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        if text == '':
            await ctx.send('Remember to say what you want to convert!')
        else:
            for i in formatted:
                if i == ' ':
                    emojified += '     '
                else:
                    emojified += ':regional_indicator_{}: '.format(i)
            if len(emojified) + 2 >= 2000:
                await ctx.send('Your message in emojis exceeds 2000 characters!')
            if len(emojified) <= 25:
                await ctx.send('Your message could not be converted!')
            else:
                await ctx.send(emojified)

def setup(bot):
    bot.add_cog(Fun(bot))
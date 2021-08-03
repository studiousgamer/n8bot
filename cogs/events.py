import discord
from discord.ext import commands
from datetime import datetime

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.bot.config.WELCOME_CHANNEL)
        embed = discord.Embed(title=f"Welcome to the server {member}", description="Hope you enjoy your stay!", color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.set_thumbnail(url=member.avatar_url)
        message = await channel.send(embed=embed)
        await message.add_reaction("👋")

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        embed = discord.Embed(title="Message delete",color=self.bot.config.EMBED_COLOR_RED)
        embed.add_field(name="Author",value=str(message.author),inline=False)
        if len(message.content) > 1021:
            message.content = message.content[:1021]+"..."
        embed.add_field(name="Message",value=str(message.content),inline=False)
        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)

        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed) 

    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        embed = discord.Embed(title="Message edit",color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="Author",value=str(before.author),inline=False)

        if len(before.content) > 1021:
            before.content = before.content[:1021]+"..."
            print(len(before.content))
        if len(after.content) > 1021:
            after.content = after.content[:1021]+"..."
            
        embed.add_field(name="Message before",value=str(before.content),inline=False)
        embed.add_field(name="Message after",value=str(after.content),inline=False)

        
        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)

        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed) 


    @commands.Cog.listener()
    async def on_mod_ban(self,user,moderator,reason):
        embed = discord.Embed(title="Ban",color=self.bot.config.EMBED_COLOR_RED)
        embed.add_field(name="User",value=str(user),inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)
        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_mod_mute(self,user,moderator,reason,time=None):
        embed = discord.Embed(title="Mute",color=self.bot.config.EMBED_COLOR_RED)
        embed.add_field(name="User",value=str(user),inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)
        if time is not None:
            embed.add_field(name="Time",value=time,inline=False)

        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_mod_unmute(self,user,moderator):
        embed = discord.Embed(title="Unmute",color=self.bot.config.EMBED_COLOR_GREEN)
        embed.add_field(name="User",value=str(user),inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)

        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_mod_kick(self,user,moderator,reason):
        embed = discord.Embed(title="Unmute",color=self.bot.config.EMBED_COLOR_RED)
        embed.add_field(name="User",value=str(user),inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)


        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_mod_unban(self,user,moderator,reason):
        embed = discord.Embed(title="Unban",color=self.bot.config.EMBED_COLOR_GREEN)
        embed.add_field(name="User",value=str(user),inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)


        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_channel_purge(self,channel,count,moderator):
        
        embed = discord.Embed(title="Purge",color=self.bot.config.EMBED_COLOR_RED)
        embed.add_field(name="Channel",value=channel,inline=False)
        embed.add_field(name="Message count",value=count,inline=False)
        embed.add_field(name="Moderator",value=str(moderator),inline=False)



        time = datetime.now()
        time = time.strftime("%x %X")
        embed.set_footer(text=time)


        channel_ = self.bot.get_channel(self.bot.config.LOGGING_CHANNEL)
        await channel_.send(embed=embed)

def setup(bot):
        bot.add_cog(Events(bot))

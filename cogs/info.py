import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpchannel(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="How to Use the Help Channels", color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="Google before asking your question, chances are that someone has already answered it", value="https://www.google.com/", inline=False)
        embed.add_field(name="If you don't have luck with google, ask your question here! Really, just ask, don't ask to ask", value="https://dontasktoask.com/", inline=False)
        embed.add_field(name="Everyone here wants to help you, so asking your question properly will only do you good", value="https://stackoverflow.com/help/how-to-ask", inline=False)
        embed.add_field(name="Be patient", value="your question will get answered, don't go pinging random users trying to get help", inline=False)
        embed.add_field(name="After someone has helped you, make sure to thank them with the bot!", value="Type **_thanks @user_who_helped_you** in one of the help channels or in *#bot-commands* and they will level up. Don't abuse this, or you will be disciplined. You can see the top 10 users by typing **_leaderboard**, and see your own or another member's level by typing **_level @user**", inline=False)
        embed.add_field(name="Do not post images of code; use code blocks instead", value="To use code blocks type three back ticks ` and type your language's abbreviation for syntax highlighting (c# is cs, javascript is js etc), then end the message with three back ticks", inline=False)
        await ctx.send(embed=embed)

        code_blocksembed = discord.Embed(tile="How to Use Code Blocks", color=self.bot.config.EMBED_COLOR_GENERAL)
        code_blocksembed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/fAAWNq-FmClOuS5e_vT13usj-hm4Pp6bZN8kHgKpYtQ/https/media.discordapp.net/attachments/713824411257667625/795692434281070622/unknown.png")
        await ctx.send(embed=code_blocksembed)

    @commands.command()
    async def suggestfeatures(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="How to Suggest Features for Allete", color=self.bot.config.EMBED_COLOR_GENERAL)
        embed.add_field(name="What is Allete?", value="Allete is a super chill isometric mobile game I made for the Brackeys Game Jam 2021.1 that I'm now continuing post-jam. You can find the devlogs here https://www.youtube.com/watch?v=rWgo3K-4IMM&list=PLjnGtp1-JGh8lyOoiSIXoe8HZYAvnGiZW", inline=False)
        embed.add_field(name="Where do I see your plans for the game?", value="I use codecks to plan Allete, and have the board publicly visible https://open.codecks.io/allete. I update the board with each week's work, so don't be surprised if there's nothing there when you check (I haven't stopped working on it :p)", inline=False)
        embed.add_field(name="Wow this is really cool! Can I suggest features for it?", value="I'm flattered. Yes, you can suggest features for the game. I want my community to really be involved with the development of this game, so I've added the codecks bot (Decky) to the server", inline=False)
        embed.add_field(name="How do I use the codecks bot to suggest features?", value="It's easy! Just follow the steps below", inline=False)
        await ctx.send(embed=embed)

        step_oneembed = discord.Embed(title="Step One", description="Suggest your feature with the !feature <idea> command, I'm not opposed to you suggesting features for the discord as well, so go ahead and do that if you want", color=self.bot.config.EMBED_COLOR_GENERAL)
        step_oneembed.set_image(url="https://media.discordapp.net/attachments/824312805103632434/825070341633474650/unknown.png")
        await ctx.send(embed=step_oneembed)

        step_twoembed = discord.Embed(title="Step Two", description="Get at least 5 (not including the bot) upvotes (👌). The card will then be moved to a deck on the codecks board that I will see", color=self.bot.config.EMBED_COLOR_GENERAL)
        step_twoembed.set_image(url="https://cdn.discordapp.com/attachments/824288299878187008/825084003127263302/unknown.png")
        await ctx.send(embed=step_twoembed)

        step_threeembed = discord.Embed(title="Step Three", description="Respond to the bot's DM with the card ID, and any comments you'd like to add to the card", color=self.bot.config.EMBED_COLOR_GENERAL)
        step_threeembed.set_image(url="https://media.discordapp.net/attachments/824288299878187008/825084428047876136/unknown.png")
        await ctx.send(embed=step_threeembed)

        step_fourembed = discord.Embed(title="Step Four", description="That's it! The bot will let everyone know when I've started working on/finished the card you suggested. A leaderboard with the most upvoted suggestions will be posted daily, so check for that!", color=self.bot.config.EMBED_COLOR_GENERAL)
        step_fourembed.set_image(url="https://media.discordapp.net/attachments/824288299878187008/825084735196758016/unknown.png")
        await ctx.send(embed=step_fourembed)

    @commands.command()
    async def poll(self, ctx, arg1, arg2, emoji1 = "1️⃣", emoji2 = "2️⃣"):
        embed = discord.Embed(title="Poll", color=self.bot.config.EMBED_COLOR_GENERAL)

        embed.add_field(name="Option 1", value=emoji1 + " - " + arg1, inline=False)

        embed.add_field(name="Option 2", value=emoji2 + " - " + arg2, inline=False)
        embed.set_footer(text=f"Poll by {ctx.message.author}")
            

        msg = await ctx.send(embed=embed)

        await msg.add_reaction(emoji1)
        await msg.add_reaction(emoji2)



def setup(bot):
    bot.add_cog(Info(bot))
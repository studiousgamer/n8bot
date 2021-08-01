import discord
from discord.ext import commands
import asyncio 
from cogs.utils.checks import is_dev

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, time=0, *, reason="Reason unspecified"):

        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        if muted_role in member.roles:
            await ctx.send(f"`{member}` is already muted 💀")
            return
        await member.add_roles(muted_role, reason=reason)
        if time == 0:
            await ctx.send(f"`{member}` has been muted 💀")
            self.bot.dispatch("mod_mute",member,ctx.message.author,reason)
        else:
            await ctx.send(f"`{member}` has been muted for `{time}` seconds 💀")
            self.bot.dispatch("mod_mute",member,ctx.message.author,reason,time=time)
            await asyncio.sleep(time)
            await member.remove_roles(muted_role)
            self.bot.dispatch("mod_unmute",member,ctx.message.author)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name="muted")
        if muted not in member.roles:
            await ctx.send(f"`{member}` is not muted smart one 💀")
            return
        await member.remove_roles(muted)
        await ctx.send(f"`{member}` has been unmuted 😄")
        self.bot.dispatch("mod_unmute",member,ctx.message.author)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Reason unspecified"):
        await member.kick(reason=reason)
        await ctx.send(f"`{member}` has been kicked 💀")
        self.bot.dispatch("mod_kick",member,ctx.message.author,reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Reason unspecified"):

        embed = discord.Embed(title='You have been banned.', color=self.bot.config.EMBED_COLOR_RED)

        embed.add_field(name='Reason', value=reason, inline=False)

        await member.ban(reason=reason)
        try:
            await member.send(embed=embed)
        except:
            pass
        await ctx.send(f"`{member}` has been banned 💀")
        self.bot.dispatch("mod_ban",member,ctx.message.author,reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, member, *, reason="Reason unspecified"):
        bannedusers = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        guild = ctx.guild
        embed = discord.Embed(title='You have been unbanned.',color=self.bot.config.EMBED_COLOR_GREEN)
        embed.add_field(name='Server', value=guild.name, inline=False)
        embed.set_thumbnail(url=guild.icon_url)

        for ban_entry in bannedusers:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"`{user.name}` has been unbanned 😄")
                self.bot.dispatch("mod_unban",member,ctx.message.author,reason)
                embed.add_field(name='Reason', value=reason, inline=False)
                try:
                    await member.send(embed=embed)
                except:
                    pass

    @commands.command(aliases=["clean", "delete"])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        message = await ctx.send(f"Deleted `{amount}` messages")
        self.bot.dispatch("channel_purge",f"<#{ctx.channel.id}>",amount,ctx.message.author)
        await asyncio.sleep(1.5)
        await message.delete()

    @commands.command()
    @commands.check(is_dev)
    async def log(self,ctx):
        await ctx.send(file=discord.File("log.txt"))

    @log.error
    async def log_error(self,ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Logs can only be accessed by devs")
def setup(bot):
    bot.add_cog(Moderation(bot))
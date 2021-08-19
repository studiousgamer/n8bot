import discord
from discord.ext import commands
import traceback
class ErrorHandler(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):

                error = getattr(error, 'original', error)
                if ctx.command is not None:
                        if ctx.command.has_error_handler():
                                return

                if isinstance(error,commands.MissingRequiredArgument):
                        missing_argument_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        missing_argument_embed.description="Missing arguments"
                        await ctx.send(embed = missing_argument_embed)

                elif isinstance(error,commands.MissingPermissions):
                        missing_permissions_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        missing_permissions_embed.description="You do not have permission to use that command"
                        await ctx.send(embed=missing_permissions_embed)

                elif isinstance(error,commands.NoPrivateMessage):
                        no_dm_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        no_dm_embed.description="Enter a proper argument"
                        await ctx.send(embed=no_dm_embed)

                elif isinstance(error,commands.BadArgument):
                        bad_argument_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        bad_argument_embed.description="Enter a proper argument"
                        await ctx.send(embed=bad_argument_embed)

                
                elif isinstance(error,commands.MissingRole):
                        missing_role_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        missing_role_embed.description="You do not have permission to use that command"
                        await ctx.send(embed=missing_role_embed)

                elif isinstance(error,commands.CommandNotFound):
                        pass
                
                elif isinstance(error,commands.NotOwner):
                        missing_role_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        missing_role_embed.description="Don't be too smart \nDevs Are smarter than you"
                        await ctx.send(embed=missing_role_embed)
                
                elif isinstance(error, HTTPException):
                        pass
                
                else:
                        unexpected_embed = discord.Embed(title='Error', colour=self.bot.config.EMBED_COLOR_RED)
                        unexpected_embed.description="There was an unexpected error with the bot :( The devs have been notified"
                        await ctx.send(embed=unexpected_embed)
                        await self.bot.logger.error(f"Error in command {ctx.command}\n Traceback dumped")
                        with open("log.txt","a") as f:
                                traceback.print_exception(type(error), error, error.__traceback__, file=f)
    @commands.Cog.listener() 
    async def on_error(self,error):
        await self.bot.logger.error(f"Error in {error}\n Traceback dumped")
        with open("log.txt","a") as f:
                traceback.print_exception(type(error), error, error.__traceback__, file=f)


def setup(bot):
        bot.add_cog(ErrorHandler(bot))

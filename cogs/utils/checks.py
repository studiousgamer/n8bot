async def is_dev(ctx):
    role = ctx.guild.get_role(ctx.bot.config.DEV_ROLE_ID)
    return role in ctx.message.author.roles
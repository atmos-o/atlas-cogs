from .rolesync import RoleSync

async def setup(bot):
    await bot.add_cog(cog)
    cog = RoleSync(bot)

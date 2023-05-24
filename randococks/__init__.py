from .randococks import randococks

async def setup(bot):
    await bot.add_cog(randococks(bot))
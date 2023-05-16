from .randococks import randococks

async def setup(bot):
    bot.add_cog(randococks(bot))
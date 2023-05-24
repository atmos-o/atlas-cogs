from .syncr import Syncr

async def setup(bot):
    await bot.add_cog(Syncr(bot))

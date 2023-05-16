from .ytdlp import YTDLP

async def setup(bot):
    bot.add_cog(YTDLP(bot))
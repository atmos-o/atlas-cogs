from .ytdlp import YTDLP

def setup(bot):
    bot.add_cog(YTDLP(bot))
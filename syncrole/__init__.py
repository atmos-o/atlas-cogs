from .syncrole import Syncrole


def setup(bot):
    bot.add_cog(Syncrole(bot))
    bot.sync_roles = {}

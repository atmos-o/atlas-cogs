import discord
from redbot.core import commands

class Syncrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.master_roles = {}  # dictionary to keep track of master roles and sub roles

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sadd(self, ctx, role: discord.Role, *sub_roles: discord.Role):
        """
        Set or update the master role for the server WITH sub roles
        """
        guild_id = ctx.guild.id

        # Check if the role already exists as a master role
        if guild_id in self.master_roles and role.id == self.master_roles[guild_id]['master_role_id']:
            self.master_roles[guild_id]['sub_roles_ids'] = [r.id for r in sub_roles]
            await ctx.send(f'Sub roles for {role.name} updated to {[r.name for r in sub_roles]}')
        else:
            self.master_roles[guild_id] = {
                'master_role_id': role.id,
                'sub_roles_ids': [r.id for r in sub_roles]
            }
            await ctx.send(f'Master role set to {role.name} with sub roles {[r.name for r in sub_roles]}')

    @commands.command()
    async def slist(self, ctx):
        """
        List all active master roles with their sub roles
        """
        response = 'Active master roles:\n'
        for guild_id, role_info in self.master_roles.items():
            guild = self.bot.get_guild(guild_id)
            master_role = guild.get_role(role_info['master_role_id'])
            sub_roles = [guild.get_role(role_id) for role_id in role_info['sub_roles_ids']]
            response += f'{guild.name}: {master_role.name} ({len(sub_roles)} sub roles)\n'
            if len(sub_roles) > 0:
                response += f'\tSub roles: {[r.name for r in sub_roles]}\n'

        await ctx.send(response)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Check if a member has the master role removed and remove sub roles if necessary
        """
        if before.roles == after.roles:
            return

        guild_id = before.guild.id
        if guild_id not in self.master_roles:
            return

        master_role_id = self.master_roles[guild_id]['master_role_id']
        sub_roles_ids = self.master_roles[guild_id]['sub_roles_ids']

        if master_role_id not in [r.id for r in before.roles] and master_role_id in [r.id for r in after.roles]:
            # master role added back, do nothing
            return

        if master_role_id in [r.id for r in before.roles] and master_role_id not in [r.id for r in after.roles]:
            # master role removed, remove sub roles
            sub_roles = [r for r in after.roles if r.id in sub_roles_ids]
            await after.remove_roles(*sub_roles)

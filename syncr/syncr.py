import os
import json
import discord
from discord.ext import commands
from redbot.core import commands, Config

class Syncr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), 'syncr_config.json')
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            self.config = {}
        else:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sadd(self, ctx, master_role: discord.Role, *sub_roles: discord.Role):
        if str(ctx.guild.id) not in self.config:
            self.config[str(ctx.guild.id)] = {}

        self.config[str(ctx.guild.id)][str(master_role.id)] = {
            'toggle': 'yes',
            'sub_roles': [str(role.id) for role in sub_roles]
        }
        self.save_config()
        await ctx.send("Master Role and Sub Roles added.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stoggle(self, ctx, master_role: discord.Role):
        if str(ctx.guild.id) in self.config:
            guild_config = self.config[str(ctx.guild.id)]
            if str(master_role.id) in guild_config:
                toggle_status = guild_config[str(master_role.id)].get('toggle', 'yes')
                if toggle_status == 'yes':
                    guild_config[str(master_role.id)]['toggle'] = 'no'
                    self.save_config()
                    await ctx.send("Tracking disabled for the Master Role.")
                else:
                    guild_config[str(master_role.id)]['toggle'] = 'yes'
                    self.save_config()
                    await ctx.send("Tracking enabled for the Master Role.")
            else:
                guild_config[str(master_role.id)] = {'toggle': 'yes'}
                self.save_config()
                await ctx.send("Tracking enabled for the Master Role.")
        else:
            self.config[str(ctx.guild.id)] = {str(master_role.id): {'toggle': 'yes'}}
            self.save_config()
            await ctx.send("Tracking enabled for the Master Role.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def slist(self, ctx):
        if str(ctx.guild.id) in self.config:
            guild_config = self.config[str(ctx.guild.id)]
            response = "Master Roles:\n"
            
            for master_role_id, data in guild_config.items():
                if master_role_id == 'master_role':
                    continue
                
                master_role = ctx.guild.get_role(int(master_role_id))
                if master_role is not None:
                    response += f"{master_role.mention} (ID: {master_role.id})\n"
                    sub_roles = data.get('sub_roles', [])
                    for sub_role_id in sub_roles:
                        sub_role = ctx.guild.get_role(int(sub_role_id))
                        if sub_role is not None:
                            response += f"- {sub_role.mention} (ID: {sub_role.id})\n"
                else:
                    response += f"Invalid Master Role ID: {master_role_id}\n"
            
            await ctx.send(response)
        else:
            await ctx.send("No Master Roles are being tracked in this server.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sdel(self, ctx, master_role: discord.Role):
        if str(ctx.guild.id) in self.config:
            guild_config = self.config[str(ctx.guild.id)]
            if str(master_role.id) in guild_config:
                del guild_config[str(master_role.id)]
                self.save_config()
                await ctx.send("Master Role and associated Sub Roles deleted.")
                return
        await ctx.send("Master Role not found.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if str(after.guild.id) in self.config:
            guild_config = self.config[str(after.guild.id)]

            for master_role_id, data in guild_config.items():
                if master_role_id == 'master_role':
                    continue

                toggle_status = data.get('toggle', 'yes')
                if toggle_status == 'yes':
                    master_role = after.guild.get_role(int(master_role_id))
                    if master_role is not None and master_role in before.roles and master_role not in after.roles:
                        sub_roles = data.get('sub_roles', [])
                        for sub_role_id in sub_roles:
                            sub_role = after.guild.get_role(int(sub_role_id))
                            if sub_role is not None and sub_role in after.roles:
                                await after.remove_roles(sub_role, reason="Master Role Removed")

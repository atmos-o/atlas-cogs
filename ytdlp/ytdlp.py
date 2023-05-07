import os
import subprocess
import datetime
import discord
from redbot.core import commands, Config


class YTDLP(commands.Cog):

    """A cog for downloading videos using YT-DLP."""

    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = {}
        # Load configuration
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild_settings = {"allowed_roles": []}
        self.config.register_guild(**default_guild_settings)

    @commands.command()
    async def dl(self, ctx, url: str):
        """Downloads a video with YT-DLP and uploads it to the Discord channel."""

        # Check if the user is the server owner or has the required role.
        allowed_roles = await self.config.guild(ctx.guild).allowed_roles()
        if ctx.author == ctx.guild.owner or any(role.id in allowed_roles for role in ctx.author.roles):
            pass  # skip permission check
        else:
            await ctx.send("You do not have permission to use this command.")
            return

        # Send "Video is downloading..." message.
        message = await ctx.send("Video is downloading...")

        # Determine the server's Boost tier.
        boost_tier = ctx.guild.premium_tier

        # Set the maximum file size based on the Boost tier.
        if boost_tier == 1:
            max_file_size = 24117248
        elif boost_tier == 2:
            max_file_size = 50331648
        elif boost_tier == 3:
            max_file_size = 102760448
        else:
            max_file_size = 25000000

        # Set the output path based on the server name.
        cache_folder = "/data/cogs/CogManager/cogs/ytdlp/cache/"
        server_name = str(ctx.guild.id)
        output_path = os.path.join(cache_folder, server_name)
        ext = ".mp4"
        os.makedirs(output_path, exist_ok=True)
        # Set the output file name.
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d %H.%M.%S")
        output_file = os.path.join(output_path, f"{date_str}{ext}")

        # Clearing cache folder
        for root, dirs, files in os.walk(output_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)



        # Download the video with YT-DLP.
        args = ["yt-dlp", "--compat-options", "filename-sanitization", "-f", "mp4", "-S", "vcodec:h264", "-o", output_file, url]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        process.stdout.close()
        process.stderr.close()

        # Check for errors and send a message to the Discord channel.
        if process.returncode != 0:
            # Delete "Video is downloading..." message.
            await message.delete()
            await ctx.send(f"Error downloading video: {stderr.decode('utf-8')}")
            return

        # Split the video into segments if it exceeds the maximum file size.
        file_size = os.path.getsize(output_file)
        duration = float(subprocess.check_output(["ffprobe", "-i", output_file, "-show_format", "-v", "quiet", "-of", "csv=%s" % ("p=0")]).decode('utf-8').split(",")[11])
        segment_duration = (max_file_size / file_size) * duration
        if file_size > max_file_size:
            segment_base_filename = os.path.join(output_path, "output")
            ff_args = ["ffmpeg", "-i", output_file, "-c", "copy", "-map", "0", "-f", "segment", "-segment_time", f"{segment_duration}", "-reset_timestamps", "1", f"{segment_base_filename}_%03d.mp4"]
            process = subprocess.Popen(ff_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            process.stdout.close()
            process.stderr.close()
            segment_files = sorted([os.path.join(output_path, f) for f in os.listdir(output_path) if f.startswith("output_")])
            for segment_file in segment_files:
                with open(segment_file, "rb") as f:
                    await ctx.send(file=discord.File(f))
                os.remove(segment_file)
        else:
            await ctx.send(file=discord.File(output_file))

        # Delete the temporary files.
        os.remove(output_file)

        # Delete "Video is downloading..." message.
        await message.delete()




    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dlallow(self, ctx, role: discord.Role):
        """Adds a role to the list of allowed roles."""
        async with self.config.guild(ctx.guild).allowed_roles() as allowed_roles:
            if str(role.id) not in allowed_roles:
                allowed_roles.append(str(role.id))
                await ctx.send(f"{role.name} is now allowed to use this command.")
            else:
                await ctx.send(f"{role.name} is already allowed to use this command.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dlremove(self, ctx, role: discord.Role):
        """Removes a role from the list of allowed roles."""
        async with self.config.guild(ctx.guild).allowed_roles() as allowed_roles:
            if str(role.id) in allowed_roles:
                allowed_roles.remove(str(role.id))
                await ctx.send(f"{role.name} is no longer allowed to use this command.")
            else:
                await ctx.send(f"{role.name} is not currently allowed to use this command.")


# # # 2nd

    @commands.command()
    async def dlt(self, ctx, url: str, start: int, end: int):
        """Downloads a specific part of a video with YT-DLP and uploads it to the Discord channel."""

        # Send "Video is downloading..." message.
        message = await ctx.send("Video is downloading...")

        # Determine the server's Boost tier.
        boost_tier = ctx.guild.premium_tier

        # Set the maximum file size based on the Boost tier.
        if boost_tier == 1:
            max_file_size = 24117248
        elif boost_tier == 2:
            max_file_size = 52428800
        elif boost_tier == 3:
            max_file_size = 104857600
        else:
            max_file_size = 25000000


        # Set the output path based on the server name.
        cache_folder = "/data/cogs/CogManager/cogs/ytdlp/cache/"
        server_name = ctx.guild.id
        output_path = f"{cache_folder}{server_name}"
        os.makedirs(output_path, exist_ok=True)
        # Set the output file name.
        output_file = os.path.join(output_path, "output.mp4")

        # Clearing cache folder
        for file in os.listdir(output_path):
            file_path = os.path.join(output_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


        # Download the video with YT-DLP.
        args = ["yt-dlp", "--compat-options", "filename-sanitization", "-f", "mp4", "-S", "vcodec:h264", "-o", output_file, "--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts", url]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check for errors and send a message to the Discord channel.
        if process.returncode != 0:
            await ctx.send(f"Error downloading video: {stderr.decode('utf-8')}")
            return

        # Split the video into segments if it exceeds the maximum file size.
        file_size = os.path.getsize(output_file)
        duration = float(subprocess.check_output(["ffprobe", "-i", output_file, "-show_format", "-v", "quiet", "-of", "csv=%s" % ("p=0")]).decode('utf-8').split(",")[11])
        segment_duration = (max_file_size / file_size) * duration
        if file_size > max_file_size:
            segment_base_filename = os.path.join(output_path, "output")
            ff_args = ["ffmpeg", "-i", output_file, "-c", "copy", "-map", "0", "-f", "segment", "-segment_time", f"{segment_duration}", "-reset_timestamps", "1", f"{segment_base_filename}_%03d.mp4"]
            process = subprocess.Popen(ff_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            process.stdout.close()
            process.stderr.close()
            segment_files = sorted([os.path.join(output_path, f) for f in os.listdir(output_path) if f.startswith("output_")])
            for segment_file in segment_files:
                with open(segment_file, "rb") as f:
                    await ctx.send(file=discord.File(f))
                os.remove(segment_file)
        else:
            await ctx.send(file=discord.File(output_file))

        # Delete the temporary files.
        os.remove(output_file)

        # Delete "Video is downloading..." message.
        await message.delete()



def setup(bot):
    bot.add_cog(YTDLP(bot))

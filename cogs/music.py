from discord.ext import commands
import discord.utils
import asyncio
import json


class music:
    """
    Super in progress, and I don't even really know what I'm doing.
    """
    def __init__(self, bot):
        self.rasis = bot
        self.connections = {}
        self.queues = {}
        self.playing = {}
        # this line not needed on Linux apparently
        # discord.opus.load_opus(json.load(open('config.json'))["opusdir"])

    @commands.group(pass_context=True)
    async def yt(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.message.author.voice_channel.name in self.connections:
                v = 'Currently playing in ' + ctx.message.author.voice_channel.name + ':\n'
                x = self.queues[ctx.message.author.voice_channel.name][0]
                v += x.title + ' [' + str(math.floor(x.duration / 60)) + ':'
                v += str(x.duration % 60) + ']\n'
                await self.rasis.say(v)

    @yt.command(name='play', pass_context=True)
    async def play(self, ctx):
        if 'youtu' not in ctx.message.content:
            await self.rasis.say('Only Youtube links are supported. If you got this error incorrectly, maybe something\'s funky with your link.')
        else:
            vc = ctx.message.author.voice_channel.name
            playr = await self.connections[vc].create_ytdl_player(ctx.message.content[9:].strip(),
                                                                  ytdl_options={'ignoreerrors': True,
                                                                                'noplaylist': True})
            self.queues[vc].append(playr)
            await asyncio.sleep(1)
            if vc not in self.playing or not self.playing[vc]:
                await self.qloop(vc)

    async def qloop(self, vc):
        self.playing[vc] = True
        try:
            self.queues[vc][0].start()
        finally:
            while not self.queues[vc][0].is_done():
                await asyncio.sleep(5)
        try:
            self.queues[vc][0].start()
        except Exception as e:
            do = 'nothing'
        else:
            self.queues[vc].pop(0)
        if len(self.queues[vc]) == 0:
            self.playing[vc] = False
        else:
            await self.qloop(vc)

    @yt.command(name='join', pass_context=True)
    async def join(self, ctx):
        try:
            if ctx.message.author.voice_channel.name not in self.connections:
                self.connections[ctx.message.author.voice_channel.name] = await self.rasis.join_voice_channel(ctx.message.author.voice_channel)
                self.queues[ctx.message.author.voice_channel.name] = []
        except discord.DiscordException as e:
            await self.rasis.say('Oh shit: `{}` : {}'.format(type(e).__name__, e))

    @yt.command(name='destroy', pass_context=True)
    async def destroy(self, ctx):
        try:
            if ctx.message.author.voice_channel.name in self.connections:
                self.connections[ctx.message.author.voice_channel.name].disconnect()
                self.queues[ctx.message.author.voice_channel.name] = []
        except discord.DiscordException as e:
            await self.rasis.say('Oh shit: `{}` : {}'.format(type(e).__name__, e))

    @yt.command(name='vol', pass_context=True)
    async def vol(self, ctx):
        self.queues[ctx.message.author.voice_channel.name][0].volume = float(ctx.message.content[9:])


def setup(rasis):
    rasis.add_cog(music(rasis))

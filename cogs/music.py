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
        discord.opus.load_opus(json.load(open('config.json'))["opusdir"])

    @commands.group(pass_context=True)
    async def yt(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.message.author.voice_channel.name in self.connections:
                v = 'Current queue for ' + ctx.message.author.voice_channel.name + ':\n'
                for x in self.queues[ctx.message.author.voice_channel.name]:
                    v += x.title + ' [' + str(round(x.duration / 60)) + ':' + str(x.duration % 60) + ']\n'
                await self.rasis.say(v)

    @yt.command(name='play', pass_context=True)
    async def play(self, ctx):
        if 'youtu' not in ctx.message.content:
            await self.rasis.say('Only Youtube links are supported. If you got this error incorrectly, maybe something\'s funky with your link.')
        else:
            vc = ctx.message.author.voice_channel.name
            playr = await self.connections[vc].create_ytdl_player(ctx.message.content[9:].strip(),
                                                                  ytdl_options={'ignoreerrors': True})
            self.queues[vc].append(playr)
            await asyncio.sleep(1)
            if vc not in self.playing or not self.playing[vc]:
                await self.qloop(vc)

    async def qloop(self, vc):
        self.playing[vc] = True
        self.queues[vc][0].start()
        while not self.queues[vc][0].is_done():
            await asyncio.sleep(5)
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


def setup(rasis):
    rasis.add_cog(music(rasis))

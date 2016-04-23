from discord.ext import commands
import discord.utils
import asyncio
import json

class music:
	"""
	Super in progress, and I don't even really know what I'm doing.
	"""
	def __init__(self, megumin):
		self.megumin = megumin
		self.connections = {}
		discord.opus.load_opus(json.load(open('config.json'))["opusdir"])

	@commands.group(pass_context=True)
	async def yt(self, ctx):
		if 'youtu.be' in ctx.message.content:
			await self.megumin.say('eh')
		if 'https://www.youtube.com/watch?v=' in ctx.message.content:
			return

	@yt.command(name='join', pass_context=True)
	async def join(self, ctx):
		vc = ctx.message.content[10:].lower()
		if vc not in self.connections:
			for channel in list(ctx.message.server.channels):
				if (channel.type is discord.ChannelType.voice) and (channel.name.lower() == vc):
					self.connections[vc] = await self.megumin.join_voice_channel(channel)

def setup(megumin):
	megumin.add_cog(music(megumin))

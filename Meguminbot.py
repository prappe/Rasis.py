import discord
import asyncio
import random
import json
from discord.ext import commands
from cogs.utils import checks

megumin = commands.Bot(command_prefix=';;', description='Megumin! build 0 — by Iced Pråppe — built with discord.py (thanks Danny you\'re a real swood guy)', pm_help=None, help_attrs=dict(hidden=True))
exts = ['cogs.music']

@megumin.event
async def on_ready():
	print('Logged in as {}#{} : {}'.format(megumin.user.name,megumin.user.discriminator,megumin.user.id))
	for extension in exts:
		try:
			megumin.load_extension(extension)
			print('{} loaded'.format(extension))
		except Exception as e:
			print('{} failed to load :c\n{}: {}'.format(extension, type(e).__name__, e))

@megumin.event
async def on_message(message):
	await megumin.process_commands(message)

@megumin.command()
async def testx(*, swex : str):
	"""Test command."""
	await megumin.say('test indeed: {}'.format(swex))

@megumin.command(hidden=True)
@checks.is_owner()
async def load(*, module : str):
	"""Loads a thing."""
	module = module.strip()
	try:
		megumin.load_extension(module)
	except Exception as e:
		await megumin.say('Ouch.\n{}: {}'.format(type(e).__name__, e))
	else:
		await megumin.say('Got it, {} loaded.'.format(module))

@megumin.command(hidden=True)
@checks.is_owner()
async def unload(*, module : str):
	"""Unloads a thing."""
	module = module.strip()
	try:
		megumin.unload_extension(module)
	except Exception as e:
		await megumin.say('Ouch.\n{}: {}'.format(type(e).__name__, e))
	else:
		await megumin.say('Alright, {} unloaded.'.format(module))

megumin.run(json.load(open('config.json'))["token"])

import discord
import asyncio
import random
import json
import os
import psutil
from discord.ext import commands
from cogs.utils import checks

rasis = commands.Bot(command_prefix=';;', description='''Rasis! build 56
                     by Pråppe — built with discord.py''',
                     pm_help=None, help_attrs=dict(hidden=True))
exts = ['cogs.music', 'cogs.times']


@rasis.event
async def on_ready():
    print('Logged in as {}#{} : {}'.format(rasis.user.name,
                                           rasis.user.discriminator,
                                           rasis.user.id))
    for extension in exts:
        try:
            rasis.load_extension(extension)
            print('{} loaded'.format(extension))
        except Exception as e:
            print('{} failed to load :c\n{}: {}'.format(extension,
                                                        type(e).__name__, e))


@rasis.event
async def on_message(message):
    await rasis.process_commands(message)


@rasis.command(description="what the fuck do you think it is")
async def testx(*, swex: str):
    """Test command."""
    await rasis.say('test indeed: {}'.format(swex))


@rasis.command(description="Checks memory usage.", hidden=True)
async def mem():
    process = psutil.Process(os.getpid())
    await rasis.say(str(round(int(process.memory_info().rss) / 1000000, 1)) + 'MB in use.')


@rasis.command(description="thing", hidden=True)
@checks.is_owner()
async def edit(*, fn: str):
    """Thing."""
    try:
        await rasis.edit_profile(avatar=open(fn, 'rb').read())
    except Exception as e:
        await rasis.say('Ouch.\n{}: {}'.format(type(e).__name__, e))


@rasis.command(hidden=True)
@checks.is_owner()
async def load(*, module: str):
    """Loads a thing."""
    module = module.strip()
    try:
        rasis.load_extension(module)
    except Exception as e:
        await rasis.say('Ouch.\n{}: {}'.format(type(e).__name__, e))
    else:
        await rasis.say('Got it, {} loaded.'.format(module))


@rasis.command(hidden=True)
@checks.is_owner()
async def unload(*, module: str):
    """Unloads a thing."""
    module = module.strip()
    try:
        rasis.unload_extension(module)
    except Exception as e:
        await rasis.say('Ouch.\n{}: {}'.format(type(e).__name__, e))
    else:
        await rasis.say('Alright, {} unloaded.'.format(module))


@rasis.command(hidden=True)
@checks.is_owner()
async def reload(*, module: str):
    """Reloads a thing."""
    module = module.strip()
    try:
        rasis.unload_extension(module)
        await asyncio.sleep(3)
        rasis.load_extension(module)
    except Exception as e:
        await rasis.say('Ouch.\n{}: {}'.format(type(e).__name__, e))
    else:
        await rasis.say('Okay, {} reloaded.'.format(module))

rasis.run(json.load(open('config.json'))["token"])

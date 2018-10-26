import aiohttp
import asyncio
import json
import math
import os
import random

from cogs.utils import checks
import discord
from discord.ext import commands
import livejson
import psutil


rasis = commands.Bot(command_prefix=';;', description='''Rasis! build 74
                     by Prappe — built with discord.py''',
                     pm_help=None, help_attrs=dict(hidden=True))
rasis.session = aiohttp.ClientSession(loop=rasis.loop)
exts = ['cogs.music', 'cogs.times']

xp_list = livejson.File('xp.json')


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
async def on_message(m):
    await rasis.process_commands(m)
    with livejson.File('xp.json') as xp_list:
        if m.author.id not in xp_list:
            xp_list[m.author.id] = {}
            xp_list[m.author.id]['xp'] = 0
            xp_list[m.author.id]['lvl'] = 1
        xp_list[m.author.id]['xp'] += len(m.content) + 7
        if len(m.content) > 1200:
            xp_list[m.author.id]['xp'] -= (len(m.content) + 9)
        xp_list[m.author.id]['name'] = m.author.display_name


@rasis.command(description="Toontown invasions.")
async def inv():
    """Toontown invasions."""
    async with rasis.session.get('https://www.toontownrewritten.com/api/invasions') as r:
        ix = await r.json()
    if ix['error'] is not None:
        await rasis.say('Some error occurred: {}'.format(ix['error']))
    else:
        m = '*There are {} invasions in ToonTown right now.*'.format(len(ix['invasions']))
        for n, i in ix['invasions'].items():
            m += '\n**{}** invasion in {}: {} cogs defeated'.format(i['type'], n, i['progress'])
        await rasis.say(m)


@rasis.command(pass_context=True)
async def xp(ctx):
    """
    Experience system description. TODO: Don't forget to write this.
    """
    with livejson.File('xp.json') as xp_list:
        if len(ctx.message.mentions) != 0:
            u = xp_list[ctx.message.mentions[0].id]
            u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
            if u['lvl'] < 1:
                u['lvl'] = 1
            await rasis.say('{} is level {} with {}XP. They have {}XP to go before the next level.'.format(ctx.message.mentions[0].display_name, u['lvl'], u['xp'], _nextXP(u['xp'], u['lvl'])))
        else:
            u = xp_list[ctx.message.author.id]
            u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
            if u['lvl'] < 1:
                u['lvl'] = 1
            await rasis.say('You are level {} with {}XP. You have {}XP to go before the next level.'.format(u['lvl'], u['xp'], _nextXP(u['xp'], u['lvl'])))


def _nextXP(xp, lvl):
    _xp = 1000 * (1.3 ** lvl)
    return math.floor(_xp - xp)


@rasis.command(pass_context=True)
async def rank(ctx):
    """
    XP Ranking.
    """
    with livejson.File('xp.json') as xp_list:
        _xp_list = {}
        for k in xp_list:
            _xp_list[k] = xp_list[k]['xp']
        _u = []
        for u in sorted(_xp_list, key=_xp_list.get, reverse=True):
            _u.append(u)
            xp_list[u]['rank'] = len(_u)
        if len(ctx.message.mentions) != 0:
            u = xp_list[ctx.message.mentions[0].id]
            u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
            if u['lvl'] < 1:
                u['lvl'] = 1
            await rasis.say('{} is #{} at level {} with {}XP.'.format(ctx.message.mentions[0].display_name, xp_list[ctx.message.mentions[0].id]['rank'], xp_list[ctx.message.mentions[0].id]['lvl'], xp_list[ctx.message.mentions[0].id]['xp']))
        else:
            u = xp_list[ctx.message.author.id]
            u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
            if u['lvl'] < 1:
                u['lvl'] = 1
            await rasis.say('You are #{} at level {} with {}XP.'.format(xp_list[ctx.message.author.id]['rank'], xp_list[ctx.message.author.id]['lvl'], xp_list[ctx.message.author.id]['xp']))


@rasis.command(pass_context=True)
async def top(ctx):
    """
    XP Leaderboards.
    """
    with livejson.File('xp.json') as xp_list:
        _xp_list = {}
        for k in xp_list:
            _xp_list[k] = xp_list[k]['xp']
        _u = []
        for u in sorted(_xp_list, key=_xp_list.get, reverse=True):
            _u.append(u)
            xp_list[u]['rank'] = len(_u)
        m = 'Top 10 users:'
        i = 1
        for u in _u[0:10]:
            xp_list[u]['lvl'] = math.floor(math.log((xp_list[u]['xp'] / 1000), 1.3)) + 1
            if xp_list[u]['lvl'] < 1:
                xp_list[u]['lvl'] = 1
            m += '\n#{}: {} at level {} with {}XP.'.format(i, xp_list[u]['name'], xp_list[u]['lvl'], xp_list[u]['xp'])
            i += 1
            # x = None
        await rasis.say(m)


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

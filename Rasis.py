import discord
import asyncio
import random
import json
import os
import psutil
from discord.ext import commands
from cogs.utils import checks
import livejson
import math
import requests

rasis = commands.Bot(command_prefix=';;', description='''Rasis! build 74
                     by Prappe — built with discord.py''',
                     pm_help=None, help_attrs=dict(hidden=True))
exts = ['cogs.music', 'cogs.times']

xpw_x = livejson.File('xp.json')


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
    if m.author.id not in xpw_x:
        xpw_x[m.author.id] = {}
        xpw_x[m.author.id]['xp'] = 0
        xpw_x[m.author.id]['lvl'] = 1
    xpw_x[m.author.id]['xp'] += len(m.content) + 7
    if len(m.content) > 1200:
        xpw_x[m.author.id]['xp'] -= (len(m.content) + 9)
    xpw_x[m.author.id]['name'] = m.author.display_name


@rasis.command(description="Toontown invasions.")
async def inv():
    """Toontown invasions."""
    r = requests.get('https://www.toontownrewritten.com/api/invasions')
    ix = r.json()
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
    if len(ctx.message.mentions) != 0:
        u = xpw_x[ctx.message.mentions[0].id]
        u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
        if u['lvl'] < 1:
            u['lvl'] = 1
        await rasis.say('{} is level {} with {}XP. They have {}XP to go before the next level.'.format(ctx.message.mentions[0].display_name, u['lvl'], u['xp'], _nextXP(u['xp'], u['lvl'])))
    else:
        u = xpw_x[ctx.message.author.id]
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
    _xpw_x = {}
    for k in xpw_x:
        _xpw_x[k] = xpw_x[k]['xp']
    _u = []
    for u in sorted(_xpw_x, key=_xpw_x.get, reverse=True):
        _u.append(u)
        xpw_x[u]['rank'] = len(_u)
    if len(ctx.message.mentions) != 0:
        u = xpw_x[ctx.message.mentions[0].id]
        u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
        if u['lvl'] < 1:
            u['lvl'] = 1
        await rasis.say('{} is #{} at level {} with {}XP.'.format(ctx.message.mentions[0].display_name, xpw_x[ctx.message.mentions[0].id]['rank'], xpw_x[ctx.message.mentions[0].id]['lvl'], xpw_x[ctx.message.mentions[0].id]['xp']))
    else:
        u = xpw_x[ctx.message.author.id]
        u['lvl'] = math.floor(math.log((u['xp'] / 1000), 1.3)) + 1
        if u['lvl'] < 1:
            u['lvl'] = 1
        await rasis.say('You are #{} at level {} with {}XP.'.format(xpw_x[ctx.message.author.id]['rank'], xpw_x[ctx.message.author.id]['lvl'], xpw_x[ctx.message.author.id]['xp']))


@rasis.command(pass_context=True)
async def top(ctx):
    """
    XP Leaderboards.
    """
    _xpw_x = {}
    for k in xpw_x:
        _xpw_x[k] = xpw_x[k]['xp']
    _u = []
    for u in sorted(_xpw_x, key=_xpw_x.get, reverse=True):
        _u.append(u)
        xpw_x[u]['rank'] = len(_u)
    m = 'Top 10 users:'
    i = 1
    for u in _u[0:10]:
        xpw_x[u]['lvl'] = math.floor(math.log((xpw_x[u]['xp'] / 1000), 1.3)) + 1
        if xpw_x[u]['lvl'] < 1:
            xpw_x[u]['lvl'] = 1
        m += '\n#{}: {} at level {} with {}XP.'.format(i, xpw_x[u]['name'], xpw_x[u]['lvl'], xpw_x[u]['xp'])
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

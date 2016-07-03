from discord.ext import commands
import discord.utils
import asyncio
import livejson
import datetime
import pytz
import time


class times:
    """
    Time-related stuff, like comparing user timezones.
    """

    def __init__(self, bot):
        self.rasis = bot
        self.times = livejson.File('times.json')

    @commands.group(pass_context=True)
    async def time(self, ctx):
        """Get the current time for someone or get the difference in two people's times.
        Usage: ;;time @dude420 >>> It's currently Wed June 29 2016, 06:37 PM EDT for xXdude420Xx right now.
        Usage: ;;time @dude420 @westcoast69 >>> xXdude420Xx is 3 hours ahead of CaliforniaGames69."""
        if ctx.invoked_subcommand is None:
            if len(ctx.message.mentions) == 1:
                if ctx.message.mentions[0].id in self.times:
                    tz = pytz.timezone(self.times[ctx.message.mentions[0].id])
                    fmt = '%a %B %d %Y, %I:%M %p %Z'
                    loc_dt = datetime.datetime.now(tz).astimezone(tz)
                    await self.rasis.say('It\'s currently ' + loc_dt.strftime(fmt) + ' for ' + ctx.message.mentions[0].display_name + ' right now.')
                else:
                    await self.rasis.say('I don\'t think ' + ctx.message.mentions[0].display_name + ' has set their timezone yet. Tell them to run `;;time zones <code>` and/or `;;time set <zone>` first.')
            elif len(ctx.message.mentions) == 2:
                if ctx.message.mentions[0].id not in self.times and ctx.message.mentions[1].id not in self.times:
                    await self.rasis.say('I don\'t think either ' + ctx.message.mentions[0].display_name + ' or ' + ctx.message.mentions[1].display_name + ' have set their timezone yet. Tell them to run `;;time zones <code>` and/or `;;time set <zone>` first.')
                elif ctx.message.mentions[0].id not in self.times:
                    await self.rasis.say('I don\'t think ' + ctx.message.mentions[0].display_name + ' has set their timezone yet. Tell them to run `;;time zones <code>` and/or `;;time set <zone>` first.')
                elif ctx.message.mentions[1].id not in self.times:
                    await self.rasis.say('I don\'t think ' + ctx.message.mentions[1].display_name + ' has set their timezone yet. Tell them to run `;;time zones <code>` and/or `;;time set <zone>` first.')
                else:
                    tz0 = pytz.timezone(self.times[ctx.message.mentions[0].id])
                    tz1 = pytz.timezone(self.times[ctx.message.mentions[1].id])
                    fmt = "%z"
                    loc_dt0 = tz0.localize(datetime.datetime.now())
                    loc_dt1 = tz1.localize(datetime.datetime.now())
                    h0 = int(loc_dt0.strftime(fmt).strip('+'))
                    h1 = int(loc_dt1.strftime(fmt).strip('+'))
                    d = (h0 - h1) / 100
                    if d > 0:
                        diff = str(d) + ' hours ahead of '
                    elif d < 0:
                        diff = str(abs(d)) + ' hours behind '
                    else:
                        diff = 'in the same timezone as '
                    await self.rasis.say(ctx.message.mentions[0].display_name + ' is ' + diff + ctx.message.mentions[1].display_name + '.')

    @time.command(name='zones', pass_context=True)
    async def zones(self, ctx, *, code: str):
        """List the timezones of a particular country.
        Usage: ;;time zones nz >>> New Zealand Timezones: Pacific/Auckland Pacific/Chatham"""
        try:
            await self.rasis.say('**' + pytz.country_names[code] + ' Timezones:** ' + ' **|** '.join(pytz.country_timezones[code]))
        except Exception as e:
            await self.rasis.say('Ouch.\n{}: {}\nIf this was a KeyError (I don\'t have code to check if it was or not), make sure you\'re using an ISO 3166-2 2-letter country code, like US or JP.'.format(type(e).__name__, e))

    @time.command(name='set', pass_context=True)
    async def set(self, ctx, *, zone: str):
        """Set a user's own time zone. You can get a list of your timezones from ;;time zones <code>.
        Usage: ;;time set America/New_York >>> Timezone set as America/New_York."""
        try:
            if len(pytz.timezone(zone).zone) < 6:
                await self.rasis.say('Timezone set as ' + pytz.timezone(zone).zone + '. But be warned — using abbreviated timezones (like \'EST\') doesn\'t account for Daylight Savings Time. See `;;time zones <code>` for a more accurate time.')
            await self.rasis.say('Timezone set as ' + pytz.timezone(zone).zone + '.')
            self.times[ctx.message.author.id] = zone
        except Exception as e:
            await self.rasis.say('Ouch.\n{}: {}\nTry running `;;time zones <code>` first to get a list of acceptable timezone names.'.format(type(e).__name__, e))


def setup(rasis):
    rasis.add_cog(times(rasis))

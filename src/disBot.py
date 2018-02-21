import discord
import re
from discord.ext import commands


class Event:
    members = []
    memberCount = 0
    time = ''
    date = ''

    def __init__(self, time, date):
        self.time = time
        self.date = date

    @staticmethod
    def add_member(member: discord.Member):
        global members, memberCount
        members[memberCount] = member


commandPrefix = "#"
botToken = 'NDAyOTAwNDAzMjAyODE4MDU5.DT_eAg._DPd4PFnl2cbZIS1mJ5CzzebAMI'
botID = '402900403202818059'
defaultChannelID = '402909305369788450'
roles = []
guildID = '402909305369788447'
copy = False
events = []

bot = commands.Bot(command_prefix=commandPrefix, description='description')


@bot.command()
async def ping():
    await bot.say('pong!')


@bot.event
async def on_ready():
    print('Logged in as: ')
    print(bot.user.name)
    server = bot.get_server(guildID)
    global roles
    roles = server.roles


@bot.event
async def on_member_join(member: discord.Member):
    await bot.send_message(bot.get_channel(defaultChannelID), 'Welcome %s to the server' % member.name)
    await bot.add_roles(member, find_role("Role"))


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
    global copy
    author = msg.author
    if copy:  # if copying is enabled
        if msg.content != '' and msg.content[:1] != commandPrefix:
            if author.id != botID:
                await bot.send_message(msg.channel, content=msg.content)


@bot.command()
async def hello():
    """Description of command here"""
    await bot.say('Hello!')


@bot.command(pass_context=True)
async def say(ctx, *, something):
    await bot.say(something)
    await bot.delete_message(ctx.message)


@bot.command()
async def roles():
    for role in roles:
        await bot.say(role.name)


@bot.command()
async def new_event(time, date):
    global events
    date_format = re.compile(r'\d\d/\d\d/\d\d\d\d')  # equivalent to the date format mm/dd/yyyy
    time_format = re.compile(r'\d\d:\d\d\w\w')  # equivalent to the time format of hh:mm AM/PM

    if time is None or not time_format.match(time):
        await bot.say("Please input a time in the following format: hh:mmAM/PM")
    else:
        await bot.say("No time issues")

    if date is None or not date_format.match(date):
        await bot.say("Please input a date in the following format: mm/dd/yyyy")
    else:
        await bot.say("No date issues")

    event = Event(time, date)
    events.append(event)


@bot.command(pass_context=True)
async def rsvp(ctx, date):
    global events
    msg = ctx.message
    member = msg.author
    for x in range(len(events)):
        if events[x].date == date:
            events[x].add_member(member)
            display = '```\n'


@bot.command()
async def copy_toggle():
    """Toggles the bot copying everything you say, disabled by default"""
    global copy
    if copy:
        copy = False
    elif not copy:
        copy = True


def find_role(name):
    for role in roles:
        if role.name == name:
            return role
    return


bot.run(botToken)

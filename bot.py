import os
import discord
import discord.utils
import urllib.request, json
import asyncio
import json
import logging

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = '42ctf'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

db_file = open('members.json', 'r')
users = json.load(db_file)
db_file.close()

logging.basicConfig(filename='bot.log', format='%(asctime)s %(message)s', level=logging.INFO)

guild = ''
roles = {}

def get_rank(token):
    url = urllib.request.urlopen("https://www.42ctf.org/accounts/rank/" + token)
    data = json.loads(url.read().decode())
    rank = data['rank']
    return rank

async def watch_roles():
    global users
    await client.wait_until_ready() # ensures cache is loaded
    while not client.is_closed():
        for member_id, token in users.items():
            if (token == "0000"):
                continue
            member = discord.utils.get(guild.members, id=int(member_id))
            rank = get_rank(token)
            if rank == 1 and roles['top1'] not in member.roles:
                await member.add_roles(roles['top1'])
                await member.remove_roles(roles['top10'])
                await member.remove_roles(roles['top50'])
            elif rank > 1 and rank <= 10 and roles['top10'] not in member.roles:
                await member.add_roles(roles['top10'])
                await member.remove_roles(roles['top1'])
                await member.remove_roles(roles['top50'])
            elif rank > 10 and rank <= 50 and roles['top50'] not in member.roles:
                await member.add_roles(roles['top50'])
                await member.remove_roles(roles['top10'])
                await member.remove_roles(roles['top1'])
            elif rank > 50:
                await member.remove_roles(roles['top1'])
                await member.remove_roles(roles['top10'])
                await member.remove_roles(roles['top50'])
        await asyncio.sleep(60)

@client.event
async def on_ready():
    global guild, roles
    guild = discord.utils.get(client.guilds, name=GUILD)
    roles['top10'] = discord.utils.get(guild.roles, id=801787467064672286)
    roles['top1'] = discord.utils.get(guild.roles, id=798638767359524875)
    roles['top50'] = discord.utils.get(guild.roles, id=803729539145924649)

    logging.info('%s is connected to the following guild: %s(id: %d)', client.user, guild.name, guild.id)
    client.loop.create_task(watch_roles())

@client.event
async def on_message(message):
    global guild, roles

    if message.author == client.user:
        return

    if '!connect' in message.content:
        try:
            user_token = message.content.split(' ')[1]
            member = discord.utils.get(guild.members, name=message.author.name)
            rank = get_rank(user_token)
            users[str(member.id)] = user_token
            logging.info("MESSAGE: from %s with token %s", message.author.name, user_token)
            with open('members.json', 'w') as json_file:
                json.dump(users, json_file)
            if rank == 1:
                await member.add_roles(roles['top1'])
                response = "Congratulations, you're now Top 1. But for how long ?"
            
            elif (rank <= 10):
                await member.add_roles(roles['top10'])
                response = "You've been granted the Top 10 role. Now, go away and flag !"
            
            elif rank <= 50:
                await member.add_roles(roles['top50'])
                response = "You've been granted the Top 50 role. Now, go away and flag !"

            else:
                response = "No role for you now, but I'll keep watching you."
        except IndexError:
            response = 'usage: !connect 42ctf_token'
        await message.author.create_dm()
        await message.author.dm_channel.send(response)


client.run(TOKEN)
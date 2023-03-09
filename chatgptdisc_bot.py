## Jonathan Vazquez
## chatgptdisc_bot.py
##
## Desc: main code to set up bot


import discord
import responses

import api_control


async def work_on_message(message, user_message, username, ctrl, is_private):
    try:
        response = responses.parse(username, user_message, ctrl)

        ## Bot was called for so respond appropriately
        if ( response != None):
            await message.author.send(response) if is_private else await message.channel.send(response)
            print('Gave user: '+username+' their pscyh eval')
        ## Bot was not called so just go save message
        ## Only save relatively long messages because most of the time its either @'s or 2 word messages
        elif( len(user_message) > 16):
            ctrl.db.add_message(username, user_message)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTA1MDQ1MzMwOTU5MDM0MzcwMQ.GSrG6x.otYnYqzv2bpzZkSODMF97i_JXu87SSVKTmj4Do'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    my_ctrl = api_control.API_Control()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        ## Do not have bot work on it's own messages or other bots in server
        if message.author == client.user or message.author.bot:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await work_on_message(message, user_message, username, my_ctrl, is_private=True)
        else:
            await work_on_message(message, user_message, username, my_ctrl, is_private=False)

    client.run(TOKEN)

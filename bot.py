import discord

with open('secret.txt', 'r') as f:
    secret = f.read()
if f is None:
    raise EnvironmentError('secret.txt may not exist or has been corrupted!')

client = discord.Client()

command_prefix = "%"

commands = {}

monitored_messages = {}

combos = {}

@client.event
async def on_ready():
    print("Logged in!")

@client.event
async def on_message(message: discord.Message):
    if message.content[0] == command_prefix:
        #Get first word of command minus the command_prefix
        command = message.content[len(command_prefix):].split(' ')[0]
        try:
            await commands[command](message)
        except KeyError:
            print(command, "is not a valid command!")

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    try:
        author_id, combo_name, reply = monitored_messages[payload.message_id]
        if author_id == payload.user_id:
            combos[combo_name].append(payload.emoji)
    except KeyError:
        pass



def make_command(func):
    global commands
    
    commands[func.__name__] = func

    return None

def get_fields(message: discord.Message):
    content = message.content
    return content.split(' ')[1:]

@make_command
async def make_combo(message: discord.Message):
    try:
        combo_name = get_fields(message)[0]
    except IndexError:
        await message.reply(content="You must specify a name for your combo (which must contain no spaces)")
        return

    reply = await message.reply(content='React to this message to build your combo! Reply to this message with ' + \
        command_prefix + 'done to finish the combo')

    author_id = message.author.id
    reply_id = reply.id
        
    combos[combo_name] = []

    monitored_messages[reply_id] = (author_id, combo_name, reply)

@make_command
async def done(message: discord.Message):
    referenced_message: discord.Message = message.reference.resolved
    if referenced_message.id in monitored_messages.keys():
        await referenced_message.delete()
        del monitored_messages[referenced_message.id]
    print('Combo Finalized!')

@make_command
async def combo(message: discord.Message):
    try:
        combo_emojis = combos[get_fields(message)[0]]
        message_to_combo: discord.Message = message.reference.resolved
        if message_to_combo is None:
            return
        for emoji in combo_emojis:
            await message_to_combo.add_reaction(emoji)
    except KeyError:
        message.reply(content='You must give a valid combo name!')

client.run(secret)
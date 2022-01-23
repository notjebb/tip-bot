from discord.ext import commands
import discord
import os, database_functions, tips, wallet
from dotenv import load_dotenv

load_dotenv()

bot_intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=bot_intents)

supported_tokens = ['ftm']

db = database_functions.init_db()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(bot.guilds)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Facilitating your Tips"))

@bot.event
async def on_guild_join(guild): #when the bot joins a new server, this is invoked 
    print("we joined a server!\n")
    print(f"{guild.id=}\t{guild.name=}\n")
    print(f"the member list is:\n")
    id_list = []
    for member in guild.members:
        if member.bot:
            continue
        id_list.append(member.id)
        # print(f"{member.id}\t{member.name} #{member.discriminator}")
        # print(type(member.id))
    #create wallets for new server
    wallet.on_join_wallet_create(id_list, db)
    print("\n")

    #want to create wallet for all the IDs that are not currently in the DB
    #(OPTIONAL) store the IDs and member info in a separate table for whatever reason

@bot.event
async def on_member_join(member): #when someone joins the server, this is invoked
    if not member.bot:
        print("someone new has joined the server! Checking if they need a wallet created!\n")
        wallet.on_user_join_wallet_create(member.id, db)
        print("\n")
    else:
        print("we won't make wallets for bots")


@bot.command()
async def tip(context, payee:discord.Member, amount:float, token:str):
    #check if token type is supported
    print(f"{token=}")
    if payee.bot:
        await context.send(f"You cannot tip a bot")
        return
    if amount <= 0:
        await context.send(f"Please don't be so stingy")
        return
    token=token.lower()
    if token not in supported_tokens:
        await context.send(f"No support {token.upper()}, yet")
        return
    
    #token is supported, check 
    

    #if payee is not a Mention (in the same server), bot will error out - handle it as an event
    #check that the token is supported
    sender, receiver = context.author.id, payee.id

    #check the author has enough $$$ for tipping, and gas, if not, insufficient funds embed
    sender_acc, receiver_acc = wallet.get_account(sender, db), wallet.get_account(receiver, db)

    print(f"{sender_acc.address=}, {sender_acc.address=}")

    #check the receiver's existence in DB (optional)
    # receiver_addr = wallet.get_key_from_id(receiver, db)

    #fetch related addressess / invoke the send
    tx_hash = tips.send(receiver_acc, sender_acc, amount) #need to add amount and token for this

    await context.send(tx_hash)

#balance
@bot.command()
async def balance(context, token='ftm'):
    # 
    user_account = wallet.get_account(context.author.id, db)
    #ftm balance
    balance = wallet.get_ftm_balance(user_account.address)
    
    await context.send(f"{balance=} and {user_account.address=}")
    
#withdraw

#deposit

#help

bot.run(os.getenv('BOT_TOKEN'))
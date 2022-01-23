from discord.ext import commands
import discord
import os, database_functions, tip
from dotenv import load_dotenv

load_dotenv()

bot_intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=bot_intents)

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
    for member in guild.members:
        if member.bot:
            continue
        print(f"{member.id}\t{member.name} #{member.discriminator}")
    print("\n")

    #want to create wallet for all the IDs that are not currently in the DB
    #(OPTIONAL) store the IDs and member info in a separate table for whatever reason


@bot.command()
async def tip(context, payee:discord.Member, amount:int, token:str):
    #if payee is not a Mention (in the same server), bot will error out - handle it as an event
    #check that the token is supported
    sender, receiver = context.author.id, payee.id
    #check the author has enough $$$ for tipping, and gas, if not, insufficient funds embed
    sender_query = database_functions.get_user_db(sender,db)
    sender_addr = sender_query[0][1]
    #check the receiver's existence in DB (optional)
    receiver_query = database_functions.get_user_db(receiver,db)
    receiver_addr = receiver_query[0][1]
    #fetch related addressess / invoke the send
    tx_hash = tip.send(receiver_addr, sender_addr) #need to add amount and token for this

    await context.send(payee)

#withdraw

#deposit

#help



bot.run(os.getenv('BOT_TOKEN'))
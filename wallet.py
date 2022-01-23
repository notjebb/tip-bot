from web3 import Web3
from eth_account import Account
from dotenv import dotenv_values
import secrets, sys
import database_functions
import requests

#need to consider circular import issues
config = dotenv_values(".env")

w3 = Web3(Web3.HTTPProvider(config['FTM_TESTNET_RPC']))

if not w3.isConnected():
    sys.exit("Connection Failed")

def create_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    print ("SAVE BUT DO NOT SHARE THIS (PRIVATE KEY):", private_key)
    acct = Account.from_key(private_key)
    print("Address:", acct.address)
    return (private_key, acct.address)

def get_public_key(priv_key):
    return Account.from_key(str(priv_key))

def get_account(id,db):
    query = database_functions.get_user_db(id,db)
    priv = query[1]
    return Account.from_key(priv)


#ftm
# def get_both_keys_from_id(id, db):
#     query = database_functions.get_user_db(id,db)
#     priv = query[0][1]
#     acc = get_public_key(priv)
#     addr = acc.address
#     return addr, priv

# def get_key_from_id(id, db):
#     query = database_functions.get_user_db(id,db)
#     priv = query[0][1]
#     acc = get_public_key(priv)
#     addr = acc.address
#     return addr

def get_ftm_balance(public_addr):
    #https://api-testnet.ftmscan.com/api?module=account&action=balance&address=0x33e0e07ca86c869ade3fc9de9126f6c73dad105e&tag=latest&apikey=YourApiKeyToken
    req = requests.get(f"https://api-testnet.ftmscan.com/api?module=account&action=balance&address={public_addr}&tag=latest&apikey={config['API_KEY']}")
    bal = req.json()['result']
    
    return int(bal)/1000000000000000000

def on_join_wallet_create(user_id_list, db):
    new_wallets = {}
    for guild_member in user_id_list:
        #if an ID in the server member list does not already have a wallet in the DB
        if not database_functions.get_user_db(guild_member, db):
            #create a wallet for them
            (priv_key, pub_key) = create_wallet()
            #insert ID (key) and Priv_key(value) in DB
            database_functions.add_user_db(guild_member, priv_key, db)
            new_wallets[str(guild_member)] = priv_key
        
    print(f"On-join wallet creation completed")
    print(f"There were {len(new_wallets)} new wallets")
    print(new_wallets)
    print(f"The DB now (test phase only):")
    print(database_functions.get_all_user(db))
            


# db = database_functions.init_db()
# print(database_functions.get_user_db(str(546308542223613953), db))
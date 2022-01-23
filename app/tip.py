from web3 import Web3
from eth_account import Account
import sys
from dotenv import dotenv_values

config = dotenv_values("../.env")

w3 = Web3(Web3.HTTPProvider(config['FTM_TESTNET_RPC']))

if not w3.isConnected():
    sys.exit("Connection Failed")

def sendFtm(toAddr, fromAddr, amount):
    tx = {
        'to': Web3.toChecksumAddress(toAddr), 
        'value':w3.toWei(str(amount),'eth'),
        'gas':80000, # gas limit 80,000
        'gasPrice': w3.toWei('200','gwei'),
        'nonce': w3.eth.getTransactionCount(fromAddr),
        'chainId': 0xfa2,
        }

    key = config[fromAddr]

    signed_tx = w3.eth.account.sign_transaction(tx, key)
    print(f"{signed_tx.rawTransaction=}")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"{tx_hash=}")

# send("0xF34C08F465F1A146ba07eC46BAbAbce8b3D0b621", "0x61178E17Fac681a16eF47ed4B3527B95357b7D09")
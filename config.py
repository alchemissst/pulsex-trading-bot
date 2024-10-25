from db import Database
from getpass import getpass
from web3 import Web3

class Connect:
    def __init__(self):
        # Update to the latest Testnet V4 RPC URL
        pls = "https://rpc.v4.testnet.pulsechain.com"
        self.web3 = Web3(Web3.HTTPProvider(pls))
        self.db = Database()

    def make_connection(self):
        address = self.db.get_address()
        if address:
            addr = address[0]
        else:
            print("Can't find active address at database, insert your PLS address here...")
            while True:
                addr = input('Address: ')
                key = getpass('Key: ')
                try:
                    self.web3.eth.get_balance(addr)
                except Exception as e:
                    print("Can't connect to blockchain:", e, ", check if address and network is correct")
                else:
                    self.db.store_address(addr, key)
                    break
        return addr


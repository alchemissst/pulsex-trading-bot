from config import Connect
from gecko import Gecko
from web3 import Web3
from db import Database
import requests
import json
import time
import sys
import subprocess
from datetime import datetime

class Main:
    def __init__(self):
        self.connection = Connect()
        self.db = Database()
        self.gecko = Gecko()
        self.connection.make_connection()
        
        # Updated to use PulseChain Testnet V4 RPC URL
        self.web3 = Web3(Web3.HTTPProvider('https://rpc.v4.testnet.pulsechain.com'))
        
        # Launch trade.py as a subprocess
        subprocess.Popen('start /wait python trade.py', shell=True)
        self.menu()

    def get_bnb_balance(self):
        # Updated terminology to reflect WPLS instead of BNB
        balance = self.web3.eth.get_balance(self.db.get_address()[0])
        return self.web3.from_wei(balance, 'ether')

    def get_wbnb_balance(self):
        # Update with WPLS contract address on PulseChain if needed
        wbnb_contract = self.web3.to_checksum_address("0xa68462c5a23b5cbb5d8750d802cb6a1aa17839a0")  # Example address
        contract = self.web3.eth.contract(address=wbnb_contract, abi=json.loads('[{"constant":true,"inputs":[],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'))
        return self.web3.from_wei(contract.functions.balanceOf(self.db.get_address()[0]).call(), 'ether')

    def menu(self):
        while True:
            print("\n\n-- Menu --")
            print("1. Create Trade")
            print("2. Show Trades")
            print("3. Modify Address")
            print("4. Exit")
            option = input("Choose an option: ")
            
            if option == '1':
                self.create_trade()
            elif option == '2':
                self.show_trades()
            elif option == '3':
                self.change_address()
            elif option == '4':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid option. Please choose again.")

    def create_trade(self):
        name = input('Name: ')
        contract_addr = input('Contract: ')
        trade_amount = input('Amount: ')
        trade_method = input('Method: ')
        trade_value = input('Value: ')
        
        # Store trade in the database
        self.db.store_trade(contract_addr, trade_amount, trade_method, trade_value, name)
        print("Trade created.")

    def show_trades(self):
        print("Trades:")
        trades = self.db.get_all_trades()
        for trade in trades:
            print(trade)
        
        print("\nPast Trades:")
        past_trades = self.db.get_all_past_trades()
        for past_trade in past_trades:
            print(past_trade)
        
        delete = input("\nWould you like to delete a trade? (yes/no): ").lower()
        if delete == 'yes':
            contract = input("Enter contract of trade to delete: ")
            self.db.delete_trade(contract)
            print("Trade deleted.")

    def change_address(self):
        print("Change Active Address")
        new_addr = input("Enter new address: ")
        new_key = input("Enter new private key: ")
        
        # Update address in the database
        self.db.store_address(new_addr, new_key)
        print("Address updated.")

if __name__ == "__main__":
    Main()



from web3 import Web3
import requests
from datetime import datetime

class blkchn:
    def __init__(self):
        # Replace with your Ethereum address and Etherscan API key
        self.etherscan_api_key = "IXSWKR7F7E7R49I82SYNB2TKV85EKT8ZQ3"
        self.address = "0x8821A05725d87e454c2da38bF95a0961E806a18c"

        # Connect to Ethereum node
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/eee3c35d22184a2eb3b92beb56f85c79'))

        # Check connection
        if self.web3.is_connected():
            print("Connected to Ethereum")
        else:
            print("Connection failed")
        pass
        self.get_eth_usd_price()


    def get_transactions_by_type(self, type):

        # Etherscan API endpoint
        self.url_etherscan = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": type,
            "address": self.address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",  # Use asc/desc  
            "apikey": self.etherscan_api_key
        }
        tx_list_tmp=[]
        response = requests.get(self.url_etherscan, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "1":  # Check if the request was successful
                tx_list_tmp=data["result"]
            else:
                print(f"No transactions found or error: {data['message']}")
        else:
            print("Failed to connect to Etherscan API")
        return tx_list_tmp

    def get_eth_usd_price(self):
        # Use an API to get the current Ethereum price in USD
        url_coingecko = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "ethereum", "vs_currencies": "usd"}
        
        response = requests.get(url_coingecko, params=params)
        if response.status_code == 200:
            data = response.json()
            self.eth_usd_price = data['ethereum']['usd']
        else:
            raise Exception("Failed to fetch Ethereum price from API "+str(response.status_code))    

    def get_ether_and_usd_value(self,web3, value):
        value_ether = web3.from_wei(value, 'ether')
        value_usd = float(value_ether) * self.eth_usd_price
        return value_ether, value_usd


    def list(self):
        tx_list=[]
        tx_list += self.get_transactions_by_type( "txlist")
        tx_list += self.get_transactions_by_type( "txlistinternal")
        if tx_list:
            for tx in tx_list[:100]:  # Limit to  100 transactions
                tx_datetime = datetime.fromtimestamp( int(tx["timeStamp"]))
                value_ether, value_usd = self.get_ether_and_usd_value(self.web3, int(tx["value"]))
                gas_ether, gas_usd = self.get_ether_and_usd_value(self.web3, int(tx["gasUsed"]))
                print()
                print(f"===From: {tx['from']} To: {tx['to']}  date {tx_datetime}")
                print(f"   Value: {value_ether}  Value_usd: {value_usd}  ")
                print(f"   GAS: {gas_ether:.20f}  GAS_usd: {gas_usd:.20f}  ")
        else:
            print("No transactions to display.")


b1=blkchn()
b1.list()

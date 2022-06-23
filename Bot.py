from web3 import Web3
INFURA_KEY = "b9b9ad2a7f9a4b41bab9669cd7ed8fa2"
ETHERSCAN_API_KEY = "NMTJEE6UCFJKN7KGJXZFWP9YGYQ4TMYERF"
CONTRACT_ADDRESS = ""
etherscan_url = ""
INFURIA_END_POINT = "https://mainnet.infura.io/v3/27a390ceab06499890c6a890e6c6415a"
INFURIA_WEB_SOCKET = "wss://mainnet.infura.io/ws/v3/27a390ceab06499890c6a890e6c6415a"
ftmscan_url = f"http://api.etherscan.io/api?module=contract&action=getabi&address=${CONTRACT_ADDRESS}&apikey=${ETHERSCAN_API_KEY}"
w3 = Web3(Web3.HTTPProvider(INFURIA_END_POINT))
print(w3.eth.get_block('latest'))
print(w3.isConnected())

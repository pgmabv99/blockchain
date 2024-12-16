from web3 import Web3
from solcx import compile_standard

# Connect to Ethereum (Infura, local node, etc.)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Solidity code for a simple contract
solidity_code = """
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 public storedData;

    function set(uint256 x) public {
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
"""

# Compile contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "SimpleStorage.sol": {
            "content": solidity_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# Get ABI and Bytecode
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# Set up account and private key
from_account = '0xYourEthereumAddress'
private_key = '0xYourPrivateKey'

# Build the contract instance
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce
nonce = w3.eth.getTransactionCount(from_account)

# Build transaction
transaction = SimpleStorage.constructor().buildTransaction({
    'chainId': 1,
    'gas': 2000000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': nonce,
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Transaction sent, hash: {txn_hash.hex()}")

# Wait for the transaction receipt
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
print(f"Contract deployed at address: {txn_receipt.contractAddress}")

# Increment nonce for the next deployment
nonce += 1

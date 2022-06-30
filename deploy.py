from solcx import compile_standard, install_solc
import json
from web3 import Web3
from web3.auto import w3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# complie solidity
print("installing...")
install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode(walking down the compiled_code.json)
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
#abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

unicorns = w3.eth.contract(address="0x4EB80695CeA632d3389385B2a182944B758e1822", abi=abi)

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_Id = 5777
my_address = "0x4EB80695CeA632d3389385B2a182944B758e1822"
#private_key = os.getenv("PRIVATE_KEY")
private_key="0xac73576585662576b8b64ad0c46427477e1fd8ce1ffa888f893283f9b0b4c54a"

# create the contract in py
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build a transaction
# 2. sign it
# 3. send it
transaction = SimpleStorage.constructor().buildTransaction
(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_Id,
        "from": my_address,
        "nonce": nonce,
    }
)

#sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
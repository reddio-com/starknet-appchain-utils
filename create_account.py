import json
import time
import requests

from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.hash.address import compute_address
from starknet_py.net.signer.stark_curve_signer import KeyPair

from settings import NODE_URL, CHAIN_ID, ARGENT_CLASS_HASH

# Please modify it to your own private key and salt
PRIVATE_KEY = 0x1234567890123456789012345678901234567890123456789012345678901234
salt = 0x1234567890123456789012345678901234567890123456789012345678901234


def create_argent_account(private_key = PRIVATE_KEY,  class_hash = ARGENT_CLASS_HASH, salt = salt):
    key_pair = KeyPair.from_private_key(private_key)
    constructor_args = [key_pair.public_key,0x0]

    # Compute an address
    address = compute_address(
        salt=salt,
        class_hash=class_hash,  # class_hash of the Account declared on the Starknet
        constructor_calldata=constructor_args,
    )

    print("deploy address will be",hex(address), "please prefund it with eth")

    # Note: add your own code to prefund ETH to the address, you may want to sleep for sometime


    account_deployment_result = Account.deploy_account_sync(
        address=address,
        class_hash=class_hash,
        salt=salt,
        key_pair=key_pair,
        client=FullNodeClient(node_url=NODE_URL),
        chain=CHAIN_ID,
        constructor_calldata=constructor_args,
        max_fee=int(1e17),
    )

    # Wait for deployment transaction to be accepted
    account_deployment_result.wait_for_acceptance_sync()
    # From now on, account can be used as usual
    account = account_deployment_result.account
    return account.address

if __name__ == "__main__":
    print(create_argent_account())
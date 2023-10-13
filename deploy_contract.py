from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair

from settings import NODE_URL, CHAIN_ID

def deploy_with_account(private_key, aa_address, class_file="cool_sierra_contract_class.json", casm_file="cool_compiled_class.casm"):
    account = Account(
        client=FullNodeClient(node_url=NODE_URL),
        address=aa_address,
        key_pair=KeyPair.from_private_key(key=private_key),
        chain=CHAIN_ID,
    )
    declare_result = Contract.declare_sync(
        account=account,
        compiled_contract=Path(class_file).read_text(),
        compiled_contract_casm=Path(casm_file).read_text(),
        max_fee=int(1e16),
    )
    declare_result.wait_for_acceptance_sync()

    print("class hash", hex(declare_result.class_hash))

    deploy_result = declare_result.deploy_sync(
        max_fee=int(1e16)
    )
    deploy_result.wait_for_acceptance_sync()

    contract = deploy_result.deployed_contract
    print("contract address", hex(contract.address))
    return hex(declare_result.class_hash), hex(contract.address)

if __name__ == "__main__":
    deploy_with_account(YourPrivateKey, YourAccountAddress)
from starknet_py.contract import Contract
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair


from abi import ERC20_abi
from settings import NODE_URL, CHAIN_ID, ETH_ADDRESS


class Starknet(object):
    def __init__(self):
        self._client = FullNodeClient(node_url=NODE_URL)
        self._eth_contract = Contract(
            address=ETH_ADDRESS,
            provider=self._client,
            cairo_version= 0,
            abi = ERC20_abi,
        )

    def transfer_eth_by_account(self, private_key, aa_address,  recipient, amount):
        client = FullNodeClient(node_url=NODE_URL)
        account = Account(
            client=client,
            address=aa_address,
            key_pair=KeyPair.from_private_key(key=private_key),
            chain=CHAIN_ID,
        ) 

        calls = [
            self._eth_contract.functions["transfer"].prepare(recipient, amount),
        ]

        transaction_response = account.execute_sync(calls=calls, max_fee=int(1e16), cairo_version= 1)
        tx = hex(transaction_response.transaction_hash)
        receipt = client.wait_for_tx_sync(tx)
        print(tx, receipt.execution_status)
        balance = self.get_eth_balance(recipient)
        print("balance", balance)
    
    def get_eth_balance(self, address):
        eth_balance = self._eth_contract.functions["balanceOf"].call_sync(address)[0]
        return eth_balance
    
    def get_receipt(self, tx):
        receipt = self._client.get_transaction_receipt_sync(tx)
        return receipt

if __name__ == "__main__":
    s = Starknet()
    # print(s.get_eth_balance(0x234acc3c3c30c4c427e30f61ae47184fd7cf8c4f81859e73f6f2af41e6b81c5))
    print(s.get_receipt(0x07814c04dc7a241b6cad891d2fba9c3889095903ec83a228ccefda81acc1d934))
from starknet_py.net.full_node_client import FullNodeClient

from settings import NODE_URL

def get_receipt(tx):
    client = FullNodeClient(node_url=NODE_URL)
    receipt = client.get_transaction_receipt_sync(tx)
    return receipt

if __name__ == "__main__":
    print(get_receipt(0x07814c04dc7a241b6cad891d2fba9c3889095903ec83a228ccefda81acc1d934))
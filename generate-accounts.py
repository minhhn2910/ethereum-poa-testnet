import json
import argparse
from eth_account import Account

def generate_eth_accounts(num_accounts, output_file, input_genesis_file, output_genesis_file):
    accounts = []
    for _ in range(num_accounts):
        acct = Account.create()
        accounts.append({
            'address': acct.address,
            'private_key': acct.key.hex()
        })

    with open(output_file, 'w') as file:
        json.dump(accounts, file, indent=4)

    if input_genesis_file != 'NA':
        with open(input_genesis_file, 'r') as file:
            genesis = json.load(file)
            for account in accounts:
                genesis['alloc'][account['address']] = {'balance': '10000000000000000000000000'}

            with open(output_genesis_file, 'w') as out_file:
                json.dump(genesis, out_file, indent=2)

    return f"{num_accounts} Ethereum accounts have been generated and stored in {output_file}"


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Ethereum accounts.')
    parser.add_argument('--num-accounts', type=int, default=1, help='Number of accounts to generate')
    parser.add_argument('--output-file', type=str, default='eth_accounts.json', help='Output file for accounts')
    parser.add_argument('--input-genesis-file', type=str, default='NA', help='Output file for genesis')
    parser.add_argument('--output-genesis-file', type=str, default='genesis.json', help='Output file for genesis')

    args = parser.parse_args()
    result = generate_eth_accounts(args.num_accounts, args.output_file , args.input_genesis_file, args.output_genesis_file)
    print(result)
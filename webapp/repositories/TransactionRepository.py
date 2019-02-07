import binascii

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from webapp.models import Transaction
from solc import compile_source
from smartContract.settings import ETH_PROVIDER


class TransactionList(LoginRequiredMixin, ListView):
    login_url = 'account_login'
    model = Transaction


class TransactionCreate(LoginRequiredMixin, CreateView):
    login_url = 'account_login'
    model = Transaction
    fields = ['timestamp']

    def persist_transaction_to_blockchain(sender, **kwargs):
        transaction = kwargs["instance"]

        if kwargs["created"]:
            eth_provider = ETH_PROVIDER
            eth_provider.defaultAccount = transaction.fr.address

            transaction_details = {
                'from': eth_provider.defaultAccount,
                'value': 0,
                "gasLimit": 0,
                "gasPrice": 0
            }

            with open('webapp/contracts/greeter.sol') as file:
                source_code = file.readlines()

            compiled_sol = compile_source(''.join(source_code), import_remappings=['=/', '-'])

            contract_interface = compiled_sol['<stdin>:Greeter']

            # Instantiate and deploy contract
            contract_factory = eth_provider.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])



            contract_constructor = contract_factory.constructor()

            # Submit the transaction that deploys the contract

            transaction_hash_ascii = contract_constructor.transact(transaction_details)

            transaction_hash = transaction_hash_ascii.hex()

            # Wait for the transaction to be mined, and get the transaction receipt
            print('Tx of a transaction {}', transaction_hash)

            transaction_receipt = eth_provider.waitForTransactionReceipt(transaction_hash, 240)

            print('transaction_receipt ', transaction_receipt)
            print('gas Used ', transaction_receipt['gasUsed'])

            # Create the contract instance with the newly-deployed address
            greeter = eth_provider.contract(
                address=transaction_receipt['contractAddress'],
                abi=contract_interface['abi'])

            print(greeter.functions.greet().estimateGas(), " estimation of greet method")

            # Display the default greeting from the contract
            print('Default contract greeting: {}'.format(
                greeter.functions.greet().call()
            ))
            transaction.txHash = transaction_hash
            transaction.contract_address = transaction_receipt['contractAddress']
            transaction.gasUsedByTxn = transaction_receipt['gasUsed']
            transaction.save()

    post_save.connect(persist_transaction_to_blockchain, sender=Transaction)


class TransactionDetail(LoginRequiredMixin, DetailView):
    login_url = 'account_login'
    model = Transaction
    fields = '__all__'

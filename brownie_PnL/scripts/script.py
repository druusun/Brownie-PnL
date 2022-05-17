from web3 import Web3
from brownie import Contract, network
import os

# Gets an address balance for native chain token (gets eth for Arbitrum;
# Set API and address as variable strings before inputting
def nativetokenbalance(API, address):
    node = Web3(Web3.HTTPProvider(API))
    balance = node.eth.get_balance(Web3.toChecksumAddress(address)) / 10 ** 18
    return balance


# Gets an address balance for native chain token in USD
# Set CLaddress and CLabi as variable strings before inputting
def nativetokenbalance_usd(
    API,
    address,
    CLaddress,
    CLabi,
):
    node = Web3(Web3.HTTPProvider(API))
    balance = nativetokenbalance(API, address)
    CLcontract = node.eth.contract(address=Web3.toChecksumAddress(CLaddress), abi=CLabi)
    CLexchangerate = CLcontract.functions.latestRoundData().call()[1] / 10 ** 8
    balanceusd = balance * CLexchangerate
    return balanceusd


# Gets an address balance for ERC20 token
# ^^
def ERC20balance(tokenaddress, address):
    VanBeet = Web3.toChecksumAddress(address)
    Erc20 = Contract.from_explorer(Web3.toChecksumAddress(tokenaddress))
    return Erc20.balanceOf(VanBeet) / 10 ** 18


# Gets an address balance in usd for ERC20 token
# ^^
def ERC20balance_usd(tokenaddress, address):
    balance = ERC20balance(tokenaddress, address)
    FXrate = Contract.from_explorer(Web3.toChecksumAddress(tokenaddress))
    return balance*FXrate.getTokenPriceSource()/10**8



# Calculates ETH collateral Vaults (Works for QiDAO, not sure about others) Collateral, Debt, and Collateral to Debt Ratio (all usd)
# ^^USE *Web3.toChecksumAddress.()* for vaultaddress!
def VaultCollateral(API, vaultaddress, vaultabi, vaultID) -> float:
    node = Web3(Web3.HTTPProvider(API))
    vaultcontract = node.eth.contract(
        address=Web3.toChecksumAddress(vaultaddress), abi=vaultabi
    )
    collateral = float(
        (
            vaultcontract.functions.vaultCollateral(vaultID).call()
            * vaultcontract.functions.getEthPriceSource().call()
        )
        / 10 ** 26
    )
    return collateral


def VaultDebt(API, vaultaddress, vaultabi, vaultID) -> float:
    node = Web3(Web3.HTTPProvider(API))
    vaultcontract = node.eth.contract(
        address=Web3.toChecksumAddress(vaultaddress), abi=vaultabi
    )
    debt = float(
        (
            vaultcontract.functions.vaultDebt(vaultID).call()
            * vaultcontract.functions.getTokenPriceSource().call()
        )
        / 10 ** 26
    )
    return debt


def VaultRatio(API, vaultaddress, vaultabi, vaultID) -> float:
    collateral = VaultCollateral(API, vaultaddress, vaultabi, vaultID)
    debt = VaultDebt(API, vaultaddress, vaultabi, vaultID)
    ratio = (collateral / debt) * 100
    return ratio

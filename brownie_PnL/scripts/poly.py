from brownie import *
from web3 import Web3
from dotenv import load_dotenv


def main():
    walletAddress = Web3.toChecksumAddress("0xa48c6ac5024051871dbb115f4d5e3dca70be0739")
    MaiAddress = Web3.toChecksumAddress("0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
    Erc20 = Contract.from_explorer(MaiAddress)
    print(Erc20.balanceOf(walletAddress) / 10 ** 18)


# print(ERC20balance(MaiAddress, walletAddress))

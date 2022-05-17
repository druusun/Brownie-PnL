from brownie import Contract, network
from web3 import Web3


VanBeet = Web3.toChecksumAddress("0xa48c6ac5024051871dbb115f4d5e3dca70be0739")
network.connect(network="Eth", launch_rpc=True)
dai = Contract.from_explorer(
    Web3.toChecksumAddress(0x6B175474E89094C44DA98B954EEDEAC495271D0F)
)

print(dai.balanceOf(VanBeet) / 10 ** 18)

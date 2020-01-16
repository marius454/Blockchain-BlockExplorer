from blockchain import blockexplorer as be
from blockchain import util

util.TIMEOUT = 30

def getOldestBlocks():
	blocks = list()
	# blocks.append(be.get_latest_block())
	# latest = vars(blocks[0])['height']
	for i in range(0,10):
		blocks.append(be.get_block(str(i)))
	return blocks

def getBlock(ID):
	return be.get_block(str(ID))

def getLatestBlock():
	return be.get_latest_block()

def getTx(ID):
	return be.get_tx(str(ID))


# print(vars(vars(getBlock(4))['transactions'][0]))
# print(vars(getTx("df2b060fa2e5e9c8ed5eaf6a45c13753ec8c63282b2688322eba40cd98ea067a")))

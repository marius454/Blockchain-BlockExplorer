from django.shortcuts import render
from . import getBlocks as gb
import datetime

# Create your views here.
def block(request):
	blockID = request.GET.get('blockID')
	rawBlock = gb.getBlock(blockID)
	block = vars(rawBlock)
	key = list()
	value = list()
	for var in block:
		if var == 'transactions':
			break
		if var == 'time' or var == 'received_time':
			value.append(datetime.datetime.fromtimestamp(block[var]))
		elif var == 'size':
			value.append(str(block[var]) + ' bytes')
		elif var == 'fee':
			value.append(str(block[var]/1e8) + ' BTC')
		else:
			value.append(block[var])
		key.append(var)
	txs = list()
	for tx in block['transactions']:
		txs.append(vars(tx)['hash'])
	blockInfo = [{'key': t[0], 'value': t[1]} for t in zip(key, value)]
	my_context = {
		"blocks": blockInfo,
		"BlockHash": block['hash'],
		"transactions": txs
		# "previousHash": block['previous_block'],
		# "version": block['version']
	}
	return render(request, 'blocks/block.html', my_context)
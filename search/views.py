from django.http import HttpResponse
from django.shortcuts import render
from . import getBlocks as gb
import datetime

def homepage(request):
	if request.GET.get('blockID'):
		blockID = request.GET.get('blockID')
		block = [gb.getBlock(blockID)]
		blockDict = [{'hash': vars(block[0])['hash'], 'height': vars(block[0])['height']}]
		my_context = {"blocks": block}
		return render(request,'search.html', my_context)


	elif request.GET.get('blockIdStart') and request.GET.get('blockIdEnd'):
		blockIdStart = request.GET.get('blockIdStart')
		blockIdEnd = request.GET.get('blockIdEnd')
		Blocks = list()
		for i in range(int(blockIdStart),int(blockIdEnd)+1):
			Blocks.append(gb.getBlock(i))
		blockHash = list()
		blockHeight = list()
		for i in Blocks:
			blocks = vars(i)
			blockHash.append(blocks['hash'])
			blockHeight.append(blocks['height'])
		block = [{'hash': t[0], 'height': t[1]} for t in zip(blockHash, blockHeight)]
		my_context = {
			"blocks": block
		}
		return render(request,'search.html', my_context)


	elif request.GET.get('txID'):
		txID = request.GET.get('txID')
		tx = [gb.getTx(txID)]
		my_context = {"transactions": tx}
		return render(request,'search.html', my_context)

	else:
		Blocks = gb.getOldestBlocks()
		blockHash = list()
		blockHeight = list()
		for i in Blocks:
			blocks = vars(i)
			blockHash.append(blocks['hash'])
			blockHeight.append(blocks['height'])
		block = [{'hash': t[0], 'height': t[1]} for t in zip(blockHash, blockHeight)]
		my_context = {
			"blocks": block
		}
		return render(request,'search.html', my_context)

def about(request):
	return HttpResponse('about')

def transaction(request):
	txID = request.GET.get('txID')
	rawTx = gb.getTx(txID)
	tx = vars(rawTx)
	key = list()
	value = list()
	for var in tx:
		if var == 'inputs':
			break
		if var == 'time':
			value.append(datetime.datetime.fromtimestamp(tx[var]))
		elif var == 'size':
			value.append(str(tx[var]) + ' bytes')
		else:
			value.append(tx[var])
		key.append(var)
	txInfo = [{'key': t[0], 'value': t[1]} for t in zip(key, value)]

	inAddress = list()
	inValue = list()
	sumIn = 0
	check1 = False
	for var in tx['inputs']:
		if 'address' in vars(var):
			inAddress.append(vars(var)['address'])
			check1 = True
		else:
			inAddress.append("None (Coinbase)")
		if 'value' in vars(var):
			inValue.append(str(vars(var)['value']/1e8) + ' BTC')
			sumIn += vars(var)['value']
		else:
			inValue.append("None")
	inputs = [{'address': t[0], 'value': t[1]} for t in zip(inAddress, inValue)]
	outAddress = list()
	outValue = list()
	sumOut = 0
	check2 = False
	for var in tx['outputs']:
		if 'address' in vars(var):
			outAddress.append(vars(var)['address'])
			check2 = True
		else:
			outAddress.append("None")
		if 'value' in vars(var):
			outValue.append(str(vars(var)['value']/1e8) + ' BTC')
			sumOut += vars(var)['value']
		else:
			outValue.append("None")
	outputs = [{'address': t[0], 'value': t[1]} for t in zip(outAddress, outValue)]
	if check1 and check2:
		fee = sumIn - sumOut
		txInfo.append({'key': "fee", 'value': str(fee/1e8) + ' BTC'})

	my_context = {
		"tx": txInfo,
		"txHash": tx['hash'],
		"inputs": inputs,
		"outputs": outputs
	}
	return render(request,'transactions.html', my_context)
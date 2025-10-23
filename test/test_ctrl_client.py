# encoding: utf-8
# author: GitHub Copilot Agent (GPT-5 mini), Tegredum
# python version: 3.10.16

import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CtrlAlgClient import CtrlAlgClient


def main():
	args: dict = {
		'port': 12346,
		'host': '127.0.0.1'
	}

	with CtrlAlgClient(args['port'], host=args['host']) as client:
		# Test 1: init
		print('\n=== Test 1: send init command ===')
		initParams = {'multiplier': 5}
		print('Sending init params:', json.dumps(initParams, ensure_ascii=False))
		client.sendInitCommand(initParams)
		if client.error_msg:
			print('Server returned error:', client.error_msg)
		else:
			print('Init completed')

		# Test 2: compute
		print('\n=== Test 2: compute (10 * multiplier) ===')
		computeParams = {'value': 10}
		print('Sending compute params:', json.dumps(computeParams, ensure_ascii=False))
		client.sendComputeCommand(computeParams)
		result = client.receiveData()
		if result is not None:
			print('Received compute result:', json.dumps(result, ensure_ascii=False))
		else:
			print('Error: no result. Server message:', client.error_msg)

		# Test 3: re-init
		print('\n=== Test 3: re-init (multiplier=2) ===')
		initParams = {'multiplier': 2}
		print('Sending init params:', json.dumps(initParams, ensure_ascii=False))
		client.sendInitCommand(initParams)
		if client.error_msg:
			print('Server returned error:', client.error_msg)
		else:
			print('Re-init completed')

		# Test 4: compute with new multiplier
		print('\n=== Test 4: compute (7 * multiplier) ===')
		computeParams = {'value': 7}
		print('Sending compute params:', json.dumps(computeParams, ensure_ascii=False))
		client.sendComputeCommand(computeParams)
		result = client.receiveData()
		if result is not None:
			print('Received compute result:', json.dumps(result, ensure_ascii=False))
		else:
			print('Error: no result. Server message:', client.error_msg)


if __name__ == '__main__':
	main()

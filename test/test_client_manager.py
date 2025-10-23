# encoding: utf-8
# author: GitHub Copilot Agent (GPT-5 mini), Tegredum
# python version: 3.10.16
import time
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))	# 添加上级目录到搜索路径，用于调用 AlgClientManager 模块
from AlgClientManager import AlgClientManager

def main():
	args: dict = {
		'port': 12345,
		'host': '127.0.0.1'
	}

	with AlgClientManager(args['port'], host=args['host']) as client:
		for idx in range(1, 4):
			request = {
				'iter': idx,
				'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
				'message': f'Request from iteration {idx}'
			}
			client.sendData(request)
			print('Request sent:', json.dumps(request, ensure_ascii=False))
			reply = client.receiveData()
			print('Reply received:', json.dumps(reply, ensure_ascii=False))
			time.sleep(1)


if __name__ == '__main__':
	main()

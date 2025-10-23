# encoding: utf-8
# author: GitHub Copilot Agent (GPT-5 mini)
# python version: 3.10.16
from typing import Any, Dict
from AlgClientManager import AlgClientManager
import time

class CtrlAlgClient(AlgClientManager):
	"""Control-algorithm client specialized from AlgClientManager.

	Mirrors MATLAB CtrlAlgClient methods:
	- sendInitCommand(params: dict)
	- sendComputeCommand(params: dict)
	- receiveData() -> returns server msg or None

	The client keeps the ability to connect to a specified host via AlgClientManager constructor.
	"""

	def __init__(self, port: int, host: str = '127.0.0.1', timeout: float | None = None):
		super().__init__(port, host=host, timeout=timeout)

	def sendInitCommand(self, params: Dict[str, Any]) -> None:
		msg = {
			'type': 'init',
			'params': params
		}
		self.sendData(msg)
		# small pause to avoid overwhelming server, similar to MATLAB pause(0.1)
		time.sleep(0.1)
		# consume server response to keep buffer clean
		_ = self.receiveData()

	def sendComputeCommand(self, params: Dict[str, Any]) -> None:
		msg = {
			'type': 'compute',
			'params': params
		}
		self.sendData(msg)

	def receiveData(self):
		# call base class receiveData which returns the 'msg' when status == 'ok', or None and sets error_msg
		return super().receiveData()

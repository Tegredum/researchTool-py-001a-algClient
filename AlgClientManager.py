# encoding: utf-8
# author: Tegredum, GitHub Copilot Agent (GPT-5 mini)
# python version: 3.10.16
import socket
import json
import struct
from typing import Optional

class AlgClientManager:
	"""A TCP client that mirrors the MATLAB `AlgClientManager` behavior.

	- Connects to localhost on the given port
	- Sends JSON messages prefixed by a 4-byte big-endian length
	- Receives responses with the same framing and decodes JSON
	- On server error responses (status != 'ok'), stores `error_msg` and returns None
	"""
	def __init__(self, port: int, host: str = '127.0.0.1', timeout: Optional[float] = None):
		self.host = host
		self.port = port
		self.error_msg: Optional[str] = None
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# disable Nagle's algorithm like MATLAB's setTcpNoDelay(true)
		self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		if timeout is not None:
			self._sock.settimeout(timeout)
		self._sock.connect((host, port))

	def sendData(self, data: dict) -> None:
		"""Send a JSON-serializable dict to the server with 4-byte big-endian length prefix."""
		json_str = json.dumps(data, ensure_ascii=False)
		payload = json_str.encode('utf-8')
		length = len(payload)
		header = struct.pack('!I', length)  # network (= big-endian) unsigned int
		self._sock.sendall(header + payload)

	def _recv_exact(self, n: int) -> bytes:
		"""Receive exactly n bytes or raise ConnectionError."""
		buf = bytearray()
		while len(buf) < n:
			chunk = self._sock.recv(n - len(buf))
			if not chunk:
				raise ConnectionError('Socket closed while receiving data')
			buf.extend(chunk)
		return bytes(buf)

	def receiveData(self):
		"""Receive a single framed JSON response from the server.

		Returns the `msg` field when status == 'ok', otherwise sets `self.error_msg` and returns None.
		"""
		# read 4-byte header
		header = self._recv_exact(4)
		length = struct.unpack('!I', header)[0]
		if length == 0:
			return None
		body = self._recv_exact(length)
		try:
			data = json.loads(body.decode('utf-8'))
		except Exception as e:
			raise ValueError(f'Failed to decode JSON: {e}')

		status = data.get('status')
		if status == 'ok':
			return data.get('msg')
		else:
			self.error_msg = data.get('error')
			return None

	def close(self):
		try:
			self._sock.shutdown(socket.SHUT_RDWR)
		except Exception:
			pass
		self._sock.close()

	# context manager support
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc, tb):
		self.close()

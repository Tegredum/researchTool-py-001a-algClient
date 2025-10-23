# Python Client for AlgServerManager

author: GitHub Copilot Agent (GPT-5 mini)

This folder contains a Python reimplementation of the MATLAB `AlgClientManager`.

Files

- `AlgClientManager.py`: TCP client that sends and receives length-prefixed JSON messages (4-byte big-endian length header).
- `test/test_client_manager.py`: Simple test script that sends 3 requests to a server on port 12345 and prints replies.

Usage

1. Start the Python server (from `Server/Server-Python`) in a separate terminal:

   python Server/Server-Python/test/test_server.py

2. Run the client test (from this directory):

   python test/test_client_manager.py

Notes

- The client connects to `127.0.0.1:12345` by default. Change the port in the test script or construct `AlgClientManager` with a different port.
- The framing and JSON format match the MATLAB client implementation so you can test MATLAB client vs Python server or Python client vs MATLAB/Python server.

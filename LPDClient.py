#/usr/bin/env python3

# Simple LPD client suggested by Google AI and tuned by Magnetic-Fox
#
# by Magnetic-Fox, 20.04 - 07.06.2026
#
# (c)2026 Bartłomiej "Magnetic-Fox" Węgrzyn

import socket


TRANSMISSION_OK = 0
ERROR_QUEUE = 1
ERROR_CONTROL_FILE = 2
ERROR_CONTROL_DATA = 3
ERROR_DATA = 4
ERROR_TRANSMISSION = 5


def lpd_print(data, ip, port = 515, queue = "RAW"):
	if isinstance(data, str):
		data = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((ip, port))

		s.sendall(b'\x02' + queue.encode() + b'\n')
		if s.recv(1) != b'\x00':
			return ERROR_QUEUE

		ctrl = f"Hlocalhost\nPuser\nfdfA001localhost\n"
		s.sendall(f"\x02{len(ctrl)} cfA001localhost\n".encode())
		if s.recv(1) != b'\x00':
			return ERROR_CONTROL_FILE

		s.sendall(ctrl.encode() + b'\x00')

		if s.recv(1) != b'\x00':
			return ERROR_CONTROL_DATA

		s.sendall(f"\x03{len(data)} dfA001localhost\n".encode())
		if s.recv(1) != b'\x00':
			return ERROR_DATA

		s.sendall(data + b'\x00')

		if s.recv(1) != b'\x00':
			return ERROR_TRANSMISSION

	return TRANSMISSION_OK

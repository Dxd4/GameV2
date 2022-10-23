import socket, threading
from functools import partial
import tkinter as tk
import time

def send(event,cli_sock):
	if event.char == "w":
			cli_sock.send(b"up")
	elif event.char == "a":
			cli_sock.send(b"left")
	elif event.char == "s":
			cli_sock.send(b"down")
	elif event.char == "d":
			cli_sock.send(b"right")


def visualise(pg_fields):
	width, height = len(pg_fields)-1, len(pg_fields[0])
	window.geometry(f"{width*48}x{height*51}")
	playground = [[0]*width for i in range(height)]
	for x in range(width):
		for y in range(height):
				playground[x][y]= (tk.Label(window,bg=pg_fields[x][y],width=6,height=3))
				playground[x][y].grid(row=x,column=y)

def pg_fields_to_array(pg_fields):
	pg_fields = pg_fields.split(",\n")
	for x in range(len(pg_fields)):
		pg_fields[x] = pg_fields[x].split(",")
	return pg_fields

def receive(cli_sock):
	while True:
		data = cli_sock.recv(1024)
		if data:
			visualise(pg_fields_to_array(data.decode()))

if __name__ == "__main__":
	cli_sock = socket.socket()
	HOST = "localhost"
	PORT = 49999
	cli_sock.connect((HOST, PORT))	
	window = tk.Tk()
	window.geometry(f"{5*48}x{5*51}")
	window.resizable(False, False)
	window.title("GAME CLIENT")
	thread_ac = threading.Thread(target=receive,args=(cli_sock,))
	thread_ac.start()
	window.bind('<KeyPress>', partial(send,cli_sock=cli_sock))
	window.mainloop()

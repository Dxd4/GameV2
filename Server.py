import tkinter as tk
from functools import partial
import random
import time
import threading
import socket


#GAME

def game():
	width = 5
	height = 5
	playground = [[0]*width for i in range(height)]
	colors = ["#BBBBBB","#BB5555","#55BBBB","#55BB55", "#5555BB"] # ["empty","blocked","bonus","player", "player2"]
	window = tk.Tk()
	window.geometry(f"{width*48}x{height*51}")
	window.resizable(False, False)
	window.title("GAME SERVER")
	for x in range(width):
		for y in range(height):
			if (x==0 and y==0):
				playground[x][y] = (tk.Label(window,bg=colors[3],width=6,height=3))
				playground[x][y].grid(row=x,column=y)
				continue
			if (x==width-1 and y==height-1):
				playground[x][y] = (tk.Label(window,bg=colors[4],width=6,height=3))
				playground[x][y].grid(row=x,column=y)
				continue
			if chance(60):
				playground[x][y]= (tk.Label(window,bg=colors[0],width=6,height=3))
				playground[x][y].grid(row=x,column=y)
				continue
			if chance(40):
				playground[x][y]= (tk.Label(window,bg=colors[1],width=6,height=3))
				playground[x][y].grid(row=x,column=y)
				continue
			else:
				playground[x][y]= (tk.Label(window,bg=colors[2],width=6,height=3))
				playground[x][y].grid(row=x,column=y)
				continue

	ser_sock = socket.socket()
	HOST = "localhost"
	PORT = 49999
	ser_sock.bind((HOST, PORT))
	ser_sock.listen(1)
	cli_sock, addr  = ser_sock.accept()

	thread_ac = threading.Thread(target=unicast_usr,args=(cli_sock,playground,colors,width,height,window))
	thread_ac.start()
	window.bind('<KeyPress>', partial(pressed,playground=playground, colors=colors, width=width, height=height, window=window, cli_sock=cli_sock))

	window.mainloop()
	

def change_field(playground,x,y,number):
	colors = ["#BBBBBB","#BB5555","#55BBBB","#55BB55", "#5555BB"]
	playground[x][y]["bg"] = colors[number]

def move(way,playground,player_field,colors,number, width, height, window, cli_sock):	
	x, y = player_field
	if way == "up":
		if (-1<(player_field[0]-1)<width) and not (playground[x-1][y]["bg"] == colors[1])and not (playground[x-1][y]["bg"] == colors[4])and not (playground[x-1][y]["bg"] == colors[3]):
			change_field(playground,x-1,y,number)
			change_field(playground,x,y,0)
			send(cli_sock,array_to_str(playground).encode())
	elif way == "left":
		if (-1<(player_field[1]-1)<width) and not (playground[x][y-1]["bg"] == colors[1])and not (playground[x][y-1]["bg"] == colors[4])and not (playground[x][y-1]["bg"] == colors[3]):
			change_field(playground,x,y-1,number)
			change_field(playground,x,y,0)
			send(cli_sock,array_to_str(playground).encode())
	elif way == "down":
		if (-1<(player_field[0]+1)<width) and not (playground[x+1][y]["bg"] == colors[1])and not (playground[x+1][y]["bg"] == colors[4])and not (playground[x+1][y]["bg"] == colors[3]):
			change_field(playground,x+1,y,number)
			change_field(playground,x,y,0)
			send(cli_sock,array_to_str(playground).encode())
	elif way == "right":
		if (-1<(player_field[1]+1)<width) and not (playground[x][y+1]["bg"] == colors[1])and not (playground[x][y+1]["bg"] == colors[4])and not (playground[x][y+1]["bg"] == colors[3]):
			change_field(playground,x,y+1,number)
			change_field(playground,x,y,0)
			send(cli_sock,array_to_str(playground).encode())
	if find_field(playground,colors,2, width, height) == None:
		for i in range(width):
			for j in range(height):
				change_field(playground,i,j,3)
				window.update()
				send(cli_sock,array_to_str(playground).encode())
				time.sleep(0.1)
				


def find_field(playground,colors,number, width, height):
	for x in range(width):
		for y in range(height):
			if playground[x][y]["bg"] == colors[number]:
				return [x,y]
	return None
def chance(chance_num):
	if random.randint(0,100) <=chance_num:
		return True
	return False


def pressed(event,playground, colors, width, height, window, cli_sock):
	player_field = find_field(playground,colors,3, width, height)
	if event.char == "w":
		move("up",playground,player_field,colors,3, width, height, window, cli_sock)
	elif event.char == "a":
		move("left",playground,player_field,colors,3, width, height, window, cli_sock)
	elif event.char == "s":
		move("down",playground,player_field,colors,3, width, height, window, cli_sock)
	elif event.char == "d":
		move("right",playground,player_field,colors,3, width, height, window, cli_sock)


# SERVER
def array_to_str(playground):
	pg_fields = ""
	for x in playground:
		for y in x:
			pg_fields += (y["bg"]) + ","
		pg_fields += "\n"
	return pg_fields

def unicast_usr(cli_sock,playground,colors, width, height, window):
	send(cli_sock,array_to_str(playground).encode())
	while True:
		try:
			data = cli_sock.recv(1024)
			if data:
				player_field = find_field(playground,colors,4, width, height)
				move(data.decode(),playground,player_field,colors,4, width, height, window, cli_sock)
		except Exception as x:
			print(x.message)
			break

def send(cli_sock,data):
	cli_sock.send(data)
	

	

if __name__ == "__main__":
	game()

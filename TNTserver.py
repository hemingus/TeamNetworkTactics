import socket
from _thread import *
import sys
from TLT import input_champion
import threading
import rich
from rich import print
from rich.prompt import Prompt
from rich.table import Table
import pickle

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team


SERVER = "192.168.150.1"
PORT = 9000
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)

player1 = []
player2 = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(f'You connected to TNTserver on {addr}'
            '\n'
            'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
            '\n'
            'Each player choose a champion each time.'
            '\n'.encode(FORMAT))
    player1_select = conn.recv(2048)
    player1 = pickle.loads(player1_select)
    print(f"Player 1 team: {player1}")
    conn.send(f"Player 1 team: {player1}".encode(FORMAT))
    

    


    """connected = True
    while connected:
        msg_length = conn.recv(2048).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send(f"Message {msg} received!".encode(FORMAT))
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")"""
            
       



def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        data = conn.recv(4096).decode()

        #if gameID in games:
            #game = games[gameID]

"""
connected = set()
games = {}
idCount = 0

while True:
    conn, addr = s.accept()
    print(f"[NEW CONNECTION] {addr}")

    idCount += 1
    p = 0
    gameID = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameID] = TLT(gameID)
        print("Creating a new game...")
    else:
        games[gameID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn,)) 
"""

def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def main() -> None:
    print("[STARTING] server is starting...")
    start()

main()






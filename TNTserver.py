import socket
from _thread import *
import threading
from rich import print
import pickle
from time import sleep

from champlistloader import load_some_champs
from core import Match, Team


SERVER = "192.168.150.1"
PORT = 9000
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)

def handle_client(conn, addr, p):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(f'You connected to TNTserver on {addr}'
            '\n'
            'Welcome to [bold yellow]Team Network Tactics[/bold yellow]!'
            '\n'
            'Each player choose a champion each time.'
            '\n'.encode(FORMAT))
    conn.send(f"You are player {str(p)}".encode(FORMAT))
    connected = True
    while connected:
        loop(conn, p)
        if len(player1) == team_size and len(player2) == team_size:
            if p == 1:
                if len(player2) > 0:
                    conn.send(player2[-1].encode(FORMAT))
            if p == 2:
                match = Match(
                            Team([champions[name] for name in player1]),
                            Team([champions[name] for name in player2])
                            )
                match.play()
                matches.append(match)
            print("calculating result...")
            sleep(3)
            summary = pickle.dumps(matches[0])
            conn.send(summary)
            break

def loop(conn, p):
    sleep(1)
    if p == 1:
        try:
            if len(player1) == len(player2) and len(player1) < team_size:
                if len(player2) > 0:
                    conn.send(player2[-1].encode(FORMAT))
                player1_select = conn.recv(2048)
            if player1_select:
                player1.append(player1_select.decode(FORMAT))
                print(f"Player 1 team: {player1}") 
        except:
            pass
          
    if p == 2:
        try:
            if len(player1) > len(player2) and len(player1) > 0:
                conn.send(player1[-1].encode(FORMAT))
                player2_select = conn.recv(2048)
            if player2_select:
                player2.append(player2_select.decode(FORMAT))
                print(f"Player 2 team: {player2}")
        except:
            pass
              
def start():

    s.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = s.accept()
        p = 1
        if threading.active_count() % 2 == 0:
            p = 2
        thread = threading.Thread(target=handle_client, args=(conn, addr, p))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

team_size = 3
matches = []
champions = load_some_champs()
player1 = []
player2 = []

def main() -> None:
    print("[STARTING] server is starting...")
    start()

main()






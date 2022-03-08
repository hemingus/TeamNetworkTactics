import socket
import rich
from TLT import print_available_champs, print_match_summary, input_champion, load_some_champs
import pickle


FORMAT = "utf-8"
PORT = 9000
SERVER = "192.168.150.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    #send_length += b' ' * (2048 - len(send_length))
    client.send(send_length)
    client.send(message)
    reply = client.recv(2048).decode()
    rich.print(reply)

def run():
    rich.print(client.recv(2048).decode())
    player1 = []
    player2 = []
    champions = load_some_champs()
    input_champion('Player 1', 'red', champions, player1, player2)
    update_team = pickle.dumps(player1)
    client.send(update_team)
    rich.print(client.recv(2048).decode())

run()

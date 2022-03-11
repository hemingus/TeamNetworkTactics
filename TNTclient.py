import socket
import rich
from TLT import print_available_champs, print_match_summary, input_champion, load_some_champs
import pickle
from time import sleep

FORMAT = "utf-8"
PORT = 9000
SERVER = "192.168.150.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

team_size = 3
champions = load_some_champs()
player1 = []
player2 = []

def send(msg):
    message = msg.encode(FORMAT)
    client.sendall(message)
    
def run():
    rich.print(client.recv(2048).decode())
    playerID = client.recv(2048).decode()
    rich.print(playerID)
    p = int(playerID[-1])
    if p == 1:
        rich.print("The [bold red]Red Team[/bold red]!")
    else:
        rich.print("The [bold blue]Blue Team[/bold blue]!")
    print_available_champs(champions)
    connected = True
    while connected:
        loop(p)
        if len(player1) == team_size and len(player2) == team_size:
            rich.print(f"[bold red]Red team[/bold red]: {player1}")
            rich.print(f"[bold blue]Blue team[/bold blue]: {player2}")
            try:
                reply = client.recv(2048)
                if reply:
                    summary = pickle.loads(reply)
                    print("Battle begins!")
                    sleep(1)
                    print("Calculating score...")
                    sleep(2)
                    print_match_summary(summary)
                    break
                else: loop(p)
            except:
                pass
        
        if p == 2:
            try:
                print("Waiting for red team...")
                update = client.recv(2048).decode(FORMAT)
                if update:
                    player1.append(update)
            except:
                pass
        if p == 1:
            try:
                print("Waiting for blue team...")
                update = client.recv(2048).decode(FORMAT)
                if update:
                    player2.append(update)
            except:
                pass

    print("Thanks for playing Team Network Tactics!")
    client.close()
        
def loop(p):
    if len(player1) == len(player2):
        player1turn = True
    else:
        player1turn = False
    
    if p == 1:
        if player1turn and len(player1) < team_size:
            input_champion('Red team - pick a champion', 'red', champions, player1, player2)
            update_team1 = str(player1[-1])
            send(update_team1)
    
    if p == 2: 
        if not player1turn and len(player2) < team_size:
            input_champion('Blue team - pick a champion', 'blue', champions, player2, player1)
            update_team2 = str(player2[-1])
            send(update_team2)
       
run()

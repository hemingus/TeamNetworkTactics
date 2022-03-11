import socket
import csv
import pickle
from core import Match, Team

SERVER = "localhost"
PORT = 9100
FORMAT = "utf-8"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)

def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = s.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        store_data(conn)

def store_data(conn):
    print("Waiting for data...")
    data = conn.recv(2048)
    if data:
        print("Collecting data...")
        match_data = pickle.loads(data)
        red_team = match_data.red_team
        blue_team = match_data.blue_team
        
    with open('TNT_DB.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\n')
        print("Writing to TNT database...")
        csv_writer.writerow(red_team)
        csv_writer.writerow(blue_team)
        
start()



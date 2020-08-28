import socket
import sqlite3
import json
import os
from game import game,player



if not os.path.isfile("users.db"):
    file = open("users.db","w+")
    file.close()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id int,login text, pass text, win int, lose int, longest int)''')

conn.commit()

sock = socket.socket()
sock.bind(('',9091))

print("DATABASE INITED")

while True:
    sock.listen(1)
    connection, address = sock.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        resp = json.loads(str(buf).split("\\r\\n")[-1])
        print(resp)

connection.close()

conn.close()


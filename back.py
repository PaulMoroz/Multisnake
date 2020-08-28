import socket
import sqlite3
import os
from game import game,player



if not os.path.isfile("users.db"):
    file = open("users.db","w+")
    file.close()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

conn.execute('''CREATE TABLE users
             (id int,login text, pass text, win int, lose int, longest int)''')

conn.commit()

sock = socket.socket()
sock.bind(('',9090))

while True:
    sock.listen(1)
    connection, address = sock.accept()
    buf = connection.recv(64)
    if len(buf) > 0:
        print(buf)
    

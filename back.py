import socket
import sqlite3
import json
import os
from game import game, player
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

if not os.path.isfile("users.db"):
    file = open("users.db","w+")
    file.close()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id int,login varchar(256), pass varchar(256), win int, lose int, longest int,temp int)''')
conn.commit()
conn.execute('''CREATE TABLE IF NOT EXISTS games
             (id int,name varchar(256), pass varchar(256),plOneId int,plTwoId int,plOneSnake text,plTwoSnake text,walls text,food text)''')
conn.commit()

sock = socket.socket()
sock.bind(('',8080))
games = {}
print("DATABASE INITED")


def register(player):
    cursor.execute("select COUNT(id) from users where login = '"+player['login']+"'")
    nums = cursor.fetchone()[0]
    if nums==0:
        cursor.execute("select COUNT(id) from users")
        pid = cursor.fetchone()[0]+1
        newp = [pid,player['login'],player['pass'] if player['temp'] == False else get_random_string(16) ,0,0,3,player['temp']]
        print(newp)
        cursor.execute(''' INSERT INTO users VALUES (?,?,?,?,?,?,?) ''',newp)
        conn.commit()
        return json.dumps({"opStatus":True,"id":pid,"login":player['login']})
    else:
        return json.dumps({"opStatus":False})

def checkIfExists(player):
    cursor.execute("select COUNT(id) from users where login = '"+player['login']+"' and pass = '"+player['pass']+"'")
    if cursor.fetchone()[0]==0:
        return json.dumps({"opStatus":False})
    else:
        return json.dumps({"opStatus":True,"id":pid,"login":player['login']})

def exit(player):
    cursor.execute("delete from users where login = '"+player['login']+"' and pass = '"+player['pass']+"' and id = '"+player['id']+"'")
    return json.dumps({"opStatus": True})

def getStat(player):
    cursor.execute("select win,lose,longest from users where login = '"+player['login']+"' and id = '"+player['id']+"' and temp = '"+str(0 if player["mode"]!=3 else 1)+"'")
    res = cursor.fetchone()
    ans = {}
    if res==None:
        ans["opStatus"] = False
    else:
        ans["win"] = res[0]
        ans["lose"] = res[1]
        ans["longest"] = res[2]
    return json.dumps(ans)
   
def getAllGames():      
    cursor.execute("select win,lose,longest from users where login = '"+player['login']+"' and id = '"+player['id']+"' and temp = '"+str(0 if player["mode"]!=3 else 1)+"'")
    res = cursor.fetchall()
    ans = {}
    ans["opStatus"] = True
    ans["games"] = res
    return json.dumps(ans)

def createGame(game):
    cursor.execute("select COUNT(id) from games where name = '"+game['name']+"'")
    nums = cursor.fetchone()[0]
    ans = {}
    if nums!=0:
        ans["opStatus"] = False
    else:
        ans["opStatus"] = True
        cursor.execute("select COUNT(id) from users")
        gid = cursor.fetchone()[0]+1
        nume = [gid,game['name'],game['pass'],game['pid'],-1,str(""),"",""]
        games[nume] = game.game()



def router(cmd: dict):
    if cmd['cmd']=="register":
        return register(cmd["player"])
    elif cmd['cmd']=="exit":
        return exit(cmd["player"])
    elif cmd['cmd']=="check":
        return checkIfExists(cmd["player"])
    elif cmd['cmd']=="getAllInfo":
        return getAllInfo(cmd["player"])
    elif cmd['cmd']=="getAllGames":
        return getAllInfo()


while True:
    sock.listen(1)
    connection, address = sock.accept()
    buf = connection.recv(1024)
    try:
        if len(buf) > 0:
            print(str(buf).split("\\r\\n"))
            print(str(buf).split("\\r\\n")[-1][:-1])
            resp = json.loads(str(buf).split("\\r\\n")[-1][:-1])
            connection.send(("HTTP/1.1 200 OK\n"
             + "Access-Control-Allow-Origin: *\n"
             + "Content-Type: json\n"
             + "\n"+router(resp)).encode('utf-8'))
    except:
        print(buf)


connection.close()

conn.close()

#!/usr/bin/env ruby
require 'sinatra'
require 'json'
require 'sinatra/cross_origin'
require 'sqlite3'
require_relative 'game.rb'
File.open("users.db","w") do |file|
end

$db = SQLite3::Database.open 'users.db'


$db.execute "CREATE TABLE IF NOT EXISTS users (id int,login varchar(256), pass varchar(256), win int, lose int, longest int,temp int)"
$db.execute "CREATE TABLE IF NOT EXISTS games (id int,name varchar(256), pass varchar(256),plOneId int,plTwoId int)"

games = {}


def register(player)
  ans = {'opStatus'=>TRUE}
  res = $db.execute 'select count(*) from users where login=?',player['login']
  if res[0][0] == 0
    res = $db.execute 'select count(*) from users'
    id = res[0][0]+1
    $db.execute 'insert into users values(?,?,?,0,0,3,?)', id, player['login'], player['pass'], player['temp']
    ans['pid'] = id
    ans['login'] = player['login']
  else
    ans['opStatus'] = FALSE
  end
   ans.to_json
end

def checkifexists(player)
  ans = {'opStatus'=>true}
  res = $db.execute 'select count(*) from users where login=? and pass=?',player['login'],player['pass']
  if res[0][0]==0
    ans['opStatus'] = FALSE
  else
    ans['pid'] = player['id']
    ans['login'] = player['login']
  end
  ans.to_json
end



def fingame(id)
  games.delete(id)
end

def exitgame(player)
  ans = {'opStatus'=>TRUE}
  res = $db.execute 'select gameId,plOneId,plTwoId from games where plOneId=? or plTwoId=?',player['id'],player['id']
  fingame(res[0][0])
  games['closed']+=1
  $db.execute 'delete from games where gameId = ?',res[0][0]
  ans.to_json
end

def exitapp(player)
  ans = {"opStatus"=>TRUE}
  exitgame(player)
  $db.execute 'delete from users where id=? and login=? and temp=1',res[0][1],res[0][2]
  ans.to_json
end


def getStat(player)
  ans = {"opStatus"=>TRUE}
  res = $db.execute 'select * from users where login=?',player['login']
  if res!=[]
    ans['win'] = res[0][3]
    ans['lose'] = res[0][4]
    ans['longest'] = res[0][5]
  else
    ans['opStatus'] = FALSE
  end
   ans.to_json
end

def getGameStatus()

end

def createGame(game)
  ans = {"opStatus"=>TRUE}
  if $games[game['name']]==nil
    id = $games.lenght()+1
    ans['gameId'] = id
    games[id] = {'game'=>Game.new}
    games[id]['fid'] = game['cid']
  else
    ans['opStatus'] = FALSE
  end
  ans.to_json
end

def logGame(player,game)
  ans = {"opStatus"=>TRUE}
  games[game['id']]['sid'] = player['id']
  ans
end

def getallgames()
  res = $db.execute "select * from games where 'plTwoId'=-1"
  ans = {"opStatus"=>TRUE}
  ans['games'] = res
   ans.to_json
end

def getstatus(player,game)

end

def router(data)
  if data['cmd']=='register'
     register(data['player'])
  elsif data['cmd']=='check'
     checkifexists(data['player'])
  elsif data['cmd']=='getAllInfo'
     getStat(data['player'])
  elsif data['cmd']=='exit'
     exitapp(data['player'])
  elsif data['cmd']=='exitgame'
    exitgame(data['player'])
  elsif data['cmd']=='getAllGames'
     getallgames
  else
     createGame(data['game'])
  end
end



configure do
  enable :cross_origin
end

before do
  response.headers['Access-Control-Allow-Origin'] = '*'
end

options "*" do
  response.headers["Allow"] = "GET, PUT, POST, DELETE, OPTIONS"
  response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, X-User-Email, X-Auth-Token"
  response.headers["Access-Control-Allow-Origin"] = "*"
  200
end



post "/" do
  data = JSON.parse request.body.read
  puts data
  res = router(data)
  res
end

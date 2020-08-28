import random
import time
class player:
    pid = ""
    snake = []
    color = 0
    side = 'U'
    def __init__(self):
        pass

    def eat(self,food:tuple):
        if self.snake[-1]==food:
            self.snake.append(food)
            return True
        return False

    def move(self):
        self.snake.pop(-1)
        if self.side == 'U':
            #row col
            self.snake.insert(0,(self.snake[0][0]-1,self.snake[0][1]))
        elif self.side=='D':
            self.snake.insert(0,(self.snake[0][0]+1,self.snake[0][1]))
        elif self.side=='R':
            self.snake.insert(0,(self.snake[0][0],self.snake[0][1]+1))
        else:
            self.snake.insert(0,(self.snake[0][0],self.snake[0][1]-1))
        

class game:
    player1 = player()
    player2 = player()
    food = ()
    walls = []
    free = []
    timeStart = 0
    currentTime = 0
    
    def __init__(self):
        pass
    
    def genNewFood(self):
        pass
    
    def genNewWall(self):
        t = random.choice(self.free)
        while t in self.player1.snake or t in self.player2.snake or t==self.food:
            t = random.choice(self.free)
        self.walls.append(t)
        self.free.remove(t)
    
    def winner(self):
        if  self.player1.snake[0] in self.player2.snake or self.player1.snake[0] in self.walls:
            return self.player2
        elif  self.player2.snake[0] in self.player2.snake or self.player2.snake[0] in self.walls:
            return self.player2
        elif self.currentTime>60 and len(self.player2.snake)>len(self.player1.snake):
            return self.player2
        elif  self.currentTime>60 and len(self.player2.snake)<len(self.player1.snake):
            return self.player1
        else:
            return None

    def eat(self):
        if self.player1.snake[0]==self.food:
            self.player1.eat(self.food)
        elif self.player2.snake[0]==self.food:
            self.player2.eat(self.food)

    def updMove(self,pid,side):
        if pid == self.player1.pid:
            self.player1.side = side
        else:
            self.player2.side = side
    
    def getAll(self):
        return self
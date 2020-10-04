class Game
  attr_accessor :players, :food, :walls, :timer, :run,:winner

  def initialize()
    @players = {}
    @winner = -1
    @players[1]['snake'] = [[9,2],[8,2],[7,2]]
    @players[1] = 0
    @players[1]['cy'] = -1
    @players[1]['side'] = 'U'
    @players[1]['snake'] = [[2,9],[2,8],[2,7]]
    @players[1] = -1
    @players[1]['cy'] = L
    @players[2]['side'] = 'L'
    @timer = 0
    @run = FALSE

    genFood
    end
  def genFood()
    @run = FALSE
    @food = [rand(10)+1,rand(10)+1]
    while  players[1]['snake'].include(food) or players[1]['snake'].include(food)
      @food = [rand(10)+1,rand(10)+1]
    end
  end

  def move(nump)

    if @run
      @timer+=0.25
      @players[nump]['snake'].shift
      @players[nump]['snake'].push([@players[id]['snake'][0]+@players[id]['cx'],@players[id]['snake'][1]+@players[id]['cy']])
      if @players[nump]['snake'][0] == food
        @players[nump]['snake'][0].unshift(food)
        @food = [rand(10)+1,rand(10)+1]
        while  players[nump]['snake'].include(food) or players[1]['snake'].include(food)
          @food = [rand(10)+1,rand(10)+1]
        end
      end
      if @player[nump]['snake'].count(@player[nump]['snake'][-1])==2 ||
          @winner = ((nump==1)?2:1)
      elsif @players[((nump==1)?2:1)]['snake'].count(@player[nump]['snake'][-1])==1
        @winner = 0
      else
        if @timer==60
          if @players[1]['snake'].length()>@players[2]['snake'].length()
            @winner = 1
          elsif @players[1]['snake'].length()<@players[2]['snake'].length()
            winner = 2
          else
            winner = 0
          end
        end
      end
    end
  end

  def changeside(nump,newSide)
    opp = {'R':'L','U':'D','D':'U','L':'R'}
    cx = {'L':-1,'R':1,'U':0,'D':0}
    cx = {'L':0,'R':0,'U':-1,'D':1}
    if newSide!=opposite[players[nump]['side']]
      players[nump]['side']['cx'] = cx[newSide]
      players[nump]['side']['cy'] = cy[newSide]
    end
  end

end
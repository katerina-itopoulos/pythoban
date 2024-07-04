from pydantic import BaseModel

class Position(BaseModel):
    x : int
    y : int 

class Score(BaseModel):
    time : 
    steps : int 
    
class Player(BaseModel):
    position : Position 
    push : bool = True 

class Box(BaseModel):
    type: 
    position: Position
    interaction : 

class Wall(BaseModel):
    type: 
    position: Position
    interaction : 

class Box(BaseModel):
    type: 
    position: Position
    interaction : 



class Level(BaseModel):
    items: list[Item]

class Map(BaseModel):
    width: int 
    height: int 
    items : list[Item]ßß
    player: Player


class Game(BaseModel):
    player : Player


    



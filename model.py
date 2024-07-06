
from pydantic import BaseModel, Field
from typing import List,Union


class Position(BaseModel):
    x : int
    y : int 

class Score(BaseModel):
    time : list[int] #[hrs, min, secs]
    steps : int 

    
class Player(BaseModel):
    position : Position 
    push : bool = True 

class AbstractItem(BaseModel):
    """ 
    Abstract base class for items in Pythoban
    """
    position : Position
    image_path : str
    symbol : str


class GoalBox(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    color : str
    goal : Position

class Goal(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    box : GoalBox
    color : str
    
class Box(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    
class Wall(AbstractItem):
    position : Position
    image_path : str
    symbol : str
   

class Magnet(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    direction : str

class MagnetSwitch(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    magnet : Magnet
    on : bool=True

class Water(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    isFilled: bool=False

class Portal(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    twin : Position
#maybe we could define two positions in the portal class? for each portal

class Hole(AbstractItem):
    position : Position
    image_path : str
    symbol : str
    isFilled: bool=False

    
class Map(BaseModel):
    matrix : List[List[Union[Player,AbstractItem]]]

class Level(BaseModel):
    map : Map 
    score : Score
    flag_path : str
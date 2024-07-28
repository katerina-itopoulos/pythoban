
import json
from pydantic import BaseModel, Field
from typing import List,Union,ClassVar


class Position(BaseModel):
    x : int
    y : int 

class Score(BaseModel):
    time : int #secs
    steps : int 

    
class Player(BaseModel):
    position : Position 
    push : bool = True
    image_path : ClassVar[str] = 'images/Isometric Blocks/PNG/Abstract tiles/abstractTile_24.png'

class AbstractItem(BaseModel):
    """ 
    Abstract base class for items in Pythoban
    """
    position : Position
    image_path : str
    symbol : str


# class GoalBox(AbstractItem):
#     position : Position
#     image_path : str
#     symbol : str
#     color : str
#     goal : Position

# class Goal(AbstractItem):
#     position : Position
#     image_path : str
#     symbol : str
#     box : GoalBox
#     color : str
    
class Box(AbstractItem):
    position : Position
    image_path : ClassVar[str] = 'images/Isometric Blocks/PNG/Platformer tiles/platformerTile_23.png'
    symbol : str = 'B'

class Goal(AbstractItem):
    position : Position
    image_path : ClassVar[str] = 'images/Isometric Blocks/PNG/Platformer tiles/platformerTile_37_2.png'
    symbol : str = 'G'
    # box : Box
    # color : str

class Wall(AbstractItem):
    position : Position
    image_path : ClassVar[str] = 'images/Isometric Blocks/PNG/Platformer tiles/platformerTile_20.png'
    symbol : str = 'W'

class Floor(AbstractItem):
    position : Position
    image_path : ClassVar[str] = 'images/Isometric Blocks/PNG/Abstract tiles/abstractTile_01.png'
    symbol : str = ' '
   

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
    matrix : List[List[Union[Player,AbstractItem,None]]]

    @classmethod
    def from_string(cls, mapString):
        matrix = []
        for i, line in enumerate(mapString.splitlines()):
            row = []
            for j, symbol in enumerate(line):
                position = Position(x=j,y=i)
                if symbol == ' ': # Nothing
                   row.append(Floor(position=position))
                elif symbol == 'W': # Wall
                    row.append(Wall(position=position))
                elif symbol == 'B': # Wall
                    row.append(Box(position=position))
                elif symbol == 'P':
                    row.append(Player(position=position))
                elif symbol == 'G':
                    row.append(Goal(position=position))
            matrix.append(row)
        return Map(matrix=matrix)


class Level(BaseModel):
    map : Map 
    score : Score
    # flag_path : str

    @classmethod
    def load_from_file(cls, path) -> "Level":
        with open(path, "r+") as file:
            levelJSON = json.loads(file.read())
            map = Map.from_string(levelJSON['map'])
            score = Score(time=levelJSON['score']['time'], steps=levelJSON['score']['steps'])
            level = Level(map=map, score=score)
            return level
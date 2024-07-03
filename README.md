# pythoban
Repository for advanced programming course group project on a game developed with Python.

#Origin

Pythoban is our take on the Japanese game Sokoban which is a puzzle video game in which the warehouse keeper ( which translates to Sokoban in Japanese) is required to push boxes around a warehouse and needs to get them into their designated goal locations. The game was designed in 1981 by Hiroyuki Imabayashi and first published in December 1982. For our edition, we have changed the character to a snake as we are doing an advanced Python course assignment and we have added various custom items to the course that differ from regular boxes and introduce irregular behaviour to each level. 

Information from : https://en.wikipedia.org/wiki/Sokoban

#Introduction 

Welcome to Pythoban! Our game is designed to be a fun problem-solving challenge with multiple levels and engaging graphics and sounds derived from Sokoban.

#Features


#Installation Guide 

#Requirements 
Python 3.0
Pygame 2.0

#Instructions for installation

1. Clone this repository
   git clone <enter url for our repo>
   cd pythoban 
   
2. Install the required dependencies
   
   pip install -r requirements.txt
   
3. Run the game
   python main.py
   
4. Testing 
   
   

#Gameplay instructions

The game starts at the main menu screen where the player can select the level.
The player can move using the arrow keys : up, down, left and right
The goal is to push the boxes into their corresponding goals/targets marked on the map. 
The player can only push boxes, it cannot pull. 
The score is tracked using the number of steps taken and time for each level. 

Each course is surrounded by and includes various wall items which cannot be pushed and act as boundaries. 
There are obstacles on each level which result in irregular behaviour. 
Magnet items will attach to boxes stopping them from moving unless the corresponding switch has been pressed down by a box. 
Water items will make the game unsolvable if a box with a goal or player steps on it. Water can be climbed over if a box without a goal has been pushed in to act as a bridge. 
Portal items allow the player and box to travel to the corresponding portal. 
Hole items will make the game unsolvable if the player or box with a goal falls inside. Holes can be closed if a box without a goal is pushed inside it. 


#Screenshots 

#License 
This project is licensed under the MIT License 

#Authors 
Katerina Itopoulos
Juan Méndez Nogales
David Rodrigues

#References  
https://en.wikipedia.org/wiki/Sokoban
https://en.wikipedia.org/wiki/Baba_Is_You
https://www.sokobanonline.com/help/how-to-play



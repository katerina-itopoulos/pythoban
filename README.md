# Pythoban

Repository for advanced programming course group project on a game developed with Python.

# Origin

Pythoban is our take on the Japanese game Sokoban which is a puzzle video game in which the warehouse keeper ( which translates to Sokoban in Japanese) is required to push boxes around a warehouse and needs to get them into their designated goal locations. The game was designed in 1981 by Hiroyuki Imabayashi and first published in December 1982. For our edition, we have changed the character to a snake as we are doing an advanced Python course assignment and we have added various custom items to the course that differ from regular boxes and introduce irregular behaviour to each level.

Information from : https://en.wikipedia.org/wiki/Sokoban

# Introduction

Welcome to Pythoban! Our game is designed to be a fun problem-solving challenge with multiple levels and engaging graphics and sounds derived from Sokoban.

# Features

# Installation Guide

# Requirements

Python 3.11 <br>
Pygame 2.0

# Instructions for installation

1. Clone this repository <be>
   `git clone <enter url for our repo>` <br>
   `cd pythoban` <br>
2. Install the required dependencies <br>

   `pip install -r requirements.txt ` <br>

3. Run the game <br>
   `python main.py` <br>
4. Testing <br>
   `pytest` to run all the tests. <br>

# How to play

The game starts at the main menu screen where the player can select the level. <br>
The player can move using the arrow keys : up, down, left and right. <br>
The goal is to push the boxes into their corresponding goals/targets marked on the map. <br>
The player can only push boxes, it cannot pull. <br>
The score is tracked using the number of steps taken and time for each level. <br> <br>

Each course is surrounded by and includes various wall items which cannot be pushed and act as boundaries. <br>
There are obstacles on each level which result in irregular behaviour. <br>
Magnet items will attach to boxes stopping them from moving unless the corresponding switch has been pressed down by a box. <br>
Water items will make the game unsolvable if a box with a goal or player steps on it. Water can be climbed over if a box without a goal has been pushed in to act as a bridge. <br>
Portal items allow the player and box to travel to the corresponding portal. <br>
Hole items will make the game unsolvable if the player or box with a goal falls inside. Holes can be closed if a box without a goal is pushed inside it. <br> <br>

## Levels

In our pythoban game, each level contains a different map with a variety of items with corresponding symbols represented in the table below, the goal is for the player to move all Boxes with goals into their goal positions. Each level is represented by a text file and converted into the graphics using this.

| Item                | Symbol |
| ------------------- | ------ |
| Box with Goal       | B      |
| Goal                | G      |
| Box on its Goal     | \*     |
| Box on another Goal | &      |
| Wall                | W      |
| Player              | P      |
| Floor               | Space  |

# Screenshots

# License

(c) 2024 Katerina Itopoulos, Juan Méndez Nogales and David Rodrigues. <br>
The Python code for this project is distributed under the conditions of the MIT License. See `LICENSE.TXT` for details. <br>
The graphics are taken from .... . See `ART_LICENSE.TXT` for a list of the authors.

# Authors

Katerina Itopoulos <br>
Juan Méndez Nogales <br>
David Rodrigues <br>

# References

# Code References

- Implemented using the Pygame library: https://www.pygame.org/ and it's provided examples and getting started tutorials.

## Art References

- Player Images: https://opengameart.org/content/isometric-snakes
- Blocks: https://opengameart.org/content/sokoban-100-tiles
- Font: https://www.dafont.com/minecraft.font
- Music: https://opengameart.org/content/menu-music
- TODO: References to the background image and logo made by David.

https://en.wikipedia.org/wiki/Sokoban <br>
https://en.wikipedia.org/wiki/Baba_Is_You <br>
https://www.sokobanonline.com/help/how-to-play <br>

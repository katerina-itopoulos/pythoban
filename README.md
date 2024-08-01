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
   `pip install -r dev_requirements.txt `<br>

3. Run the game <br>
   `python main.py` <br>
4. Testing <br>
   `pytest` to run all the tests. <br>

# How to play

The game starts at the main menu screen where the player can select the level. <br>
The player can move using the arrow keys : up, down, left and right. <br>
The goal is to push the boxes into goal objects marked on the map. <br>
The player can only push boxes, it cannot pull. <br>
The score is tracked using the number of steps taken and time for each level. <br> <br>
Each course is surrounded by and includes various wall items which cannot be pushed and act as boundaries. <br>


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
See `ART_LICENSE.TXT` for a list of the authors who designed the images and graphics used to build our Pythoban game.

# Authors

Katerina Itopoulos <br>
Juan Méndez Nogales <br>
David Rodrigues <br>

# References

# Code References

Development Tools and Documentation

1. Pygame Documentation
   - Website: [Pygame](https://www.pygame.org/docs/)
   - Description: This documentation was crucial for understanding the functions and classes used in the game development process.

2. Pytest Documentation
   - Website: [Pytest](https://docs.pytest.org/)
   - Description: Used for setting up testing frameworks to ensure game stability and performance.
  
3. Github Actions Documentation
   - Website: [GithubActions](https://docs.github.com/en/actions)
   - Description : Used to set up continuous integration for our project.


## Art and Game References

Can be found in the document titled ART_LICENSE.txt


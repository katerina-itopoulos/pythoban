import pytest
import pygame
import json
import tempfile
import os
from unittest.mock import patch
from model import Level,Map,Player,Score,Position
from game import Game

@pytest.fixture
def setup_game():
    # Initialize Pygame
    pygame.init()

    # Create a mock level with a simple map for testing
    test_map = "WWW    \nWGWWWWW\nWGG    \nW BBBPW\nW    WW\nWWWWWW "
    mock_map = Map.from_string(test_map)
    mock_score = Score(time=0, steps=0)
    level = Level(map=mock_map, score=mock_score, file_path="")

    # Create a Game instance and set up the initial state
    game = Game()
    game.loaded_levels = [level]
    game.selected_level = 1
    game.start_level()  # Initialize the level

    return game

def test_start_level(setup_game):
    game = setup_game

    # Assertions to check if the level is initialized correctly
    assert game._current_level is not None
    assert isinstance(game._current_level.map, Map)
    assert game._player is not None
    assert isinstance(game._player, Player)
    assert game._level_start_time is not None
    assert game._level_steps == 0

def test_restart_level(setup_game):
    game = setup_game

    # Modify the game state to simulate gameplay
    game._level_steps = 5

    # Call restart_level to reset the level
    game.restart_level()

    # Assertions to check if the level is reset correctly
    assert game._current_level is not None
    assert isinstance(game._current_level.map, Map)
    assert game._player is not None
    assert isinstance(game._player, Player)
    assert game._level_start_time is not None
    assert game._level_steps == 0

def test_player_movement_up(setup_game):
    game = setup_game
    player_initial_position = game._player.position

    # Simulate UP key press
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

    # Process all events in the queue (including the posted one)
    pygame.event.pump()

    # Assert player position is updated correctly
    assert game._player.position == Position(x=player_initial_position.x, y=player_initial_position.y - 1)

    # Clean up after the test (optional for small tests)
    pygame.quit()
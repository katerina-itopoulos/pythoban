import pytest
import pygame
import json
import tempfile
import os
from unittest.mock import patch
from model import Level, Map, Player, Score, Position
from game import Game
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT


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


@pytest.fixture
def winning_game():
    pygame.init()

    # Create a mock level with a winning map
    test_map = "WWW    \nWBWWWWW\nWBB    \nW    PW\nW    WW\nWWWWWW "
    mock_map = Map.from_string(test_map)
    mock_score = Score(time=0, steps=0)

    # Use a temporary file to avoid writing to the actual file system
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()  # Close the file so it can be used by the game
    file_path = temp_file.name

    level = Level(map=mock_map, score=mock_score, file_path=file_path)

    # Create a Game instance and set up the initial state
    game = Game()
    game.loaded_levels = [level]
    game.selected_level = 1
    game.start_level()  # Initialize the level

    # Simulate the game being in a winning state
    game.check_if_won()  # Ensure the game detects the win

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


def test_is_valid_position(setup_game):
    game = setup_game

    # Test valid positions (within bounds)
    assert game._is_valid_position((1, 1)) == True
    assert game._is_valid_position((1, 3)) == True
    assert game._is_valid_position((2, 3)) == True

    # Test invalid positions (outside bounds)
    assert game._is_valid_position((0, 8)) == False
    assert game._is_valid_position((7, 0)) == False
    assert game._is_valid_position((-1, 0)) == False


def test_move_player(setup_game):
    game = setup_game

    # Get initial player position
    initial_position = game._player.position

    # Define a new valid position for the player to move to
    new_position = (initial_position.x + 1, initial_position.y)  # Move one to the right

    # Call the move_player function
    game._move_player(new_position)

    # Assert that the player position is updated correctly
    assert (
        game._player.position.x == new_position[0]
        and game._player.position.y == new_position[1]
    )


def test_get_box_next_position_down(setup_game):
    game = setup_game
    game._player.position = Position(x=4, y=2)

    # Simulate pressing the down key
    keys = {pygame.K_DOWN: True}

    next_position = game._get_box_next_position(keys)

    assert next_position == (4, 4)


def test_check_if_won_non_winning(setup_game):
    game = setup_game
    # Simulate the game state as not complete
    game.check_if_won()
    assert not game._has_won
    # Cleanup: remove the temporary file
    if os.path.exists(game.loaded_levels[0].file_path):
        os.remove(game.loaded_levels[0].file_path)


def test_check_if_won_winning(winning_game):
    game = winning_game
    # Simulate the game state as won
    game.check_if_won()
    assert game._has_won
    # Cleanup: remove the temporary file
    if os.path.exists(game.loaded_levels[0].file_path):
        os.remove(game.loaded_levels[0].file_path)

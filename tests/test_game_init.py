import pygame
import pytest
from unittest.mock import patch
from game import Game

@pytest.fixture
def game():
    # Create a Game instance and initialize it
    game_instance = Game()
    game_instance.init_game()
    yield game_instance

@patch('pygame.mixer.music.load')  # Mock the music loading
@patch('pygame.mixer.music.play')  # Mock the music playing
@patch('pygame.mixer.init')  # Mock the mixer initialization
def test_initialization(mock_play, mock_load, mock_init, game):
    # Assertions to verify the initialization
    assert game.screen is not None
    assert game.clock is not None
    assert game.screen.get_size() == (game.screen_width, game.screen_height)
    assert game._current_level_index == 0
    assert game.selected_option_main_menu == 'newGame'
import pygame
import pytest
from game import Game

@pytest.fixture
def game():
    game_instance = Game()
    game_instance.init_game()
    yield game_instance
    

def test_initialization(game):
    assert game.screen is not None
    assert game.clock is not None
    assert game.screen.get_size() == (game.screen_width, game.screen_height)
    assert game._current_level_index == 0
    assert game.selected_option_main_menu == 'newGame'

"""
Pythoban Game Logic 
"""

import pygame
from datetime import datetime, timedelta
from typing import Any, Type, ClassVar
from pydantic import BaseModel, Field
from os import listdir
from os.path import isfile, join
from model import (
    Level,
    Box,
    Wall,
    Floor,
    Goal,
    Player,
    HorizontalDirectionEnum,
    VerticalDirectionEnum,
)


class Game(BaseModel):
    _current_level_index: int = 0  # 0 Is main menu, -1 is choosing level
    _current_level: Level | None
    screen: Any = Field(exclude=True, title="screen", default=None)
    clock: Any = Field(exclude=True, title="clock", default=None)
    screen_width: int = 1280
    screen_height: int = 720
    text_size: int = screen_height // 10
    running: bool = True
    levels_directory: str = "levels"
    loaded_levels: list[Level] = []
    _fontPath: str = "fonts/minecraft.ttf"
    _background_image: pygame.Surface | None = None
    _title_image: pygame.Surface | None = None
    _background_path: str = "images/background.png"
    _title_path: str = "images/logo.png"
    _icon_path: str = (
        "images/Isometric Blocks/PNG/Platformer tiles/platformerTile_23.png"
    )

    _music_path: str = "audio/awesomeness.wav"
    _music_volume: float = 0.25

    # restart image relative path
    BUTTON_IMAGE_PATH: ClassVar[str] = "images/restart/restart.png"

    restart_button_image: pygame.Surface | None = None
    restart_button_rect: pygame.Rect | None = None

    # Main Menu
    _selected_option_color = "green"
    _unselected_option_color = "white"

    selected_option_main_menu: str = "newGame"
    title_text: str = "Pythoban"
    texts: dict[str, str] = {
        "newGame": "New Game",
        "chooseLevel": "Choose Level",
        "quitGame": "Quit Game",
    }

    item_images: dict[Type, Any] = {}
    _available_items = [Box]

    # Choose Level
    selected_level: int = 0

    # Current Level
    _player: Player | None = None
    _level_start_time: datetime | None = None
    _level_steps: int = 0
    _has_won: bool = False

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.text_size = self.screen_height // 10

    def save_score(self):
        new_time_in_seconds = int(
            (datetime.now() - self._level_start_time).total_seconds()
        )
        new_steps = self._level_steps
        self.loaded_levels[self._current_level_index - 1].update_score(
            new_time_in_seconds, new_steps
        )

    def get_file_paths_in_dir(self, directory):
        return [
            join(directory, file)
            for file in listdir(directory)
            if isfile(join(directory, file))
        ]

    def load_levels(self):
        levels_files_paths = self.get_file_paths_in_dir(self.levels_directory)
        levels_files_paths.sort()
        self.loaded_levels = [
            Level.load_from_file(level_file) for level_file in levels_files_paths
        ]
        # print([l.file_path for l in self.loaded_levels])

    def load_item_images(self):
        items = [Box, Floor, Wall, Goal, Player]
        for item in items:
            if item == Player:
                self.item_images[item] = self.load_player_images(item)
            else:
                self.item_images[item] = self.load_static_item_images(item)

    def load_player_images(self, player_class):
        """Load images for the player, considering direction."""
        player_images_dict = {}
        for vertical_direction in VerticalDirectionEnum:
            player_images_dict[vertical_direction] = {}
            for horizontal_direction in HorizontalDirectionEnum:
                image_path = join(
                    player_class.image_path,
                    f"{vertical_direction}_{horizontal_direction}.png",
                )
                player_images_dict[vertical_direction][
                    horizontal_direction
                ] = pygame.image.load(image_path)
        return player_images_dict

    def load_static_item_images(self, item_class):
        """Load images for static items and apply transparency."""
        image = pygame.image.load(item_class.image_path)
        number_of_images = 4
        images = [image.copy() for _ in range(number_of_images)]

        for index, img in enumerate(images):
            img.set_alpha(int(255 * (1 - (index / number_of_images))))

        return images

    def load_images(self):
        """Load all game-related images."""
        self.load_item_images()
        self.load_restart_button_image()
        self.load_background_image()
        self.load_title_image()

    def load_restart_button_image(self):
        """Load the restart button image and set its position."""
        self.restart_button_image = pygame.image.load(self.BUTTON_IMAGE_PATH)
        if self.restart_button_image:
            self.restart_button_rect = self.restart_button_image.get_rect(
                topleft=(self.screen_width // 40, self.screen_height * 3 // 20)
            )

    def load_background_image(self):
        """Load and scale the background image to fit the screen size."""
        background_image = pygame.image.load(self._background_path)
        self._background_image = pygame.transform.scale(
            background_image, (self.screen_width, self.screen_height)
        )

    def load_title_image(self):
        """Load and scale the title image to fit a portion of the screen width."""
        original_title_image = pygame.image.load(self._title_path)
        title_width = int(self.screen_width * 0.8)
        title_height = (
            original_title_image.get_height() * title_width
        ) // original_title_image.get_width()
        self._title_image = pygame.transform.scale(
            original_title_image, (title_width, title_height)
        )

    def show_main_menu(self):
        """Display the main menu with a title and selectable options."""
        font = self.get_font(self.text_size)
        self.display_title()
        self.display_menu_options(font)

    def get_font(self, size):
        """Return a font object of a given size."""
        return pygame.font.Font(self._fontPath, size)

    def display_title(self):
        """Display the title image centered at the top of the screen."""
        text_rect = self._title_image.get_rect(
            midtop=(self.screen_width / 2, self.screen_height // 10)
        )
        self.screen.blit(self._title_image, text_rect)

    def display_menu_options(self, font):
        """Display each menu option with appropriate styling."""
        for index, text_key in enumerate(self.texts):
            text_surface = self.get_text_surface(font, text_key)
            text_rect = self.get_text_rect(text_surface, index)
            self.screen.blit(text_surface, text_rect)

    def get_text_surface(self, font, text_key):
        """Render the text surface for a menu option."""
        font.set_underline(self.selected_option_main_menu == text_key)
        color = (
            self._selected_option_color
            if self.selected_option_main_menu == text_key
            else self._unselected_option_color
        )
        return font.render(self.texts[text_key], True, color)

    def get_text_rect(self, text_surface, index):
        """Get the position for a menu option's text surface."""
        return text_surface.get_rect(
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) + (index * text_surface.get_height()),
            )
        )

    def show_choose_level_menu(self):
        self.show_choose_level_menu_title()
        self.show_choose_level_menu_levels()
        self.show_choose_level_menu_goback()

    def show_choose_level_menu_title(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        text_surface = font.render(
            self.texts["chooseLevel"], True, self._unselected_option_color
        )
        text_rect = text_surface.get_rect(
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) - (4 * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

    def show_choose_level_menu_levels(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        for index, test_key in enumerate(self.loaded_levels):
            font.set_underline(self.selected_level == index + 1)
            text_surface = font.render(
                f"Level {index+1}",
                True,
                (
                    self._selected_option_color
                    if self.selected_level == index + 1
                    else self._unselected_option_color
                ),
            )
            text_rect = text_surface.get_rect(
                center=(
                    self.screen_width / 2,
                    (self.screen_height / 3) + (index * text_surface.get_height()),
                )
            )
            self.screen.blit(text_surface, text_rect)

    def show_choose_level_menu_goback(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        font.set_underline(self.selected_level == 0)
        text_surface = font.render(
            f"< Go back to main menu",
            True,
            (
                self._selected_option_color
                if self.selected_level == 0
                else self._unselected_option_color
            ),
        )
        text_rect = text_surface.get_rect(
            center=(
                self.screen_width / 2,
                (self.screen_height / 2.2)
                + (len(self.loaded_levels) * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

    def show_win_screen(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        self._show_win_screen_title(font)
        self._show_win_screen_time(size)
        self._show_win_screen_steps(size)
        self._show_win_screen_levels(font)
        self._show_win_screen_go_back(font)

    def _show_win_screen_title(self, font):
        title_text = f"You beat level {self._current_level_index}"
        self._render_text(
            title_text,
            font,
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) - (4 * font.get_height()),
            ),
            color=self._unselected_option_color,
        )

    def _show_win_screen_time(self, size):
        score_font = pygame.font.Font(self._fontPath, size // 2)
        passed_time = timedelta(
            seconds=self.loaded_levels[self._current_level_index - 1].score.time
        )
        passed_time_text = self.duration_to_str(passed_time)
        time_text = f"Time: {passed_time_text}"
        self._render_text(
            time_text,
            score_font,
            center=(
                self.screen_width // 2,
                (self.screen_height / 2) - (5 * score_font.get_height()),
            ),
            color=self._unselected_option_color,
        )

    def _show_win_screen_steps(self, size):
        score_font = pygame.font.Font(self._fontPath, size // 2)
        steps_text = f"Steps: {self._level_steps}"
        self._render_text(
            steps_text,
            score_font,
            center=(
                self.screen_width // 2,
                (self.screen_height / 2) - (4 * score_font.get_height()),
            ),
            color=self._unselected_option_color,
        )

    def _show_win_screen_levels(self, font):
        if self._current_level_index < len(self.loaded_levels):
            font.set_underline(self.selected_level == self._current_level_index + 1)
            level_text = f"Level {self._current_level_index + 1}"
            self._render_text(
                level_text,
                font,
                center=(
                    self.screen_width / 2,
                    (self.screen_height / 3.1)
                    + (self._current_level_index * font.get_height()),
                ),
                color=self._selected_option_color
                if self.selected_level == self._current_level_index + 1
                else self._unselected_option_color,
            )

    def _show_win_screen_go_back(self, font):
        font.set_underline(self.selected_level == 0)
        go_back_text = "< Go back to main menu"
        self._render_text(
            go_back_text,
            font,
            center=(
                self.screen_width / 2,
                (self.screen_height / 2.5)
                + (len(self.loaded_levels) * font.get_height()),
            ),
            color=self._selected_option_color
            if self.selected_level == 0
            else self._unselected_option_color,
        )

    def _render_text(self, text, font, center, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def duration_to_str(self, duration):
        fullDuration = str(duration)
        return fullDuration.split(".")[0]

    def draw_level_text(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        self._draw_level_title(font)
        self._draw_score_and_time(size)
        self._draw_steps(size)

    def _draw_level_title(self, font):
        level_text = f"Level {self._current_level_index}"
        self._draw_level_text(
            level_text,
            font,
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) - (4 * font.get_height()),
            ),
            color=self._unselected_option_color,
        )

    def _draw_score_and_time(self, size):
        score_font = pygame.font.Font(self._fontPath, size // 2)
        passed_time = datetime.now() - self._level_start_time
        passed_time_text = self.duration_to_str(passed_time)

        time_text = f"Time: {passed_time_text}"
        self._draw_level_text(
            time_text,
            score_font,
            topleft=(self.screen_width // 40, self.screen_height // 20),
            color=self._unselected_option_color,
        )

    def _draw_steps(self, size):
        score_font = pygame.font.Font(self._fontPath, size // 2)
        steps_text = f"Steps: {self._level_steps}"
        self._draw_level_text(
            steps_text,
            score_font,
            topleft=(self.screen_width // 40, self.screen_height * 2 // 20),
            color=self._unselected_option_color,
        )

    def _draw_level_text(self, text, font, center=None, topleft=None, color=None):
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=center)
        elif topleft:
            text_rect = text_surface.get_rect(topleft=topleft)
        else:
            raise ValueError(
                "Either 'center' or 'topleft' must be provided for text positioning."
            )
        self.screen.blit(text_surface, text_rect)

    def draw_level(self):
        self.draw_level_text()
        self.draw_level_items()

    def draw_level_items(self):
        x_offset = 64
        y_offset = 64
        main_surface = self._create_main_surface(x_offset, y_offset)
        self._draw_items_on_surface(main_surface, x_offset, y_offset)
        self._blit_scaled_surface(main_surface)
        self._draw_restart_button()

    def _create_main_surface(self, x_offset, y_offset):
        main_surface_size = (
            len(self._current_level.map.matrix[0]) * x_offset,
            len(self._current_level.map.matrix) * y_offset,
        )
        main_surface = pygame.Surface(main_surface_size)
        main_surface.fill("black")
        return main_surface

    def _draw_items_on_surface(self, surface, x_offset, y_offset):
        for i, row in enumerate(self._current_level.map.matrix):
            for j, column in enumerate(row):
                for k, cell in enumerate(column):
                    class_to_draw = type(cell)
                    if class_to_draw != type(None):
                        image_to_draw = self._get_image_for_cell(class_to_draw)
                        surface.blit(image_to_draw, (j * x_offset, i * y_offset))

    def _get_image_for_cell(self, class_to_draw):
        if class_to_draw == Player:
            return self.item_images[class_to_draw][
                self._player.last_vertical_direction
            ][self._player.last_horizontal_direction]
        else:
            return self.item_images[class_to_draw][0]

    def _blit_scaled_surface(self, surface):
        scale_factor = 0.7
        scaled_surface_size = (
            min(int(self.screen_width * scale_factor), surface.get_width()),
            min(int(self.screen_height * scale_factor), surface.get_height()),
        )
        surface = pygame.transform.scale(surface, scaled_surface_size)
        surface_rect = surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(surface, surface_rect)

    def _draw_restart_button(self):
        self.screen.blit(self.restart_button_image, self.restart_button_rect)

    def process_global_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_q]:
            if self._current_level_index == 0:
                self.running = False
            else:
                self.selected_level = 0
                self.start_level()

    def process_main_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
                self._handle_navigation(keys)
            elif keys[pygame.K_RETURN]:
                self._handle_selection()

    def _handle_navigation(self, keys):
        text_keys = list(self.texts.keys())
        if keys[pygame.K_DOWN]:
            self._navigate_down(text_keys)
        elif keys[pygame.K_UP]:
            self._navigate_up(text_keys)

    def _navigate_down(self, text_keys):
        new_option_index = (text_keys.index(self.selected_option_main_menu) + 1) % len(
            text_keys
        )
        self.selected_option_main_menu = text_keys[new_option_index]

    def _navigate_up(self, text_keys):
        new_option_index = (text_keys.index(self.selected_option_main_menu) - 1) % len(
            text_keys
        )
        self.selected_option_main_menu = text_keys[new_option_index]

    def _handle_selection(self):
        if self.selected_option_main_menu == "newGame":
            self._start_new_game()
        elif self.selected_option_main_menu == "chooseLevel":
            self._choose_level()
        elif self.selected_option_main_menu == "quitGame":
            self._quit_game()

    def _start_new_game(self):
        self.selected_level = 1
        self.start_level()

    def _choose_level(self):
        self.selected_level = 1
        self._current_level_index = -1

    def _quit_game(self):
        self.running = False

    def process_choose_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.selected_level = (self.selected_level + 1) % (
                    len(self.loaded_levels) + 1
                )
            elif keys[pygame.K_UP]:
                self.selected_level = (self.selected_level - 1) % (
                    len(self.loaded_levels) + 1
                )
            elif keys[pygame.K_RETURN]:
                self.start_level()

    def process_win_screen_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if self._current_level_index < len(self.loaded_levels):
                if keys[pygame.K_DOWN]:
                    self.selected_level = (
                        0
                        if self.selected_level == self._current_level_index + 1
                        else self._current_level_index + 1
                    )
                elif keys[pygame.K_UP]:
                    self.selected_level = (
                        0
                        if self.selected_level == self._current_level_index + 1
                        else self._current_level_index + 1
                    )
            if keys[pygame.K_RETURN]:
                self.start_level()

    def process_level_events(self, event):
        if event.type == pygame.QUIT:
            self._handle_quit_event()
        elif event.type == pygame.KEYDOWN:
            self._handle_keydown_event(pygame.key.get_pressed())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down_event(pygame.mouse.get_pos())

    def _handle_quit_event(self):
        self.running = False

    def _handle_keydown_event(self, keys):
        (
            player_next_position,
            direction_updated,
        ) = self._get_player_next_position_and_direction(keys)

        if player_next_position:
            self._process_player_move(player_next_position)
            if direction_updated:
                self._update_directions(direction_updated)

    def _get_player_next_position_and_direction(self, keys):
        if keys[pygame.K_DOWN]:
            return (
                self._player.position.x,
                self._player.position.y + 1,
            ), VerticalDirectionEnum.down
        elif keys[pygame.K_UP]:
            return (
                self._player.position.x,
                self._player.position.y - 1,
            ), VerticalDirectionEnum.up
        elif keys[pygame.K_LEFT]:
            return (
                self._player.position.x - 1,
                self._player.position.y,
            ), HorizontalDirectionEnum.left
        elif keys[pygame.K_RIGHT]:
            return (
                self._player.position.x + 1,
                self._player.position.y,
            ), HorizontalDirectionEnum.right
        return None, None

    def _process_player_move(self, player_next_position):
        if self._is_valid_position(player_next_position):
            player_next_cell = self._current_level.map.matrix[player_next_position[1]][
                player_next_position[0]
            ][1]
            if player_next_cell is None:
                self._move_player(player_next_position)
                self._level_steps += 1
            elif isinstance(player_next_cell, Box):
                self._process_box_movement(player_next_position)

    def _process_box_movement(self, player_next_position):
        box_next_position = self._get_box_next_position(pygame.key.get_pressed())
        if box_next_position and self._is_valid_position(box_next_position):
            box_next_cell = self._current_level.map.matrix[box_next_position[1]][
                box_next_position[0]
            ][1]
            if box_next_cell is None:
                self._move_box_and_player(player_next_position, box_next_position)
                self._level_steps += 1
                self.check_if_won()

    def _update_directions(self, direction):
        if isinstance(direction, VerticalDirectionEnum):
            self._player.last_vertical_direction = direction
        elif isinstance(direction, HorizontalDirectionEnum):
            self._player.last_horizontal_direction = direction

    def _handle_mouse_button_down_event(self, mouse_pos):
        if self.restart_button_rect.collidepoint(mouse_pos):
            self.restart_level()

    def _is_valid_position(self, position):
        return 0 <= position[1] < len(self._current_level.map.matrix) and 0 <= position[
            0
        ] < len(self._current_level.map.matrix[0])

    def _get_box_next_position(self, keys):
        if keys[pygame.K_DOWN]:
            return (self._player.position.x, self._player.position.y + 2)
        elif keys[pygame.K_UP]:
            return (self._player.position.x, self._player.position.y - 2)
        elif keys[pygame.K_LEFT]:
            return (self._player.position.x - 2, self._player.position.y)
        elif keys[pygame.K_RIGHT]:
            return (self._player.position.x + 2, self._player.position.y)
        return None

    def _move_player(self, position):
        # Remove player from current position
        self._current_level.map.matrix[self._player.position.y][
            self._player.position.x
        ][1] = None

        # Move player to new position
        self._player.position.x, self._player.position.y = position
        self._current_level.map.matrix[position[1]][position[0]][1] = self._player

    def _move_box_and_player(self, player_position, box_position):
        # Remove box from current position
        box = self._current_level.map.matrix[player_position[1]][player_position[0]][1]
        self._current_level.map.matrix[player_position[1]][player_position[0]][1] = None

        # Move box to new position
        box.position.x, box.position.y = box_position
        self._current_level.map.matrix[box_position[1]][box_position[0]][1] = box

        # Move player to new position
        self._move_player(player_position)

    def process_events(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            self.process_global_events(event)
            if self._current_level_index == 0:
                self.process_main_menu_events(event)
            elif self._current_level_index == -1:
                self.process_choose_level_events(event)
            else:
                if not self._has_won:
                    self.process_level_events(event)
                else:
                    self.process_win_screen_events(event)

    def start_level(self):
        self._current_level_index = self.selected_level
        self._current_level = self.loaded_levels[
            self._current_level_index - 1
        ].model_copy(deep=True)
        self._has_won = False
        self._player = None

        # Get Player from level matrix
        for row in self._current_level.map.matrix:
            for column in row:
                if type(column[1]) == Player:
                    self._player = column[1]
                    break
            if self._player != None:
                break
        self._level_start_time = datetime.now()
        self._level_steps = 0

    def check_if_won(self):
        has_won = True
        for row in self._current_level.map.matrix:
            for column in row:
                if type(column[0]) == Goal and type(column[1]) != Box:
                    has_won = False
                    break
            if not has_won:
                break
        self._has_won = has_won
        if self._has_won:
            self.selected_level = (
                self._current_level_index + 1
                if self._current_level_index + 1 < len(self.loaded_levels)
                else 0
            )
            self.save_score()

    def restart_level(self):
        self.start_level()

    def clean_screen(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.blit(self._background_image, (0, 0))

    def update_screen(self):
        # flip() the display to put your work on screen
        pygame.display.flip()
        self.clock.tick(60)  # limits FPS to 60

    def init_game(self):
        self.init_pygame()
        self.load_levels()
        self.load_images()
        self.play_music()  # Call play_music after initializing the mixer and loading the music

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Pythoban")
        pygame.display.set_icon(pygame.image.load(self._icon_path))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()  # Initialize the mixer here

    def play_music(self):
        pygame.mixer.music.load(
            self._music_path
        )  # Load music after initializing the mixer
        pygame.mixer.music.set_volume(self._music_volume)
        pygame.mixer.music.play(loops=-1)  # Play music in the background

    def run(self):
        self.init_game()
        while self.running:
            self.process_events()
            self.clean_screen()

            if self._current_level_index == 0:
                self.show_main_menu()
            elif self._current_level_index == -1:
                self.show_choose_level_menu()
            else:
                if not self._has_won:
                    self.draw_level()
                else:
                    self.show_win_screen()

            self.update_screen()

        pygame.quit()

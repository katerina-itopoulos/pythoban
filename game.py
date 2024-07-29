"""
Pythoban Game Logic 
"""

import pygame
from datetime import datetime, timedelta
from typing import Any, Type, ClassVar
from pydantic import BaseModel, Field
from os import listdir
from os.path import isfile, join
from model import Level,Box,Wall,Floor,Goal,Player,HorizontalDirectionEnum,VerticalDirectionEnum



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

    selected_option_main_menu: int = "newGame"
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
        for i in items:
            if i == Player:
                player_images_dict = {}
                for vertical_direction in VerticalDirectionEnum:
                    player_images_dict[vertical_direction] = {}
                    for horizontal_direction in HorizontalDirectionEnum:
                        path = join(
                            i.image_path,
                            f"{vertical_direction}_{horizontal_direction}.png",
                        )
                        player_images_dict[vertical_direction][horizontal_direction] = (
                            pygame.image.load(path)
                        )
                self.item_images[i] = player_images_dict
            else:
                image = pygame.image.load(i.image_path)
                numberOfImages = 4
                self.item_images[i] = [image.copy() for _ in range(numberOfImages)]
                for index, image in enumerate(self.item_images[i]):
                    image.set_alpha(int(255 * (1 - (index / numberOfImages))))

    def load_images(self):
        # Load item images
        self.load_item_images()

        # Load restart button image
        self.restart_button_image = pygame.image.load(self.BUTTON_IMAGE_PATH)
        if self.restart_button_image:
            self.restart_button_rect = self.restart_button_image.get_rect(
                topleft=(self.screen_width // 40, self.screen_height * 3 // 20)
            )
        # Load background image
        self._background_image = pygame.transform.scale(
            pygame.image.load(self._background_path),
            (self.screen_width, self.screen_height),
        )
        # Load title image
        original_title_image = pygame.image.load(self._title_path)
        title_width = int(self.screen_width * 0.8)
        title_height = (original_title_image.get_height() * title_width) / original_title_image.get_width()
        self._title_image = pygame.transform.scale(original_title_image, (title_width, title_height))

    def show_main_menu(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        # Title
        text_rect = self._title_image.get_rect(
            midtop=(
                self.screen_width / 2,
                self.screen_height // 10,
            )
        )
        self.screen.blit(self._title_image, text_rect)
        # Other texts
        for index, textKey in enumerate(self.texts):
            font.set_underline(self.selected_option_main_menu == textKey)
            text_surface = font.render(
                self.texts[textKey],
                True,
                (
                    self._selected_option_color
                    if self.selected_option_main_menu == textKey
                    else self._unselected_option_color
                ),
            )
            text_rect = text_surface.get_rect(
                center=(
                    self.screen_width / 2,
                    (self.screen_height / 2) + (index * text_surface.get_height()),
                )
            )
            self.screen.blit(text_surface, text_rect)

    def show_choose_level_menu(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        # Title
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

        # Levels
        for index, textKey in enumerate(self.loaded_levels):
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
                    (self.screen_height / 2) + (index * text_surface.get_height()),
                )
            )
            self.screen.blit(text_surface, text_rect)

        # Go back
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
                (self.screen_height / 2)
                + (len(self.loaded_levels) * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

    def show_win_screen(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        # Title
        text_surface = font.render(
            f"You beat level {self._current_level_index}",
            True,
            self._unselected_option_color,
        )
        text_rect = text_surface.get_rect(
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) - (4 * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

        # Score
        # Time
        scoreFont = pygame.font.Font(self._fontPath, size // 2)
        passed_time = timedelta(
            seconds=self.loaded_levels[self._current_level_index - 1].score.time
        )
        passed_time_text = self.duration_to_str(passed_time)

        passed_time_text_surface = scoreFont.render(
            f"Time: {passed_time_text}", True, self._unselected_option_color
        )
        passed_time_text_rect = passed_time_text_surface.get_rect(
            center=(
                self.screen_width // 2,
                (self.screen_height / 2) - (3 * text_surface.get_height()),
            )
        )
        self.screen.blit(passed_time_text_surface, passed_time_text_rect)

        # Steps
        steps_text_surface = scoreFont.render(
            f"Steps: {self._level_steps}", True, self._unselected_option_color
        )
        steps_time_text_rect = steps_text_surface.get_rect(
            center=(
                self.screen_width // 2,
                (self.screen_height / 2) - (2 * text_surface.get_height()),
            )
        )
        self.screen.blit(steps_text_surface, steps_time_text_rect)

        # Levels
        if self._current_level_index + 1 < len(self.loaded_levels):
            font.set_underline(self.selected_level == self._current_level_index + 1)
            text_surface = font.render(
                f"Level {self._current_level_index+1}",
                True,
                (
                    self._selected_option_color
                    if self.selected_level == self._current_level_index + 1
                    else self._unselected_option_color
                ),
            )
            text_rect = text_surface.get_rect(
                center=(
                    self.screen_width / 2,
                    (self.screen_height / 2)
                    + (self._current_level_index * text_surface.get_height()),
                )
            )
            self.screen.blit(text_surface, text_rect)

        # Go back
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
                (self.screen_height / 2)
                + (len(self.loaded_levels) * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

    def duration_to_str(self, duration):
        fullDuration = str(duration)
        return fullDuration.split(".")[0]


    def draw_level_text(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)

        # Title
        text_surface = font.render(
            f"Level {self._current_level_index}", True, self._unselected_option_color
        )
        text_rect = text_surface.get_rect(
            center=(
                self.screen_width / 2,
                (self.screen_height / 2) - (4 * text_surface.get_height()),
            )
        )
        self.screen.blit(text_surface, text_rect)

        # Score
        # Time
        scoreFont = pygame.font.Font(self._fontPath, size // 2)
        passed_time = datetime.now() - self._level_start_time
        passed_time_text = self.duration_to_str(passed_time)

        passed_time_text_surface = scoreFont.render(
            f"Time: {passed_time_text}", True, self._unselected_option_color
        )
        passed_time_text_rect = passed_time_text_surface.get_rect(
            topleft=(self.screen_width // 40, self.screen_height // 20)
        )
        self.screen.blit(passed_time_text_surface, passed_time_text_rect)

        # Steps
        steps_text_surface = scoreFont.render(
            f"Steps: {self._level_steps}", True, self._unselected_option_color
        )
        steps_time_text_rect = steps_text_surface.get_rect(
            topleft=(self.screen_width // 40, self.screen_height * 2 // 20)
        )
        self.screen.blit(steps_text_surface, steps_time_text_rect)

    def draw_level(self):
        self.draw_level_text()
        self.draw_level_items()

    def draw_level_items(self):
        x_offset = 64
        y_offset = 64
        main_surface_size = (
            len(self._current_level.map.matrix[0]) * x_offset,
            len(self._current_level.map.matrix) * y_offset,
        )
        main_surface = pygame.Surface(main_surface_size)
        main_surface.fill("black")

        # Items next
        for i, row in enumerate(self._current_level.map.matrix):
            for j, column in enumerate(row):
                for k, cell in enumerate(column):
                    classToDraw = type(cell)
                    if classToDraw != type(None):
                        if classToDraw == Player:
                            # print(self._player.last_vertical_direction, self._player.last_horizontal_direction)
                            imageToDraw = self.item_images[classToDraw][
                                self._player.last_vertical_direction
                            ][self._player.last_horizontal_direction]
                        else:
                            imageToDraw = self.item_images[classToDraw][0]
                        main_surface.blit(imageToDraw, (j * x_offset, i * y_offset))

        # In case the level doesn't fit on the screen, define maximum values
        scale_factor = 0.7
        scaled_main_surface_size = (
            min(int(self.screen_width * scale_factor), main_surface.get_width()),
            min(int(self.screen_height * scale_factor), main_surface.get_height()),
        )
        main_surface = pygame.transform.scale(main_surface, scaled_main_surface_size)
        main_surface_rect = main_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )

        # Now into the actual screen
        self.screen.blit(main_surface, main_surface_rect)
        # Draw restart button
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
        textKeys = list(self.texts.keys())
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                newOptionIndex = (
                    textKeys.index(self.selected_option_main_menu) + 1
                ) % len(textKeys)
                self.selected_option_main_menu = textKeys[newOptionIndex]
            elif keys[pygame.K_UP]:
                newOptionIndex = (
                    textKeys.index(self.selected_option_main_menu) - 1
                ) % len(textKeys)
                self.selected_option_main_menu = textKeys[newOptionIndex]
            elif keys[pygame.K_RETURN]:
                if self.selected_option_main_menu == "newGame":
                    self.selected_level = 1
                    self.start_level()
                elif self.selected_option_main_menu == "chooseLevel":
                    self.selected_level = 1
                    self._current_level_index = -1
                elif self.selected_option_main_menu == "quitGame":
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
            if self._current_level_index + 1 < len(self.loaded_levels):
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
            self.running = False
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            player_next_position = None

            if keys[pygame.K_DOWN]:
                player_next_position = (
                    self._player.position.x,
                    self._player.position.y + 1,
                )
                self._player.last_vertical_direction = VerticalDirectionEnum.down
            elif keys[pygame.K_UP]:
                player_next_position = (
                    self._player.position.x,
                    self._player.position.y - 1,
                )
                self._player.last_vertical_direction = VerticalDirectionEnum.up
            elif keys[pygame.K_LEFT]:
                player_next_position = (
                    self._player.position.x - 1,
                    self._player.position.y,
                )
                self._player.last_horizontal_direction = HorizontalDirectionEnum.left
            elif keys[pygame.K_RIGHT]:
                player_next_position = (
                    self._player.position.x + 1,
                    self._player.position.y,
                )
                self._player.last_horizontal_direction = HorizontalDirectionEnum.right

            # If valid player_next_position
            if player_next_position is not None and self._is_valid_position(
                player_next_position
            ):
                player_next_cell = self._current_level.map.matrix[
                    player_next_position[1]
                ][player_next_position[0]][1]

                if player_next_cell is None:
                    # Move player to new position
                    self._move_player(player_next_position)
                    self._level_steps += 1

                elif isinstance(player_next_cell, Box):
                    box_next_position = self._get_box_next_position(keys)

                    if box_next_position is not None and self._is_valid_position(
                        box_next_position
                    ):
                        box_next_cell = self._current_level.map.matrix[
                            box_next_position[1]
                        ][box_next_position[0]][1]

                        if box_next_cell is None:
                            self._move_box_and_player(
                                player_next_position, box_next_position
                            )
                            self._level_steps += 1
                            self.check_if_won()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.restart_button_rect.collidepoint(mouse_x, mouse_y):
                self.restart_level()  # Add this method to handle restarting the level

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
        self.play_music()
        self.load_levels()
        self.load_images()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Pythoban")
        pygame.display.set_icon(pygame.image.load(self._icon_path))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(self._music_path)
        pygame.mixer.music.set_volume(self._music_volume)

    def play_music(self):
        pygame.mixer.music.play(loops=-1)

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

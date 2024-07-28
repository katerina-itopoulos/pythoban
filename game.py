"""
Pythoban Game Logic 
"""
import pygame
from datetime import datetime
from typing import Any, Type
from pydantic import BaseModel, Field
from os import listdir
from os.path import isfile, join
from model import Level, Box, Wall, Floor, Goal, Player

class Game(BaseModel):
    _current_level_index: int = 0 # 0 Is main menu, -1 is choosing level
    _current_level: Level | None
    screen: Any = Field(exclude=True, title='screen', default=None)
    clock: Any = Field(exclude=True, title='clock', default=None)
    screen_width: int = 1280
    screen_height: int = 720
    text_size: int = screen_height // 10 
    running: bool = True
    levels_directory: str = 'levels'
    loaded_levels: list[Level] = []
    _fontPath: str = 'fonts/minecraft.ttf'
    _background_image: pygame.Surface | None = None
    _background_path: str = 'images/background.png'
    _icon_path: str = 'images/Isometric Blocks/PNG/Platformer tiles/platformerTile_23.png'

    _music_path: str = 'audio/awesomeness.wav'
    _music_volume: float = 0.25

    # Main Menu
    _selected_option_color = 'green'
    _unselected_option_color = 'white'
    
    selected_option_main_menu: int = "newGame"
    title_text: str = "Pythoban"
    texts: dict[str, str] = {
        "newGame": "New Game",
        "chooseLevel": "Choose Level",
        "quitGame": "Quit Game"
    }

    item_images: dict[Type, Any] = {}
    _available_items = [Box]

    # Choose Level
    selected_level: int = 0

    # Current Level
    _player: Player | None  = None
    _level_start_time: datetime | None = None
    _level_steps: int = 0
    _has_won: bool = False
    

    def save_score(self):
        new_time_in_seconds = int((datetime.now() - self._level_start_time).total_seconds())
        new_steps = self._level_steps
        self.loaded_levels[self._current_level_index - 1].update_score(new_time_in_seconds, new_steps)

    def load_levels(self):
        levels_files_paths =  [join(self.levels_directory, file) for file in listdir(self.levels_directory) if isfile(join(self.levels_directory, file))]
        self.loaded_levels = [Level.load_from_file(level_file) for level_file in levels_files_paths]

    def load_item_images(self):
        items = [Box, Floor, Wall, Goal, Player]
        for i in items:
            image = pygame.image.load(i.image_path)
            numberOfImages = 4
            self.item_images[i] = [image.copy() for _ in range(numberOfImages)]
            for index, image in enumerate(self.item_images[i]):
                image.set_alpha(int(255 * (1 - (index / numberOfImages))))

    def show_main_menu(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        
        # Title
        text_surface = font.render(self.title_text, True, self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) - (4 * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)
        # Other texts
        for index, textKey in enumerate(self.texts):
            font.set_underline(self.selected_option_main_menu == textKey)
            text_surface = font.render(self.texts[textKey], True, self._selected_option_color if self.selected_option_main_menu == textKey else self._unselected_option_color)
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) + (index * text_surface.get_height())))
            self.screen.blit(text_surface, text_rect)
    
    def show_choose_level_menu(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        
        # Title
        text_surface = font.render(self.texts['chooseLevel'], True, self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) - (4 * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)
        
        # Levels
        for index, textKey in enumerate(self.loaded_levels):
            font.set_underline(self.selected_level == index + 1)
            text_surface = font.render(f'Level {index+1}', True, self._selected_option_color if self.selected_level == index + 1 else self._unselected_option_color)
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) + (index * text_surface.get_height())))
            self.screen.blit(text_surface, text_rect)
        
        # Go back
        font.set_underline(self.selected_level == 0)
        text_surface = font.render(f'< Go back to main menu', True, self._selected_option_color if self.selected_level == 0 else self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) + (len(self.loaded_levels) * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)
    
    def show_win_screen(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        
        # Title
        text_surface = font.render(f'You beat level {self._current_level_index}', True, self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) - (4 * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)

        # Score
        # Time
        scoreFont = pygame.font.Font(self._fontPath, size // 2)
        passed_time = datetime.now() - self._level_start_time
        passed_time_text = self.duration_to_str(passed_time)
        
        passed_time_text_surface = scoreFont.render(f'Time: {passed_time_text}', True, self._unselected_option_color)
        passed_time_text_rect = passed_time_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 20))
        self.screen.blit(passed_time_text_surface, passed_time_text_rect)

        # Steps
        steps_text_surface = scoreFont.render(f'Steps: {self._level_steps}', True, self._unselected_option_color)
        steps_time_text_rect = steps_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 2 // 20))
        self.screen.blit(steps_text_surface, steps_time_text_rect)
        
        # Levels
        if(self._current_level_index + 1 < len(self.loaded_levels)):
            font.set_underline(self.selected_level == self._current_level_index + 1)
            text_surface = font.render(f'Level {self._current_level_index+1}', True, self._selected_option_color if self.selected_level == self._current_level_index + 1 else self._unselected_option_color)
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) + (self._current_level_index * text_surface.get_height())))
            self.screen.blit(text_surface, text_rect)
        
        # Go back
        font.set_underline(self.selected_level == 0)
        text_surface = font.render(f'< Go back to main menu', True, self._selected_option_color if self.selected_level == 0 else self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) + (len(self.loaded_levels) * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)

    def duration_to_str(self,duration):
        fullDuration = str(duration)
        return fullDuration.split('.')[0]

    def draw_level(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        
        # Title
        text_surface = font.render(f'Level {self._current_level_index}', True, self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) - (4 * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)

        # Score
        # Time
        scoreFont = pygame.font.Font(self._fontPath, size // 2)
        passed_time = datetime.now() - self._level_start_time
        passed_time_text = self.duration_to_str(passed_time)
        
        passed_time_text_surface = scoreFont.render(f'Time: {passed_time_text}', True, self._unselected_option_color)
        passed_time_text_rect = passed_time_text_surface.get_rect(topleft=(self.screen_width // 40, self.screen_height // 20))
        self.screen.blit(passed_time_text_surface, passed_time_text_rect)

        # Steps
        steps_text_surface = scoreFont.render(f'Steps: {self._level_steps}', True, self._unselected_option_color)
        steps_time_text_rect = steps_text_surface.get_rect(topleft=(self.screen_width // 40, self.screen_height * 2 // 20))
        self.screen.blit(steps_text_surface, steps_time_text_rect)

        x_offset = 56
        y_offset = 32
        top = (self.screen_height // 4) - y_offset
        left = (self.screen_width // 2) - x_offset

        # Floor first
        for i, row in enumerate(self._current_level.map.matrix):
            for j, column in enumerate(row):
                classToDraw = type(column[0])
                imageToDraw =  self.item_images[Goal][0] if classToDraw == Goal else self.item_images[Floor][0]
                self.screen.blit(imageToDraw, (left + (j * x_offset) - (i * x_offset), top + (i * y_offset) + (j * y_offset)))
        
        top_offset = 64
        top = (self.screen_height // 4) - y_offset - top_offset
        left = (self.screen_width // 2) - x_offset

        # Items next
        transparentPositionsPlayer = []
        for i, row in enumerate(self._current_level.map.matrix):
            for j, column in enumerate(row):
                classToDraw = type(column[1])
                if(classToDraw != type(None)):
                    # shouldBeTransparent = False
                    imageToDraw = None
                    if((i == self._player.position.y + 1 and j == self._player.position.x)
                        or (i == self._player.position.y and j == self._player.position.x + 1)
                        or (i == self._player.position.y + 1 and j == self._player.position.x + 1)
                        or (i > 0 and j > 0 and {type(item) for item in self._current_level.map.matrix[i-1][j-1]}.intersection({Goal, Box}))
                        ):
                        # print('transparent image around player or important object', j, i, self._player.position)
                        imageToDraw = self.item_images[classToDraw][-1]
                        transparentPositionsPlayer.append((j,i))
                    
                    # if(classToDraw != Player):
                    #     for m in range(i):
                    #         for n in range(j):
                    #             # print(type(level.map.matrix[m][n]))
                    #             if type(level.map.matrix[m][n]) not in [Floor, Wall]:
                    #                 imageToDraw = self.item_images[classToDraw][-3]
                    #                 break
                    #         if(imageToDraw): break
                    # print("column", column)
                    # print("classToDraw", classToDraw)
                    if(not imageToDraw): imageToDraw = self.item_images[classToDraw][0]
                    # imageToDraw = self.item_images[classToDraw][1] if shouldBeTransparent else self.item_images[classToDraw][0]
                    # if(classToDraw in [Wall, Box, Player]):
                    self.screen.blit(imageToDraw, (left + (j * x_offset) - (i * x_offset), top + (i * y_offset) + (j * y_offset)))
        # if(transparentPositionsPlayer): print(transparentPositionsPlayer)

    def process_global_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_q]:
            if(self._current_level_index == 0):
                self.running = False
            else:
                self.selected_level = 0
                self.start_level()

    def process_main_menu_events(self, event):
        textKeys = list(self.texts.keys())
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                newOptionIndex = (textKeys.index(self.selected_option_main_menu) + 1) % len(textKeys)
                self.selected_option_main_menu = textKeys[newOptionIndex]
            elif keys[pygame.K_UP]:
                newOptionIndex = (textKeys.index(self.selected_option_main_menu) - 1) % len(textKeys)
                self.selected_option_main_menu = textKeys[newOptionIndex]
            elif keys[pygame.K_RETURN]:
                if self.selected_option_main_menu == 'newGame':
                    self.selected_level = 1
                    self.start_level()
                elif self.selected_option_main_menu == 'chooseLevel':
                    self.selected_level = 1
                    self._current_level_index = -1
                elif self.selected_option_main_menu == 'quitGame':
                    self.running = False

    def process_choose_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.selected_level = (self.selected_level + 1) % (len(self.loaded_levels) + 1)
            elif keys[pygame.K_UP]:
                self.selected_level = (self.selected_level - 1) % (len(self.loaded_levels) + 1)
            elif keys[pygame.K_RETURN]:
                self.start_level()
    
    def process_win_screen_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if(self._current_level_index + 1 < len(self.loaded_levels)):
                if keys[pygame.K_DOWN]:
                    self.selected_level = 0 if self.selected_level == self._current_level_index + 1 else self._current_level_index + 1
                elif keys[pygame.K_UP]:
                    self.selected_level = 0 if self.selected_level == self._current_level_index + 1 else self._current_level_index + 1
            elif keys[pygame.K_RETURN]:
                self.start_level()

    def process_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            player_next_position = None
            if keys[pygame.K_DOWN]:
                player_next_position = (self._player.position.x, self._player.position.y + 1)
            elif keys[pygame.K_UP]:
                player_next_position = (self._player.position.x, self._player.position.y - 1)
            elif keys[pygame.K_LEFT]:
                player_next_position = (self._player.position.x - 1, self._player.position.y)
            elif keys[pygame.K_RIGHT]:
                player_next_position = (self._player.position.x + 1, self._player.position.y)
            #if(player_next_position):
                #print('player_next_position', player_next_position)
                #print(player_next_position[1] < len(self._current_level.map.matrix), player_next_position[1] >= 0, player_next_position[0] < len(self._current_level.map.matrix[0]), player_next_position[0] >= 0)
            # If valid player_next_position
            if(player_next_position != None 
               and player_next_position[1] < len(self._current_level.map.matrix) 
               and player_next_position[1] >= 0
               and player_next_position[0] < len(self._current_level.map.matrix[0])
               and player_next_position[0] >= 0):
                player_next_cell = self._current_level.map.matrix[player_next_position[1]][player_next_position[0]][1]
                #print('player_next_cell', player_next_cell)
                if(type(player_next_cell) == type(None)):
                    # Remove player from current position
                    self._current_level.map.matrix[self._player.position.y][self._player.position.x][1] = None

                    # Add player to new position
                    self._player.position.x = player_next_position[0]
                    self._player.position.y = player_next_position[1]
                    self._current_level.map.matrix[player_next_position[1]][player_next_position[0]][1] = self._player

                    self._level_steps += 1

                elif(type(player_next_cell) == Box):
                    #print('Trying to move box')
                    box_next_position = None
                    if keys[pygame.K_DOWN]:
                        box_next_position = (self._player.position.x, self._player.position.y + 2)
                    elif keys[pygame.K_UP]:
                        box_next_position = (self._player.position.x, self._player.position.y - 2)
                    elif keys[pygame.K_LEFT]:
                        box_next_position = (self._player.position.x - 2, self._player.position.y)
                    elif keys[pygame.K_RIGHT]:
                        box_next_position = (self._player.position.x + 2, self._player.position.y)
                    #if(box_next_position):
                        #print('box_next_position', box_next_position)
                        #print(box_next_position[1] < len(self._current_level.map.matrix), box_next_position[1] >= 0, box_next_position[0] < len(self._current_level.map.matrix[0]), box_next_position[0] >= 0)
                    
                    # If valid box_next_position

                    if(box_next_position != None 
                       and box_next_position[1] < len(self._current_level.map.matrix) 
                       and box_next_position[1] >= 0
                       and box_next_position[0] < len(self._current_level.map.matrix[0])
                       and box_next_position[0] >= 0):
                        box_next_cell = self._current_level.map.matrix[box_next_position[1]][box_next_position[0]][1]
                        #print(box_next_cell)
                        box_to_move = player_next_cell
                        if(type(box_next_cell) == type(None)):
                            # Remove box from current position
                            self._current_level.map.matrix[player_next_position[1]][player_next_position[0]][1] = None

                            # Add box to new position
                            box_to_move.position.x = box_next_position[0]
                            box_to_move.position.y = box_next_position[1]
                            self._current_level.map.matrix[box_next_position[1]][box_next_position[0]][1] = box_to_move

                            # Remove player from current position
                            self._current_level.map.matrix[self._player.position.y][self._player.position.x][1] = None

                            # Add player to new position
                            self._player.position.x = player_next_position[0]
                            self._player.position.y = player_next_position[1]
                            self._current_level.map.matrix[player_next_position[1]][player_next_position[0]][1] = self._player

                            self._level_steps += 1
                            self.check_if_won()

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
                if(not self._has_won):
                    self.process_level_events(event)
                else:
                    self.process_win_screen_events(event)

    def start_level(self):

        self._current_level_index = self.selected_level
        self._current_level = self.loaded_levels[self._current_level_index - 1].model_copy(deep=True)
        self._has_won = False
        self._player = None
        
        # Get Player from level matrix
        for row in self._current_level.map.matrix:
            for column in row:
                if(type(column[1]) == Player): 
                    self._player = column[1]
                    break
            if(self._player != None):
                break
        self._level_start_time = datetime.now()
        self._level_steps = 0

    def check_if_won(self):
        has_won = True
        for row in self._current_level.map.matrix:
            for column in row:
                if(type(column[0]) == Goal and type(column[1]) != Box):
                    has_won = False
                    break
            if(not has_won): break
        self._has_won = has_won
        if(self._has_won):
            self.selected_level = self._current_level_index + 1 if self._current_level_index + 1 < len(self.loaded_levels) else 0
            self.save_score()
    
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
        self.load_item_images()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Pythoban')
        pygame.display.set_icon(pygame.image.load(self._icon_path))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self._background_image = pygame.transform.scale(pygame.image.load(self._background_path), (self.screen_width, self.screen_height))
        pygame.mixer.music.load(self._music_path)
        pygame.mixer.music.set_volume(self._music_volume)
    
    def play_music(self):
        pygame.mixer.music.play(loops=-1)
    
    def run(self):
        self.init_game()
        while self.running:
            self.process_events()
            self.clean_screen()

            if(self._current_level_index == 0):
                self.show_main_menu()
            elif(self._current_level_index == -1):
                self.show_choose_level_menu()
            else:
                if(not self._has_won): self.draw_level()
                else:
                    self.show_win_screen()
                
            
            self.update_screen()

        pygame.quit()


"""
Pythoban Game Logic 
"""
import pygame
from typing import Any
from pydantic import BaseModel, Field
from os import listdir
from os.path import isfile, join

class Map(BaseModel):
    matrix: list[str]
class Level(BaseModel):
    score: int = 0
    map: Map
    @classmethod
    def load_from_file(cls, path) -> "Level":
        with open(path, "r") as file:
            map = Map(matrix=file.readlines())
            level = Level(map=map)
            return level


        

class Game(BaseModel):
    level: int = 0 # 0 Is main menu, -1 is choosing level
    screen: Any = Field(exclude=True, title='screen', default=None)
    clock: Any = Field(exclude=True, title='clock', default=None)
    screen_width: int = 1280
    screen_height: int = 720
    text_size: int = screen_height // 10 
    running: bool = True
    levels_directory: str = 'levels'
    loaded_levels: list = []
    _fontPath: str = 'fonts/minecraft.ttf'
    _background_path: str = 'images/background.png'
    _background_image: pygame.Surface | None = None
    _selected_option_color = 'green'
    _unselected_option_color = 'white'

    # Main Menu
    selected_option_main_menu: int = "newGame"
    title_text: str = "Pythoban"
    texts: dict[str,str] = {
        "newGame": "New Game",
        "chooseLevel": "Choose Level",
        "quitGame": "Quit Game"
    }

    # Choose Level
    selected_level: int = 0

    def load_levels(self):
        levels_files_paths =  [join(self.levels_directory, file) for file in listdir(self.levels_directory) if isfile(join(self.levels_directory, file))]
        self.loaded_levels = [Level.load_from_file(level_file) for level_file in levels_files_paths]

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

    def draw_level(self):
        size = self.text_size
        font = pygame.font.Font(self._fontPath, size)
        
        # Title
        text_surface = font.render(f'Level {self.level}', True, self._unselected_option_color)
        text_rect = text_surface.get_rect(center=(self.screen_width / 2, (self.screen_height / 2) - (4 * text_surface.get_height())))
        self.screen.blit(text_surface, text_rect)
        pass

    def process_events(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.level == 0:
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
                            self.level = -1
                        elif self.selected_option_main_menu == 'quitGame':
                            self.running = False
            elif self.level == -1:
                textKeys = list(self.texts.keys())
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_DOWN]:
                        self.selected_level = (self.selected_level + 1) % (len(self.loaded_levels) + 1)
                    elif keys[pygame.K_UP]:
                        self.selected_level = (self.selected_level - 1) % (len(self.loaded_levels) + 1)
                    elif keys[pygame.K_RETURN]:
                        self.start_level()

    def start_level(self):
        self.level = self.selected_level    
    
    def clean_screen(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.blit(self._background_image, (0, 0))
    
    def update_screen(self):
        # flip() the display to put your work on screen
        pygame.display.flip()
        self.clock.tick(60)  # limits FPS to 60
    
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self._background_image = pygame.transform.scale(pygame.image.load(self._background_path), (self.screen_width, self.screen_height))


    def run(self):
        self.init_pygame()
        self.load_levels()
        while self.running:
            self.process_events()
            self.clean_screen()

            if(self.level == 0):
                self.show_main_menu()
            elif(self.level == -1):
                self.show_choose_level_menu()
            else:
                self.draw_level()
            
            self.update_screen()

        pygame.quit()


"""
Pythoban Game Logic 
"""
import pygame
from typing import Optional, Any
from pydantic import BaseModel, Field

class Game(BaseModel):
    level: int = 0
    screen: Any = Field(exclude=True, title='screen', default=None)
    clock: Any = Field(exclude=True, title='clock', default=None)
    running:bool = True

    def run(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


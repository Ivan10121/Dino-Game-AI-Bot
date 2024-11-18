from GameObject import GameObject
from numpy import random
import pygame

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 1350

    def update(self,speed,delta_time):
        self.x -= speed * delta_time
    
    def is_offscreen(self):
        return self.x + self.width < 0

class Cactus(Enemy):
    def __init__(self):
        super().__init__()
        self.sprite_offset[0] = -2
        self.sprite_offset[1] = -2
        self.cactus_widths = [30, 64, 98, 46, 96, 146]
        self.cactus_heights = [66, 66, 66, 96, 96, 96]
        self.sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
        self.cactus_sprites = [
            self.sprite_sheet.subsurface((446, 2, 34, 70)),
            self.sprite_sheet.subsurface((480, 2, 68, 70)),
            self.sprite_sheet.subsurface((548, 2, 102, 70)),
            self.sprite_sheet.subsurface((652, 2, 50, 100)),
            self.sprite_sheet.subsurface((702, 2, 100, 100)),
            self.sprite_sheet.subsurface((802, 2, 150, 100))
        ]
        
        self.cactus_y_pos = [470, 470, 470, 444, 444, 444]
        self.type =random.randint(0,6)
        self.width = self.cactus_widths[self.type]
        self.height = self.cactus_heights[self.type]
        self.y = self.cactus_y_pos[self.type]
        self.sprite = self.cactus_sprites[self.type]

    def display(self,screen):
        screen.blit(self.sprite, (self.x + self.sprite_offset[0], self.y + self.sprite_offset[1]))

class Bird(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 84
        self.height = 40
        self.sprite_offset[0] = -4
        self.sprite_offset[1] = -16
        self.birds_y_pos = [435, 480, 370]
        self.type =random.randint(0,3)
        self.y = self.birds_y_pos[self.type]
        self.sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
        self.sprite = self.sprite_sheet.subsurface((260, 2, 92, 80))

    def display(self,screen):
        screen.blit(self.sprite, (self.x + self.sprite_offset[0], self.y + self.sprite_offset[1]))




        
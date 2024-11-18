from GameObject import GameObject
import pygame

class Ground(GameObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 515

        self.sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
        self.sprite = self.sprite_sheet.subsurface((2, 104, 2400, 24))


    def update(self,speed, delta_time):
        self.x -= speed * delta_time
        if self.x <= -self.sprite.get_width():
            self.x = 0
    
    def display(self,screen):
        screen.blit(self.sprite, (self.x,self.y))
        screen.blit(self.sprite, (self.x + self.sprite.get_width(), self.y))

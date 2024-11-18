import pygame


class GameObject():
    def __init__(self):
        pygame.init()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.sprite_offset = [0,0]


    def get_rect(self):
        # Get the collider of the object
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_colliding(self, other):
        return self.get_rect().colliderect(other.get_rect())
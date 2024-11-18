from dino import Dino
import pygame
from enemy import Cactus,Bird
from ground import Ground

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.player = Dino()
        pygame.init()
        self.ground = Ground()
        self.sprite_sheet = pygame.image.load("Juego/sprites.png").convert_alpha()
        self.ground_sprite = self.sprite_sheet.subsurface((2, 104, 2400, 24))
        self.ground_x = 0
        self.speed = 1000
        self.cacti = []
        self.birds = []
        self.spawn_timer = 0

    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.player.jump()

        if keys[pygame.K_DOWN]:
            if self.player.jumping:
                self.player.stop_jump()
            else:
                self.player.crouch()
        else:
            if self.player.crouching:
                self.player.stop_crouching()

    def spawn_cactus(self,delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer > 2:
            self.cacti.append(Cactus())
            self.spawn_timer = 0

    def update_cacti(self,delta_time):
        for cactus in self.cacti:
            cactus.update(self.speed,delta_time)
            if cactus.is_offscreen():
                self.cacti.remove(cactus)

    def spawn_bird(self,delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer > 2:
            self.cacti.append(Bird())
            self.spawn_timer = 0

    def update_birds(self,delta_time):
        for bird in self.birds:
            bird.update(self.speed,delta_time)
            if bird.is_offscreen():
                self.cacti.remove(bird)

    def check_collisions(self):
        for cactus in self.cacti:
            if self.player.is_colliding(cactus):
                print("Game over")

        for bird in self.birds:
            if self.player.is_colliding(bird):
                print("Game over")
    
    def update(self,delta_time):
        self.handle_events()
        self.player.update()

        self.ground.update(self.speed,delta_time)
        self.spawn_cactus(delta_time)
        self.update_cacti(delta_time)
        self.spawn_bird(delta_time)
        self.update_birds(delta_time)
        self.check_collisions()

    def display(self):
        self.ground.display(self.screen)
        self.player.display(self.screen)
        for cactus in self.cacti:
            cactus.display(self.screen)
        for bird in self.birds:
            bird.display(self.screen)


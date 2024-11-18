import pygame
from GameObject import GameObject
from brain import Brain
import numpy as np

class Dino(GameObject):
    def __init__(self,genome):
        super().__init__()
        self.x = 200
        self.y = 450
        self.width = 80
        self.height = 86
        self.sprite_offset[0] = -4
        self.sprite_offset[1] = -2
        self.alive = True
        self.score = 0
        self.crouching = False
        self.jump_stage = 0
        self.sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
        self.game_sprites = {}
        self.load_sprites()
        self.sprite = self.game_sprites["walking_dino_1"]
        self.genome = None
        self.brain = Brain(genome)
        self.brain_inputs = np.zeros((7))
    
    def load_sprites(self):
        self.game_sprites = {}
        self.game_sprites["standing_dino"] = self.sprite_sheet.subsurface((1338, 2, 88, 94))
        self.game_sprites["walking_dino_1"] = self.sprite_sheet.subsurface((1514, 2, 88, 94))
        self.game_sprites["walking_dino_2"] = self.sprite_sheet.subsurface((1602, 2, 88, 94))
        self.game_sprites["dead_dino"] = self.sprite_sheet.subsurface((1690, 2, 88, 94))
        self.game_sprites["crouching_dino_1"] = self.sprite_sheet.subsurface((1866, 36, 118, 60))
        self.game_sprites["crouching_dino_2"] = self.sprite_sheet.subsurface((1984, 36, 118, 60))

    def update_brain_inputs(self,next_obstacle_info,speed):
        self.brain_inputs[0] = next_obstacle_info[0] / 900;                  
        self.brain_inputs[1] = (next_obstacle_info[1] - 450) / (1350 - 450)
        self.brain_inputs[2] = (next_obstacle_info[2] - 370) / (480 - 370) 
        self.brain_inputs[3] = (next_obstacle_info[3] - 30) / (146 - 30)    
        self.brain_inputs[4] = (next_obstacle_info[4] - 40) / (96 - 40)     
        self.brain_inputs[5] = (self.y - 278) / (484-278)                 
        self.brain_inputs[6] = (speed - 15) / (30 - 15)  

    def process_brain_output(self):
        if self.brain.outputs[0] != 0:
            if not self.crouching and not self.jumping():
                self.jump()
        if self.brain.outputs[1] == 0:
            if self.crouching:
                self.stop_crouching()
        else:
            if self.jumping():
                self.stop_jump()
            self.crouch()
            
    def display(self,screen):
        if self.alive:
            screen.blit(self.sprite, (self.x + self.sprite_offset[0], self.y + self.sprite_offset[1]))

    def f(self,x):
        return (-4 * x * (x - 1)) * 172
    
    def update(self,next_obstacle_info,speed):
        self.update_brain_inputs(next_obstacle_info, speed)
        self.brain.feed_forward(self.brain_inputs)
        self.process_brain_output()
        if self.jumping():
            self.update_jump()

    def jump(self):
        self.jump_stage = 0.0001
        self.sprite = self.game_sprites["walking_dino_1"]

    def stop_jump(self):
        self.jump_stage = 0
        self.y = 450
        self.sprite = self.game_sprites["walking_dino_1"]

    def update_jump(self):
        self.y = 450 - self.f(self.jump_stage)
        self.jump_stage += 0.03
        if self.jump_stage > 1:
            self.stop_jump()

    def jumping(self):
        return self.jump_stage > 0 

    def crouch(self):
        if not self.crouching:
            self.crouching = True
            self.y = 484
            self.width = 110
            self.height = 52
            self.sprite = self.game_sprites["crouching_dino_1"]
            
    def stop_crouching(self):
        self.crouching = False
        self.y = 450
        self.width = 80
        self.height = 86
        self.sprite = self.game_sprites["walking_dino_1"]

    def die(self,score):
        self.alive = False
        self.score = score

    def reset(self):
        self.alive = True
        self.score = 0







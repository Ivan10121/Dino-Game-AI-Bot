
import pygame
from dino import Dino
from enemy import Cactus, Bird
from ground import Ground
from GA import GeneticAlgorithm
import time
import random
import numpy as np

class Simulation:
    def __init__(self,screen):   
        self.screen = screen   
        self.Ndinos = 500
        self.GA = GeneticAlgorithm(self.Ndinos)
        self.genomes = self.GA.population
        self.dinos = [Dino(self.genomes[i]) for i in range(self.Ndinos)]
        self.enemies = []
        self.speed = 1000
        self.ground = Ground()
        self.score = 0 
        self.bestScore = 0
        self.generation = 1
        self.dinos_alive = 0
        self.MIN_SPAWN_MILLIS = 500
        self.MAX_SPAWN_MILLIS = 1500
        self.last_spawn_time = time.time() * 1000
        self.time_to_spawn = random.uniform(self.MIN_SPAWN_MILLIS, self.MAX_SPAWN_MILLIS)
        self.last_score_update = time.time() 


    def update(self,delta_time):
        if time.time() - self.last_score_update >= 0.1:  
            self.score += 1
            self.last_score_update = time.time()

        for dino in self.dinos:
            if dino.alive:
                dino.update(self.next_obstacle_info(dino),self.speed)

        for enemy in self.enemies:
            enemy.update(self.speed,delta_time)
            if enemy.is_offscreen():
                self.enemies.remove(enemy)

        if (time.time() * 1000 - self.last_spawn_time > self.time_to_spawn):
            self.spawn_enemy()
            self.last_spawn_time = time.time() * 1000
            self.time_to_spawn = random.uniform(self.MIN_SPAWN_MILLIS, self.MAX_SPAWN_MILLIS)

        self.ground.update(self.speed,delta_time)
        self.check_collisions()
        self.speed += 0.1

    def display(self):
        self.ground.display(self.screen)
        for enemy in self.enemies:
            enemy.display(self.screen)
        for dino in self.dinos:
            dino.display(self.screen)
        self.display_info()

    def display_info(self):
        font = pygame.font.Font(None, 36)  
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))  
        self.screen.blit(score_text, (10, 10))  
        best_score_text = font.render(f'Best score: {self.bestScore}', True, (0,0,0))
        self.screen.blit(best_score_text, (1050,10))
        generation_text = font.render(f'Generation: {self.generation}',True, (0,0,0))
        self.screen.blit(generation_text, (300, 10))  
        dinos_alive_text = font.render(f'Dinos alive: {self.dinos_alive}',True, (0,0,0))
        self.screen.blit(dinos_alive_text, (800, 10))  





    def spawn_enemy(self):
        if random.uniform(0,1) < 0.5:
            self.enemies.append(Cactus())
        else:
            self.enemies.append(Bird())

    def check_collisions(self):
        self.dinos_alive = 0
        for dino in self.dinos:
            for enemy in self.enemies:
                if dino.alive and dino.is_colliding(enemy):
                    dino.die(self.score)
                    pass
            if dino.alive:
                self.dinos_alive += 1
        if self.dinos_alive == 0:
            self.nextGeneration()
            

    def nextGeneration(self):
        self.generation += 1
        self.score = 0
        self.speed = 1000
        self.enemies.clear()
        self.GA.updateScore([dino.score for dino in self.dinos])  
        x = np.max(self.GA.score)
        if self.bestScore < x:
            self.bestScore = x
        self.genomes = self.GA.getNextGeneration1()
        for i in range(self.Ndinos):
            self.dinos[i].brain.genome = self.genomes[i]
            self.dinos[i].brain.update_weights()
            self.dinos[i].reset()

    def next_obstacle_info(self,dino):
        result = [1280, 0, 0, 0, 0]
        for enemy in self.enemies:
            if enemy.x > dino.x:
                result[0] = enemy.x - dino.x
                result[1] = enemy.x
                result[2] = enemy.y
                result[3] = enemy.width
                result[4] = enemy.height
                break
        return result
  
            



        


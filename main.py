from Game import Game
import pygame
from simulation import Simulation

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

game = Simulation(screen)

############# MAIN LOOP ###############
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(60) / 1000.0  # Tiempo en segundos


    screen.fill((255, 255, 255))  #white background            
    game.update(delta_time)
    game.display()
    pygame.display.flip()  


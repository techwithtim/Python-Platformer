import os 
import random 
import math 
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer Paul")

BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VELOCITY = 7

window = pygame.display.set_mode((WIDTH, HEIGHT))

def main(window):

    #set up fps and event quitting to end game upon user exit i.e. clicking 'x' button
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()

    pass

if __name__ == "__main__":
    main(window)
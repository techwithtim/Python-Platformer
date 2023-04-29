import os
import random
import math
import pygame
import numpy as np
import variables as var
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("PyGame")
window = pygame.display.set_mode((var.WIDTH, var.HEIGHT))


# generating the background
def generate_background(name):
    image = pygame.image.load(join(var.ASSETS_FOLDER_NAME, var.BACKGROUND_FOLDER_NAME, name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(var.WIDTH // width + 1):
        for j in range(var.HEIGHT // height + 1):
            # drawing background starts from top left corner, so here we should to know the position of each tile
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(window, background, bg_image):
    # drawing each tile by using its position from list of tuples 'background' including positions
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    random_image_id = random.randint(0, len(var.ARRAY_OF_ALL_BG_TILES)-1)
    print(random_image_id)
    background, bg_image = generate_background(var.ARRAY_OF_ALL_BG_TILES[random_image_id])

    run = True
    while run:
        clock.tick(var.FPS)

        # define to stop program when quit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_image)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main(window)
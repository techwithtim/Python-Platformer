import os
import random
import math
import pygame, sys
from os import listdir
from os.path import isfile, join
from Menu.menu_button import TextButton
from Game.game_button import GameButton
import game



pygame.init()

WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cute Platformer")
menu_background = pygame.image.load("assets/Background/Sky.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
game_screen = game.main


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def menu(window):
    run = True
    while run:
        window.blit(menu_background, (0,0))
     

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(55).render("CUTE PLATFORMER", True, "#d7fcd4")
        menu_rect = menu_text.get_rect(center=(500, 100))

        window.blit(menu_text, menu_rect)

        play_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            # if event.type == pygame.quit():
            #     pygame.quit()
            #     sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    print('PLAY GAME')
                    game_screen(window)
                if options_button.checkForInput(menu_mouse_pos):
                    print('OPTIONS')
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        # pygame.quit()
        # quit()
    

menu(window)
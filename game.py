import os
import random
import math
import pygame, sys
from os import listdir
from os.path import isfile, join
import Game.game_button
import Game.Classes.player
import Game.Classes.object
import Game.Functions.load
import Game.Functions.physics
from Menu.menu_button import TextButton

pygame.init()



WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
Player = Game.Classes.player.Player
Fire = Game.Classes.object.Fire
Block = Game.Classes.object.Block
get_background = Game.Functions.load.get_background
handle_move = Game.Functions.physics.handle_move
menu_background = pygame.image.load("assets/Background/Sky.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))


window = pygame.display.set_mode((WIDTH, HEIGHT))
menu_button = Game.game_button
pygame.display.set_caption("Cute Platformer")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
    
def draw(window, background, bg_image, player, objects, offset_x, menu_items):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    menu_items.draw(window)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    block_size = 96
    back_button_img = pygame.image.load("assets/Menu/Buttons/Back.png") 
    back_button = menu_button.GameButton(0,0, back_button_img, 2)
   
    
    player = Player(0, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH * 2 // block_size, (WIDTH * 2) // block_size)]
    # objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), 
    #            Block(block_size * 3, HEIGHT - block_size * 4, block_size),  
    #            Block(block_size * 4, HEIGHT - block_size * 4, block_size), fire]
    platforms = [Block(block_size * i+100, HEIGHT - block_size * 4, block_size) for i in range(10)]
    objects = [*floor, *platforms,  Block(0, HEIGHT - block_size * 2, block_size), fire]
   

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.draw(window) == True:
                    menu(window)

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, back_button)
        if player.rect.y > 700 :
            game_over(window)
        if player.health == 0:
            game_over(window)
        
        

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

def game_over(window):
    run = True
    while run:
        window.fill("BLACK")
        menu_text = get_font(55).render("GAME OVER", True, "#d7fcd4")
        menu_rect = menu_text.get_rect(center=(500, 100))
        menu_mouse_pos = pygame.mouse.get_pos()
        
        play_again_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        main_menu_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 400), 
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        window.blit(menu_text, menu_rect)
        
        for button in [play_again_button, main_menu_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)
        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.checkForInput(menu_mouse_pos):
                    main(window)
                if main_menu_button.checkForInput(menu_mouse_pos):
                    menu(window)
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    



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
           if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    print('PLAY GAME')
                    main(window)
                if options_button.checkForInput(menu_mouse_pos):
                    print('OPTIONS')
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        

# if __name__ == "__main__":
#     main(window)
menu(window)

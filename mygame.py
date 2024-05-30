import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("DEATH BY YOYO")

WIDTH = 1000
HEIGHT = 600
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join('assets', dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() //width): 
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites

BLACK = (0, 0, 0)


YOYO_VEL = 7
# GUY_WIDTH, GUY_HEIGHT = 200, 200

# GUY_ONE_IMAGE = pygame.image.load(os.path.join('assets', 'MainCharacters', 'YoyoGuy', 'fall.png'))
# GUY_ONE = pygame.transform.scale(GUY_ONE_IMAGE, (GUY_WIDTH, GUY_HEIGHT ))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0 , 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "YoyoGuy", 32, 32, True)
    ANIMATION_DELAY = 5
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel): 
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
              
    def move_right(self, vel): 
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        
    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.x_vel != 0:
            sprite_sheet = 'run'
            
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        spite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[spite_index]
        self.animation_count += 1
        self.update()
        
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win):
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

def get_background(name):
    image = pygame.image.load(join('assets', 'Background', name))
    _,_, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
            
    return tiles, image


# def handle_movement(keys_pressed, guy):
#     if keys_pressed[pygame.K_a]: #LEFT
#         guy.x -= PLAYER_VEL
#     elif keys_pressed[pygame.K_d]: #RIGHT
#         guy.x += PLAYER_VEL
        
def handle_move(player):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

        
def handle_yoyo(yoyo):
    for yoyo_throw in yoyo:
        yoyo_throw.x += YOYO_VEL
        if yoyo_throw.x > WIDTH:  # Remove yoyo if it goes off-screen
            yoyo.remove(yoyo_throw)


def draw_window(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    
    player.draw(window)
    
    # window.blit(GUY_ONE, (guy.x, guy.y))
    # for yoyo_throw in yoyo:
    #     pygame.draw.rect(window, BLACK, yoyo_throw)
        
    pygame.display.update()
        

# Event loop
def main():
    
    player = Player(100, 350, 50, 50)
    
    # Load music
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load("yoyo.wav")  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)
    
    background, bg_image = get_background('Purple.png')
    
    # guy = pygame.Rect(100, 300, GUY_WIDTH, GUY_HEIGHT)
    
    yoyo_throw = []
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Never go over the framerate
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit if the red button is clicked
                run = False
                
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LSHIFT:
            #         yoyo = pygame.Rect(guy.x + guy.width, guy.y + guy.height/2 - 2, 10, 5)
            #         yoyo_throw.append(yoyo)
                    
        player.loop(FPS)
        handle_move(player)
        # keys_pressed = pygame.key.get_pressed()
        # handle_movement(keys_pressed, guy)r
                
        handle_yoyo(yoyo_throw)
        
        draw_window(window, background, bg_image, player)
                
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main()
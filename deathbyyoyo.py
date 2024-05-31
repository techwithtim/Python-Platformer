import os
import random
import math
import pygame, sys
# from button import Button
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("DEATH BY YOYO")

WIDTH = 1000
HEIGHT = 600
FPS = 60
PLAYER_VEL = 5
YOYO_VEL = 7

window = pygame.display.set_mode((WIDTH, HEIGHT))

# For flipping character when moving left and right
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

def get_block(size):
    path = join('assets', "Terrain", 'MyTerrain.png')
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0 , 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "YoyoGuy", 32, 32, True)
    ANIMATION_DELAY = 3
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
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
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    def update_sprite(self):
        sprite_sheet = 'idle'
        
        if self.y_vel != 0:
            if self.jump_count == 1:
                sprite_sheet = 'jump'
        
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
        
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_background(name):
    image = pygame.image.load(join('assets', 'Background', name))
    _,_, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
            
    return tiles, image
        
        
def handle_verticle_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.ret.top = obj.rect.bottom
                player.hit_head()
                
        collided_objects.append(obj)
        
    return collided_objects
        
def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)
        
    handle_verticle_collision(player, objects, player.y_vel)
      
def handle_yoyo(yoyo):
    for yoyo_throw in yoyo:
        yoyo_throw.x += YOYO_VEL
        if yoyo_throw.x > WIDTH:  # Remove yoyo if it goes off-screen
            yoyo.remove(yoyo_throw)


def draw_window(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window)
    
    player.draw(window)
        
    pygame.display.update()
        


# Event loop
def main():
    
     # Load music
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load("assets/Music/dark.wav")  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)
    
    block_size = 96
    
    player = Player(100, 350, 50, 50)
    
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    background, bg_image = get_background('Test.png')
    
    yoyo_throw = []
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Never go over the framerate
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit if the red button is clicked
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LSHIFT:
            #         yoyo = pygame.Rect(guy.x + guy.width, guy.y + guy.height/2 - 2, 10, 5)
            #         yoyo_throw.append(yoyo)
                    
        player.loop(FPS)
        handle_move(player, floor)
                
        handle_yoyo(yoyo_throw)
        
        draw_window(window, background, bg_image, player, floor)
                
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main()
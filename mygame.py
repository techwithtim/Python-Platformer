import pygame
import os

WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Death By Yoyo")

BLACK = (0, 0, 0)

VEL = 5
FPS = 60
YOYO_VEL = 7
GUY_WIDTH, GUY_HEIGHT = 200, 200

GUY_ONE_IMAGE = pygame.image.load(os.path.join('assets', 'MainCharacters', 'YoyoGuy', 'fall.png'))
GUY_ONE = pygame.transform.scale(GUY_ONE_IMAGE, (GUY_WIDTH, GUY_HEIGHT ))

def handle_movement(keys_pressed, guy):
    if keys_pressed[pygame.K_a]: #LEFT
        guy.x -= VEL
    elif keys_pressed[pygame.K_d]: #RIGHT
        guy.x += VEL
    

def draw_window(guy, yoyo):
    window.fill((255, 200, 255))
    window.blit(GUY_ONE, (guy.x, guy.y))
    for yoyo_throw in yoyo:
        pygame.draw.rect(window, BLACK, yoyo_throw)
    pygame.display.update()
        
def handle_yoyo(yoyo):
    for yoyo_throw in yoyo:
        yoyo_throw.x += YOYO_VEL
        if yoyo_throw.x > WIDTH:  # Remove yoyo if it goes off-screen
            yoyo.remove(yoyo_throw)
        
# Event loop
def main():
    guy = pygame.Rect(100, 300, GUY_WIDTH, GUY_HEIGHT)
    
    yoyo_throw = []
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Never go over the framerate
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit if the red button is clicked
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    yoyo = pygame.Rect(guy.x + guy.width, guy.y + guy.height/2 - 2, 10, 5)
                    yoyo_throw.append(yoyo)
                
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, guy)
                
        handle_yoyo(yoyo_throw)
        
        draw_window(guy, yoyo_throw)
                
    pygame.quit()
    
if __name__ == "__main__":
    main()
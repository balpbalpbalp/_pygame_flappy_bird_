import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (576, 1024)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CLOCK = pygame.time.Clock()

game_font = pygame.font.Font(pygame.font.get_default_font(), 40)

gravity = 0.25

bird_movement = 0

game_activate = True

score = 0
high_score = 0

background_surface = pygame.image.load("assets/background-day.png").convert()
background_surface = pygame.transform.scale2x(background_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

def draw_floor():

    SCREEN.blit(floor_surface, (floor_x_position, 800))
    SCREEN.blit(floor_surface, (floor_x_position + 576, 800))

def create_pipe():

    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_position - 300))
    return bottom_pipe, top_pipe

def move_pipe(pipes):

    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    
    for pipe in pipes:

        if pipe.bottom >= 1024:

            SCREEN.blit(pipe_surface, pipe)
        
        else:

            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flip_pipe, pipe)

def check_collision(pipes):
    
    for pipe in pipes:

        if bird_rectangle.colliderect(pipe):
            
            return False
    
    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 800:

        return False
    
    return True

def rotate_bird(bird):

    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1)
    return new_bird

def bird_animation():
    
    new_bird = bird_frames[bird_index]
    new_bird_rectangle = new_bird.get_rect(center = (100, bird_rectangle.centery))
    return new_bird, new_bird_rectangle

def score_display(game_state):
    
    if game_state == "main_game":

        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center = (288, 100))
        SCREEN.blit(score_surface, score_rectangle)
    
    if game_state == "game_over":

        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center = (288, 100))
        SCREEN.blit(score_surface, score_rectangle)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rectangle = high_score_surface.get_rect(center = (288, 150))
        SCREEN.blit(high_score_surface, high_score_rectangle)

def update_score(score, high_score):

    if score > high_score:

        high_score = score
    
    return high_score

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center = (100, 512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rectangle = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
pipe_height = [500, 600, 700]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_surface_rectangle = game_over_surface.get_rect(center = (288, 512))

# flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_activate:

                bird_movement = 0
                bird_movement -= 10
                
                # flap_sound.play()
        
            if event.key == pygame.K_SPACE and game_activate == False:

                game_activate = True
                pipe_list.clear()
                bird_rectangle.center = (100, 512)
                bird_movement = 0
                score = 0
            
        if event.type == SPAWN_PIPE:
            
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:

            if bird_index < 2:

                bird_index += 1
            
            else:

                bird_index = 0
            
            bird_surface, bird_rectangle = bird_animation()

    SCREEN.blit(background_surface, (0, 0))

    if game_activate:

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rectangle.centery += bird_movement

        SCREEN.blit(rotated_bird, bird_rectangle)

        game_activate = check_collision(pipe_list)

        pipe_list = move_pipe(pipe_list)

        draw_pipe(pipe_list)

        score += 0.01
        score_display("main_game")
    
    else:

        SCREEN.blit(game_over_surface, game_over_surface_rectangle)
        high_score = update_score(score, high_score)
        score_display("game_over")

    floor_x_position -= 1
    draw_floor()

    if floor_x_position <= -576:

        floor_x_position = 0

    pygame.display.update()

    CLOCK.tick(120)
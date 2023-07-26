import pygame
import random
import os

# Inicializa o pygame
pygame.init()

# Cores
BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Dimensões da janela
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carrega imagens
dino_img = pygame.image.load(os.path.join("v2", "imagens", "dino.png"))
pipe_img = pygame.image.load(os.path.join("v2", "imagens", "pipe.png"))

# Define o tamanho do pássaro
BIRD_SIZE = (50, 40)


# Variáveis do jogo
dino_y = HEIGHT // 2
dino_dy = 0
gravity = 1
flap_power = -15
pipe_width = 50
gap_height = 200
pipe_x = WIDTH
pipe_height = random.randint(50, HEIGHT - gap_height - 50)
score = 0
font = pygame.font.SysFont('Arial', 32)

clock = pygame.time.Clock()

passed_pipe = False

def show_start_screen():
    screen.fill(BLUE)
    start_text = font.render("Aperte qualquer tecla para comecar", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen():
    screen.fill(BLUE)
    game_over_text = font.render("Voce perdeu :(", True, BLACK)
    restart_text = font.render("Aperte qualquer tecla para comecar!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

show_start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino_dy = flap_power

    # Lógica do jogo
    dino_dy += gravity
    dino_y += dino_dy
    pipe_x -= 5
    
    # Quando o pássaro passa o cano
    if pipe_x + pipe_width < 50 and not passed_pipe:
        score += 1
        passed_pipe = True
    
    if pipe_x + pipe_width < 0:
        pipe_x = WIDTH
        pipe_height = random.randint(50, HEIGHT - gap_height - 50)
        passed_pipe = False

    # Verificar colisões
    if dino_y < 0 or dino_y > HEIGHT or (pipe_x < 50 < pipe_x + pipe_width and (dino_y < pipe_height or dino_y > pipe_height + gap_height)):
        show_game_over_screen()
        dino_y = HEIGHT // 2
        dino_dy = 0
        pipe_x = WIDTH
        pipe_height = random.randint(50, HEIGHT - gap_height - 50)
        score = 0
        passed_pipe = False
        continue

    # Desenhar tudo
    screen.fill(BLUE)
    screen.blit(dino_img, (50, int(dino_y)))
    screen.blit(pipe_img, (pipe_x, 0))
    screen.blit(pipe_img, (pipe_x, pipe_height + gap_height))
    
    score_text = font.render(str(score), True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
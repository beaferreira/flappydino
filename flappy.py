import pygame, random
from pygame.locals import *

pygame.init()

#cores
BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#fonte
font = pygame.font.Font(pygame.font.get_default_font(), 20)

pontos = 0

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Dino(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('dino1.png').convert_alpha(),
                       pygame.image.load('dino2.png').convert_alpha(),
                       pygame.image.load('dino3.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('dino1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

dino_group = pygame.sprite.Group()
dino = Dino()
dino_group.add(dino)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

passed_pipe = False

def mostrar_pontos():
    pontos_texto = font.render(f"Pontos: {pontos}", True, BLACK)
    screen.blit(pontos_texto, (10, 10))

def show_start_screen():
    screen.fill(BLUE)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    start_text = font.render("Aperte qualquer tecla para começar", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def mostrar_pontos():
    pontos_texto = font.render(f"Pontos: {pontos}", True, BLACK)
    screen.blit(pontos_texto, (10, 10))

def show_game_over_screen():
    score_text = font.render(f"Pontuação final: {pontos}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + restart_text.get_height() // 2))
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    screen.fill(BLUE)
    game_over_text = font.render("Voce perdeu :(", True, BLACK)
    restart_text = font.render("Aperte qualquer tecla para comecar!", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - restart_text.get_height() // 2))
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

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                dino.bump()

    screen.blit(BACKGROUND, (0, 0))

     # Verificar se o dinossauro passou por um obstáculo
    if not passed_pipe and pipe_group.sprites()[0].rect[0] < dino.rect[0]:
        passed_pipe = True
        pontos += 1

    if (pygame.sprite.groupcollide(dino_group, ground_group, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(dino_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over
        show_game_over_screen()
        pontos = 0

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    dino_group.update()
    ground_group.update()
    pipe_group.update()

    dino_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(dino_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(dino_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over
        input()
        break
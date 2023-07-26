import pygame
import random
from pygame.locals import *

# Configurações
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED, GAME_SPEED, GRAVITY = 10, 200, 1
GROUND_WIDTH, GROUND_HEIGHT = 2 * SCREEN_WIDTH, 100
PIPE_WIDTH, PIPE_HEIGHT, PIPE_GAP = 80, 500, 200

pygame.init()

def load_image(filename, scale=None):
    img = pygame.image.load(filename).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = load_image('background.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Dino(pygame.sprite.Sprite):
    IMAGES = [load_image('dinoolhoaberto.png'),
              load_image('dinoolhoarregalado.png'),
              load_image('dinosemolho.png')]

    def __init__(self):
        super().__init__()
        self.current_image = 0
        self.image = self.IMAGES[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - GROUND_HEIGHT - 50))
        self.speed = SPEED

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.IMAGES[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):
    IMAGE = load_image('pipe-red.png', (PIPE_WIDTH, PIPE_HEIGHT))

    def __init__(self, inverted, xpos, ysize):
        super().__init__()
        self.image = Pipe.IMAGE.copy()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = -self.rect[3] + ysize if inverted else SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    IMAGE = load_image('base.png', (GROUND_WIDTH, GROUND_HEIGHT))

    def __init__(self, xpos):
        super().__init__()
        self.image = Ground.IMAGE
        self.rect = self.image.get_rect(topleft=(xpos, SCREEN_HEIGHT - GROUND_HEIGHT))

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    return Pipe(False, xpos, size), Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)

dino_group = pygame.sprite.GroupSingle(Dino())
ground_group = pygame.sprite.Group(Ground(x) for x in [0, GROUND_WIDTH])
pipe_group = pygame.sprite.Group(pipe for _ in range(2) for pipe in get_random_pipes(SCREEN_WIDTH * _ + 800))

game_started = False
if not game_started:
    pygame.time.wait(3000)  # 3 segundos de delay
    game_started = True


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            dino_group.sprite.bump()

    # Atualização da lógica do jogo
    dino_group.update()
    ground_group.update()
    pipe_group.update()

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[:2])
        pipe_group.add(*get_random_pipes(SCREEN_WIDTH * 2))

    # Renderização
    screen.blit(BACKGROUND, (0, 0))
    pipe_group.draw(screen)
    ground_group.draw(screen)
    dino_group.draw(screen)

    pygame.display.flip()

    if game_started and (pygame.sprite.groupcollide(dino_group, ground_group, False, False, pygame.sprite.collide_mask) or
    pygame.sprite.groupcollide(dino_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        
        pygame.time.wait(2000)
        running = False

pygame.quit()

import pygame, random
from pygame.locals import *

#principais variáveis
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
GAME_SPEED = 200
GRAVITY = 1

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

#colocando o dinossauro
class Dino(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #definindo as expressões do dinossauro
        self.images = [pygame.image.load('dinoolhoaberto.png').convert_alpha(),
                       pygame.image.load('dinoolhoarregalado.png').convert_alpha(),
                       pygame.image.load('dinosemolho.png').convert_alpha()]

        self.speed = SPEED

        #definindo o ciclo das imagens
        self.current_image = 0

        self.image = pygame.image.load('dinoolhoaberto.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)



        self.rect = self.image.get_rect()
        #posicionando ele na tela
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    #definindo o ciclo das imagens

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY
        
    # definindo a altura que o dino vai cair
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

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

        #irá definir tanto a velocidade do chão quanto dos canos
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


pygame.init()
#criando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#colocando o background
BACKGROUND = pygame.image.load('background.png')
#escalando para que a imagem fique do tamanho da tela
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

#mostrar o dinossauro na tela
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


#ajustando a velocidade das expressoes
clock = pygame.time.Clock()

#laço principal do jogo
while True:

    clock.tick(3)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                dino.bump()

    screen.blit(BACKGROUND, (0, 0))

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

    if  (pygame.sprite.groupcollide(dino_group, ground_group, False, False, pygame.sprite.collide_mask)) or
        (pygame.sprite.groupcollide(dino_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        input()
        #gameover
        break

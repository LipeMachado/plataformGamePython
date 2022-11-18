import os.path

import pygame

# iniciar o pygame
pygame.init()

# criando janela e definindo tamanho da tela
width, height = 1200, 700
surface = pygame.display.set_mode((width, height))

# Mudar título da janela
pygame.display.set_caption('Cold Adventures')

#Assets
#assets = os.path.join(os.getcwd(), 'Assets')
#dirt = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'dirt.png')), (50, 50))

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# renderizar objetos na tela

#Desenhando Tile Map

tile_map = [
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '........................',
    '.........XXXXXXX........',
    '........................',
    'XXXXXXXXX.......XXXXXXXX',
    'XXXXXXXXXXX...XXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXX',
]

#Colisão do Player

def colliding(rect1, rect2):
    if not(rect1.x + rect1.width <= rect2.x or rect2.x + rect2.width <= rect1.x):
        if not(rect1.y + rect1.height <= rect2.y or rect2.y + rect2.height <= rect1.y):
            return True
    return False

#Criação do Player
class Character:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def would_collide(self, x, y, current_map):
        character_rect = pygame.Rect(self.x + x, self.y + y, self.width, self.height)

        for y in range(len(current_map)):
            for x in range(len(current_map[y])):
                if current_map[y][x] == 'X':
                    rect = pygame.Rect(x * 50, y * 50, 50, 50)
                    if colliding(character_rect, rect):
                        return True
        return False

class Player(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 0.5)
        self.jumping = False
        self.falling = False
        self.max_jumps = 300
        self.jumps_left = self.max_jumps

    def handle_movement(self, key):
        if self.jumping:
            if not(self.would_collide(0, -self.speed, tile_map)) and self.jumps_left != 0:
                self.y -= self.speed
            else:
                self.jumping = False
                self.falling = True
                self.jumps_left = self.max_jumps
            self.jumps_left -= 1

        if not(self.would_collide(0, self.speed, tile_map)) and not(self.jumping):
            self.falling = True
            self.y += self.speed
        else:
            self.falling = False

        if key[pygame.K_a] and not(self.would_collide(-self.speed, 0, tile_map)):
            self.x -= self.speed

        if key[pygame.K_d] and not(self.would_collide(self.speed, 0, tile_map)):
            self.x += self.speed

        if key[pygame.K_w] and not(self.jumping) and not (self.falling):
            self.jumping = True

#Desenhando mapa e colocando player
def draw_window(current_map, player):
    surface.fill(BLACK)

    #Desenhando Mapa
    for y in range(len(current_map)):
        for x in range(len(current_map[y])):
            if current_map[y][x] == 'X':
                #Renderizando Mapa por cor
                rect = pygame.Rect(x * 50, y * 50, 50, 50)
                pygame.draw.rect(surface, WHITE, rect)

    #Colocando Player
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    pygame.draw.rect(surface, RED, player_rect)

    pygame.display.update()

# Rodar Loop principal até o jogador fechar
def main():
    run_game = True
    clock = pygame.time.Clock()
    fps = 60

    player = Player(50, 500, 50, 50)

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        key_pressed = pygame.key.get_pressed()
        player.handle_movement(key_pressed)

        draw_window(tile_map, player)


if __name__ == '__main__':
    main()

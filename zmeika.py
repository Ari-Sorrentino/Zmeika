from pygame import *
from random import *
from time import time as timer

main_win = display.set_mode((750, 500))
display.set_caption("Змейка")

background = transform.scale(image.load("background.jpg"), (750, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__(player_image, player_x, player_y)
        self.dx = 50
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.dy == 0:
            self.dx = 0
            self.dy = -50
        elif keys[K_DOWN] and self.dy == 0:
            self.dx = 0
            self.dy = 50
        elif keys[K_LEFT] and self.dx == 0:
            self.dx = -50
            self.dy = 0
        elif keys[K_RIGHT] and self.dx == 0:
            self.dx = 50
            self.dy = 0

head = Snake("head.png", 200, 250)

clock = time.Clock()
game = True
finish = False
walking_timer = timer()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        current_timer = timer()
        main_win.blit(background, (0, 0))
        head.get_direction()

        if current_timer - walking_timer >= 0.5:
            head.update()
            walking_timer = timer()
        
        head.draw()

    display.update()
    clock.tick(60)

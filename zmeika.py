from pygame import *
from random import *
from time import time as timer

main_win = display.set_mode((700, 500))
display.set_caption("Змейка")

background = transform.scale(image.load("background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

head = GameSprite("head.png", 350, 250)
clock = time.Clock()
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        main_win.blit(background, (0, 0))
        head.draw()

    display.update()
    clock.tick(60)
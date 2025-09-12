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
        for i in range(len(snake) - 1, 0, -1):
            snake[i].rect.x = snake[i - 1].rect.x
            snake[i].rect.y = snake[i - 1].rect.y

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x > 700:
            self.rect.x = 0

        if self.rect.x < 0:
            self.rect.x = 700

        if self.rect.y < 0:
            self.rect.y = 450

        if self.rect.y > 450:
            self.rect.y = 0

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

class Apple(GameSprite):
    def __init__(self, player_image):
        super().__init__(player_image, 0, 0)
        self.respawn()

    def respawn(self):
        self.rect.x = randrange(0, 700, 50)
        self.rect.y = randrange(0, 450, 50)

class BadApple(GameSprite):
    def __init__(self, player_image):
        super().__init__(player_image, 0, 0)
        self.respawn()

    def respawn(self):
        self.rect.x = randrange(0, 700, 50)
        self.rect.y = randrange(0, 450, 50)

class GoldenApple(GameSprite):
    def __init__(self, player_image):
        super().__init__(player_image, 0, 0)
        self.respawn()

    def respawn(self):
        self.rect.x = randrange(0, 700, 50)
        self.rect.y = randrange(0, 450, 50)

def load_record():
    try:
        with open("record.txt", "r") as file:
            return(int(file.read()))

    except:
        return 0

def save_record(value):
    with open("record.txt", "w") as file:
        file.write(str(value))

head = Snake("head.png", 200, 250)
apple = Apple("apple.png")
bad_apple = BadApple("heaviest_thing_ever.png")
golden_apple = GoldenApple("golden_apple.png")
snake = [head]

clock = time.Clock()
record = load_record()
score = 0
game = True
finish = False
walking_timer = timer()
font.init()
font_1 = font.Font(None, 50)
font_2 = font.Font(None, 35)

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
    
            if head.rect.colliderect(apple.rect):
                score += 1
                main_win.blit(score_text, (50, 50))
                apple.respawn()
                last_part = snake[-1]
                x_part2, y_part2 = last_part.rect.x, last_part.rect.y

                if head.dx > 0:
                    x_part2 -= 50
                elif head.dx < 0:
                    x_part2 += 50
                elif head.dy > 0:
                    y_part2 -= 50
                elif head.dy < 0:
                    y_part2 += 50

                new_part = Snake("square.png", x_part2, y_part2)
                snake.append(new_part)

            if head.rect.colliderect(bad_apple.rect):
                score -= 5
                bad_apple.respawn()
                if len(snake) > 1:
                    last_part = snake[-1]
                    snake.remove(last_part)

            if head.rect.colliderect(golden_apple.rect):
                score += 5
                main_win.blit(score_text, (50, 50))
                golden_apple.respawn()
                last_part = snake[-1]
                x_part2, y_part2 = last_part.rect.x, last_part.rect.y

                if head.dx > 0:
                    x_part2 -= 50
                elif head.dx < 0:
                    x_part2 += 50
                elif head.dy > 0:
                    y_part2 -= 50
                elif head.dy < 0:
                    y_part2 += 50

                new_part = Snake("square.png", x_part2, y_part2)
                snake.append(new_part)

                last_part = snake[-1]
                x_part2, y_part2 = last_part.rect.x, last_part.rect.y

                if head.dx > 0:
                    x_part2 -= 50
                elif head.dx < 0:
                    x_part2 += 50
                elif head.dy > 0:
                    y_part2 -= 50
                elif head.dy < 0:
                    y_part2 += 50

                new_part = Snake("square.png", x_part2, y_part2)
                snake.append(new_part)

            walking_timer = timer()

        for part in snake[1:]:
            if head.rect.colliderect(part.rect):
                finish = True
                main_win.blit(lose_text, (400, 250))
                if score > record:
                    record = score
                    save_record(record)
                    
        apple.draw()
        bad_apple.draw()
        golden_apple.draw()
        for part in snake:
                part.draw()

        if score < 0:
            finish = True
            main_win.blit(lose_text, (400, 250))

        lose_text = font_1.render("You lost!", 1, (255, 0, 0))
        score_text = font_2.render("Счёт: " + str(score), 1, (0, 200, 0))
        main_win.blit(score_text, (50, 50))
        record_text = font_2.render("Рекорд: " + str(record), 1, (0, 200, 0))
        main_win.blit(record_text, (50, 75))

    display.update()
    clock.tick(60)

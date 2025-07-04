#Создай собственный Шутер!

from pygame import *
import random
import math
global number
#создай игру "Лабиринт"!

font.init()
font = font.SysFont('Arial', 100)
win = font.render('YOU WIN!', True, (255, 0, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 255))
win_height = 1000
win_width = 1500
window = display.set_mode((win_width, win_height))
score = 0
lives = 3

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire = mixer.Sound('fire.ogg')
display.set_caption("Шутер")

galaxy = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.fire_count = 0
        self.reloading = False
        self.reload_time = 0
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if self.reloading:
            self.reload_time += 1
            if self.reload_time >= 120:  # 2 секунды (60 FPS)
                self.reloading = False
                self.reload_time = 0
    def fire(self):
        if not self.reloading:
            bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 10, 15, 20)
            bullets.add(bullet)
            fire.play()
            self.fire_count += 1
            if self.fire_count >= 5:
                self.reloading = True
                self.fire_count = 0



lost = 0

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed_range, width, height):
        speed = random.uniform(*speed_range)
        super().__init__(player_image, player_x, player_y, speed, width, height)
        self.alive = True


    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(80, win_width - 80)
            lost = lost + 1


class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    





        



rocket = Player('rocket.png', win_width // 2, win_height - 100, 10, 65, 110)
enemies = sprite.Group() 
bullets = sprite.Group()
asteroids = sprite.Group()

max_enemies = 5
max_asteroids = 2

for e in range(max_enemies):
    enemy = Enemy('ufo.png', 
    random.randint(0, win_width - 130), random.randint(-200, -50), (2, 5), 110, 65)
    enemies.add(enemy)

for a in range(max_asteroids):
    asteroid = Asteroid('asteroid.png',
    random.randint(0, win_width - 130), random.randint(-500, -100), 3, 110, 65)
    asteroids.add(asteroid)


max_lost = 5
max_score = 10

clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        window.blit(galaxy, (0, 0))
        rocket.reset()
        rocket.update()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

    #Столкновения ракеты с врагами
    sprites_list = sprite.spritecollide(rocket, enemies, False)
    for enemy in sprites_list:
        if lives > 0:
            lives -= 1
            enemy.kill()
        if lives <= 0:
            finish = True
            window.blit(lose, (win_width // 2 - 200, win_height // 2 - 50))
    #Столкн пуль с врагами
    sprites_list = sprite.groupcollide(enemies,bullets, True, True)
    if len(sprites_list) > 0:
        score += len(sprites_list)
    
    #Столкн ракеты с астероидами
    sprites_list = sprite.spritecollide(rocket, asteroids, False)
    for asteroid in sprites_list:
        if lives > 0:
            lives -= 1
            asteroid.kill()
        if lives <= 0:
            finish = True
            window.blit(lose, (win_width // 2 - 200, win_height // 2 - 50))


    
    while len(enemies) < max_enemies:
        enemy = Enemy('ufo.png', 
        random.randint(0, win_width - 130), random.randint(-200, -50), (2, 5), 110, 65)
        enemies.add(enemy)

    while len(asteroids) < max_asteroids:
        asteroid = Asteroid('asteroid.png',
        random.randint(0, win_width - 130), random.randint(-500, -100), 3, 110, 65)
        asteroids.add(asteroid)

    if lost >= max_lost:
        finish = True
        window.blit(lose, (win_width // 2 - 200, win_height // 2 - 50))
    
    if score >= max_score:
        finish = True
        window.blit(win, (win_width // 2 - 200, win_height // 2 - 50))
    
    lost_text = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
    window.blit(lost_text, (1, 1))
    score_text = font.render("Счёт:" + str(score), 1, (255, 255, 255))
    window.blit(score_text, (1, 80))
    lives_text = font.render("Жизни:" + str(lives), 1, (255, 255, 255))
    window.blit(lives_text, (1, 160))


    if rocket.reloading:
        reload_text = font.render("Wait, reload", True, (255, 255, 255))
        window.blit(reload_text, (win_width // 2 - 150, win_height - 100))

        
    display.update()
    clock.tick(FPS)
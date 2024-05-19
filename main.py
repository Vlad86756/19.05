from random import randint

from pygame import *
from time import time as timer
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

img_back = "3d1b18dc51.png"
img_hero = "завантаження-removebg-preview (2).png"
img_bullet = "bullet.png"
img_enemy = "lohik.png"
img_hero2 = "rocket2-removebg-preview.png"
score = 0
lost = 0
max_lost = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 10, -15)
        bullets.add(bullet)
class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 10, -15)
        bullets2.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -50
            lost += 1
ship = Player(img_hero, 600, win_height - 80, 80, 100, 10)
ship2 = Player2(img_hero2, 5, win_height - 80, 50, 100, 10)
bullets = sprite.Group()
bullets2 = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(50, win_width-80), -60, 80, 80, randint(2, 5))
    monsters.add(monster)
mixer.init()
mixer.music.load("dist_space (1).ogg")
mixer.music.play()
fire_sound = mixer.Sound("dist_fire.ogg")

font.init()
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 36)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (255, 0, 0))

background = transform.scale(image.load(img_back), (win_width, win_height))
finish = False
run = True
goal = 15
life = 3
max_fire = 5
real_time = False
num_fire = 0
real_time2 = False
num_fire2 = 0

show_menu = True
show_game = False
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, True, color)
    text_rect = text_object.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_object, text_rect)
while run:
    if show_menu:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if 260 <= mouse_pos[0] <= 380 and 160 <= mouse_pos[1] <= 200:
                    background = background
                    show_menu = False
                    show_game = True
                if 260 <= mouse_pos[0] <= 380 and 220 <= mouse_pos[1] <= 270:
                    run = False
                    show_menu = False
            mouse_pos = mouse.get_pos()
            font3 = font.Font(None, 50)
            window.blit(background, (0, 0))
            if 260 <= mouse_pos[0] <= 400 and 160 <= mouse_pos[1] <= 210:
                draw_text("Play", font3, (255, 0, 0), window, 330, 200)
                if mouse.get_pressed()[0]:
                    selected = "Play"
            else:
                draw_text("Play", font3, (255, 255, 255), window, 330, 200)
            if 260 <= mouse_pos[0] <= 380 and 220 <= mouse_pos[1] <= 270:
                draw_text("Exit", font3, (255, 0, 0), window, 330, 250)
                if mouse.get_pressed()[0]:
                    selected = "Exit"
            else:
                draw_text("Exit", font3, (255, 255, 255), window, 330, 250)
    if show_game:
            for e in event.get():
                if e.type == QUIT:
                    run = False
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        if num_fire < max_fire and real_time == False:
                            num_fire += 1
                            fire_sound.play()
                            ship.fire()
                        if num_fire >= max_fire and real_time == False:
                            last_time = timer()
                            real_time = True
                    if e.key == K_b:
                        if num_fire2 < max_fire and real_time2 == False:
                            num_fire2 += 1
                            fire_sound.play()
                            ship2.fire()
                        if num_fire2 >= max_fire and real_time2 == False:
                            last_time2 = timer()
                            real_time2 = True
            if not finish:
                window.blit(background, (0,0))
                ship.update()
                ship2.update()
                bullets.update()
                bullets2.update()
                monsters.update()
                text = font2.render("Рахунок: "+ str(score), True, (255, 255, 255))
                window.blit(text, (10, 20))
                text_lose = font2.render("Пропущено: "+ str(lost), True, (255, 255, 255))
                window.blit(text_lose, (10, 50))
                ship.reset()
                ship2.reset()
                bullets.draw(window)
                bullets2.draw(window)
                monsters.draw(window)
                collides = sprite.groupcollide(monsters, bullets, True, True)
                for c in collides:
                    score += 1
                    monster = Enemy(img_enemy, randint(50, win_width-80), -60, 80, 50, randint(1, 5))
                    monsters.add(monster)
                collides2 = sprite.groupcollide(monsters, bullets2, True, True)
                for c in collides2:
                    score += 1
                    monster = Enemy(img_enemy, randint(50, win_width - 80), -60, 80, 50, randint(1, 5))
                    monsters.add(monster)
                if real_time == True:
                    now_time = timer()
                    if now_time - last_time < 3:
                        reload = font2.render("Wait, reload...", True, (255,0,0))
                        window.blit(reload, (440, 460))
                    else:
                        real_time = False
                        num_fire = 0
                if real_time2 == True:
                    now_time2 = timer()
                    if now_time2 - last_time2 < 3:
                        reload = font2.render("Wait, reload...", True, (255,0,0))
                        window.blit(reload, (60, 460))
                    else:
                        real_time2 = False
                        num_fire2 = 0
                if life == 3:
                    life_color = (0, 150, 0)
                if life == 2:
                    life_color = (150, 150, 0)
                if life == 1:
                    life_color = (150, 0, 0)
                text_life = font1.render(str(life), True, life_color)
                window.blit(text_life, (650, 10))
                if sprite.spritecollide(ship, monsters, False):
                    sprite.spritecollide(ship, monsters, True)
                    life -=1
                if life == 0 or lost >= max_lost:
                    finish = True
                    window.blit(lose, (200, 200))
                if score >= goal:
                    finish = True
                    window.blit(win, (200, 200))
            else:
                time.delay(3000)
                score = 0
                lost = 0
                life = 3
                num_fire = 0
                finish = False
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                for i in range(1, 6):
                    monster = Enemy(img_enemy, randint(50, win_width-80), -60, 80, 50, randint(1, 5))
                    monsters.add(monster)
    display.update()
    time.delay(50)
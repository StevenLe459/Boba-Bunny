# Music: asianoriental1.ogg by Tozan <https://opengameart.org/content/asianoriental1> licensed under cc0
# Import statements
import pygame
import random
from os import path

# Global variables and constants
WIDTH = 800 # Width of screen
HEIGHT = 800 # Height of screen
FPS = 60 # Frames per second
BLACK = (0, 0, 0)
score = 0 # Player's score
health = 10 # Player's health
src_path = path.join(path.dirname(__file__), 'src')
font_name = pygame.font.match_font('arial')
file = open(path.join(src_path, "highScore.txt"), "r+")
high_score = int(file.read())

# Define classes
class BobaBunny(pygame.sprite.Sprite): # Main player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boba_bunny_img
        self.rect = self.image.get_rect()
        self.radius = 75
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    def update(self):
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speedx = -8
        if key_state[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        bullet = BobaPearl(self.rect.centerx - 25, self.rect.top)
        all_sprites.add(bullet)
        boba_pearls.add(bullet)
class SauRieng(pygame.sprite.Sprite): # Enemy sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sau_rieng_image
        self.rect = self.image.get_rect()
        self.radius = 50
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.x < -25 or self.rect.x > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
class BobaPearl(pygame.sprite.Sprite): # Bullet sprite
    def __init__(self ,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boba_pearl_image
        self.rect = self.image.get_rect()
        self.radius = 8
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class TraiHong(pygame.sprite.Sprite): # Power-up sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = trai_hong_image
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.x < -25 or self.rect.x > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Define functions
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def record_score(score):
    global high_score
    if score > high_score:
        high_score = score
        file.write(str(score))

# Initialize pygame and create window
pygame.init()
pygame.mixer.init() # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boba Bunny")

# Initialize graphics
background = pygame.image.load(path.join(src_path, "background.png"))
background = pygame.transform.scale(background, (800, 800))
background_rect = background.get_rect()
menu = pygame.image.load(path.join(src_path, "mainMenu.png"))
menu = pygame.transform.scale(menu, (800, 800))
menu_rect = menu.get_rect()
boba_bunny_img = pygame.image.load(path.join(src_path, "bobaBunny.png"))
boba_bunny_img = pygame.transform.rotozoom(boba_bunny_img, 0, 0.4)
sau_rieng_image = pygame.image.load(path.join(src_path, "sauRieng.png"))
sau_rieng_image = pygame.transform.rotozoom(sau_rieng_image, 0, 0.08)
boba_pearl_image = pygame.image.load(path.join(src_path, "bobaPearl.png"))
boba_pearl_image = pygame.transform.rotozoom(boba_pearl_image, 0, 0.03)
trai_hong_image = pygame.image.load(path.join(src_path, "traiHong.png"))
trai_hong_image = pygame.transform.rotozoom(trai_hong_image, 0, 0.05)

# Initialize sounds and music
pygame.mixer.music.load(path.join(src_path, 'music.ogg'))

# Initialize clock
clock = pygame.time.Clock()

# Play music
pygame.mixer.music.play(loops=-1)

# Define screen function
def main_menu():
    screen.blit(menu, menu_rect)
    draw_text(screen, "High Score: " + str(high_score), 24, WIDTH / 6, HEIGHT * 2 / 3)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_RETURN]:
                waiting = False

#Game loop
running = True
show_screen = True
while running:
    if show_screen:
        main_menu()
        show_screen = False
        all_sprites = pygame.sprite.Group()
        sau_rieng = pygame.sprite.Group()
        boba_pearls = pygame.sprite.Group()
        trai_hong = pygame.sprite.Group()
        boba_bunny = BobaBunny()
        all_sprites.add(boba_bunny)
        th = TraiHong()
        all_sprites.add(th)
        trai_hong.add(th)
        for i in range(8):
            sr = SauRieng()
            all_sprites.add(sr)
            sau_rieng.add(sr)
        score = 0
        health = 10
    # Keeps loop running at the right speed
    clock.tick(FPS)
    #Process inputs and events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Checks for closing window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                boba_bunny.shoot()
    #Update
    all_sprites.update()
    # Checks for boba pearl-durian collision
    hits = pygame.sprite.groupcollide(sau_rieng, boba_pearls, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        sr = SauRieng()
        all_sprites.add(sr)
        sau_rieng.add(sr)
        score += 100
    # Checks for bunny-durian collision
    hits = pygame.sprite.spritecollide(boba_bunny, sau_rieng, True, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            sr = SauRieng()
            all_sprites.add(sr)
            sau_rieng.add(sr)
            health -= 1
    # Checks for bunny-persimmon collision
    hits = pygame.sprite.spritecollide(boba_bunny, trai_hong, True, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            tr = TraiHong()
            all_sprites.add(tr)
            trai_hong.add(tr)
            health += 1
    if health == 0:
        show_screen = True
        record_score(score)
    #Draw/render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Health: " + str(health), 24, 3 * WIDTH / 4, HEIGHT - 100)
    draw_text(screen, "Score: " + str(score), 24, 3 * WIDTH / 4, HEIGHT - 50)
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()

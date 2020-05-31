import pygame, sys, random
from pygame import mixer

# Initalize
pygame.init()
WIDTH = 900
HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()

# define colors(RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load("background1.png")
# background position
backgroundX = 0
backgroundY = 0

# Title and Icon (później się zmieni :D)
pygame.display.set_caption("nazwa")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Load all sounds
explosion_sound = mixer.Sound("wybuch_gracza.wav")
bullet_sound = mixer.Sound("pocisk.wav")

# music
#mixer.music.load("muzyczka.wav")
#samixer.music.play(0)

# Load all images (później się zmieni 😀 )
bulletImg = pygame.image.load("pocisk.png")
playerImg = pygame.image.load("player.png")
ship_monsterImg = pygame.image.load("enemy9.png")
ship_monster_bulletImg = pygame.image.load("fire.png")
cthulhuImg = pygame.image.load("enemy3.png")
lobsterImg = pygame.image.load("enemy4.png")
snakeImg = pygame.image.load("enemy5-0.png")
snakeImg2 = pygame.image.load("enemy5-1.png")


# explosion animation
explosion_anin = {}
# lista z grafikami dużymi
explosion_anin["lg"] = []
# lista z grafikami małymi
explosion_anin["sm"] = []

# dodajemy 5 grafik do ich list
for i in range(4):
    filename = "eksplozja{}.png".format(i)
    img = pygame.image.load(filename)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anin["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (35, 35))
    explosion_anin["sm"].append(img_sm)


# PLAYER
class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg

        #         tworze prostokąt, żeby łatwiej nim manipulować (rect. = rectangle)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT / 2

        #         to jest taki jakby jak hit box w kształcie okręgu, łatwiej dzięki temu dopracować kolizje
        self.radius = 12
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.speedX = 0
        self.speedY = 0

        #         poziom osłony
        self.shield = 100

    def update(self):
        # Movement
        self.speedX = 0
        self.speedY = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.rect.x -= 3
        if keystate[pygame.K_d]:
            self.rect.x += 3
        if keystate[pygame.K_s]:
            self.rect.y += 3
        if keystate[pygame.K_w]:
            self.rect.y -= 3

        # Creat the Boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.right - 2, self.rect.bottom - 6)
        all_sprites_group.add(bullet)
        bullets_group.add(bullet)


# pociski gracza
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImg, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.radius = 5
        bullet_sound.play()
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)

    def update(self):
        self.rect.x += 17
        # kill if it moves off the screen
        if self.rect.left > WIDTH:
            self.kill()


# Ship Monster
class Ship_monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship_monsterImg
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 12)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.x = random.randint(1000, 20000)
        self.rect.y = random.randint(100, HEIGHT - 200)
        # poziom osłony
        self.shield = 100
        self.speedX = 0
        # wskaźnik gotowości do strzału
        self.ready_to_fire = True
        # zmienna decydująca czy strzela
        self.madness = 0

    def update(self):
        self.rect.x -= 1.5

    def shoot(self, x, y):
        # add to the Ship_monster_bullet class
        ship_monster_bullet = Ship_monster_bullet(x, y)
        all_sprites_group.add(ship_monster_bullet)
        enemies_group.add(ship_monster_bullet)


# pociski Ship Monstera
class Ship_monster_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship_monster_bulletImg
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.radius = 10
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)

    def update(self):
        self.rect.x -= 8
        # kill if it moves off the screen
        if self.rect.right < 0:
            self.kill()


#  Cthulhu
class Cthulhu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cthulhuImg
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.x = random.randint(1000, 5000)
        self.rect.y = random.randint(20, 500)
        # poziom osłony przeciwnika
        self.shield = 100

    def update(self):
        self.rect.x -= 3


#  Lobster
class Lobster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = lobsterImg
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 12)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        # self.rect.x = random.randint(1000, 1500)
        # self.rect.y = random.randint(50, HEIGHT - 50)
        self.rect.x = random.randint(1000, 3000)
        self.rect.y = -90
        # poziom osłony przeciwnika
        self.shield = 100
        self.speedY = 0
        self.speedX = -1

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # kiedy gracz znajdzie się pod nim atakuje
        if self.rect.x - player.rect.x < 90:
            self.speedY = 6
            self.speedX = -2

# Snake
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snakeImg
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 12)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        # self.rect.x = random.randint(1000, 1500)
        # self.rect.y = random.randint(50, HEIGHT - 50)
        self.rect.x = random.randint(1000, 3000)
        self.rect.y = 500
        # poziom osłony przeciwnika
        self.shield = 100
        self.speedY = 0
        self.speedX = -1

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # kiedy gracz znajdzie się pod nim atakuje
        if self.rect.x - player.rect.x < 90:
            self.speedY = -6
            self.speedX = -2

            if self.image == snakeImg2:
                self.image = snakeImg
            else:
                self.image = snakeImg2


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anin[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        #         zmiana klatek (grafik)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anin[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anin[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Create sprites group
all_sprites_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
lobsters_group = pygame.sprite.Group()
ship_monsters_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()

# add player to class and sprite
player = Player()
all_sprites_group.add(player)

# add Ship Monster to his sprite and class
num_of_ship_monster = 50
ship_monster = Ship_monster()

ship_monsters_list = []
for i in range(num_of_ship_monster):
    ship_monster_i = Ship_monster()
    ship_monsters_list.append(ship_monster_i)

for item in ship_monsters_list:
    enemies_group.add(item)
    all_sprites_group.add(item)
    ship_monsters_group.add(item)

# add Cthulhu to his sprite and class
num_of_cthulhu = 10
for i in range(num_of_cthulhu):
    ct = Cthulhu()
    all_sprites_group.add(ct)
    enemies_group.add(ct)

# add Lobster to his sprite and class
num_of_lobsters = 10
for i in range(num_of_lobsters):
    lo = Lobster()
    all_sprites_group.add(lo)
    lobsters_group.add(lo)

# add snake to his sprite and class
num_of_snakes = 10
for i in range(num_of_snakes):
    sn = Snake()
    all_sprites_group.add(sn)
    lobsters_group.add(sn)

# Game Loop (wykonuje się, dopóki program jest włączony)
while True:
    # keep loop running at the right speed
    clock.tick(FPS)

    # CHECKING INPUTS
    for event in pygame.event.get():
        # jeśli wydardzenie to "wyjście -> wyłącz program"
        if event.type == pygame.QUIT:
            sys.exit(0)
        # jeśli wydarzenie to wcziśniecie klawisza
        if event.type == pygame.KEYDOWN:
            # jeśli wciśnęty kalawisz to espace -> wyłącz program
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)

            #  jeśli naciśnięto spacje, player uruchamia metodę shoot
            if event.key == pygame.K_SPACE:
                player.shoot()

    # UPDATE
    # odświerza wszystkie elementy znajdujące się w grupię all_sprites (wszystko)
    all_sprites_group.update()

    # chceck to see if bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(hit.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

    # chceck to see if bullet hit a lobster
    hits = pygame.sprite.groupcollide(lobsters_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(hit.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

    # chceck to see if bullet hit a Ship Monster
    hits = pygame.sprite.groupcollide(ship_monsters_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        # Ship Monster nie może strzelać
        ship_monster.ready_to_fire = False
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(hit.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

    # check for player collision with ship monster
    collision = pygame.sprite.spritecollide(player, ship_monsters_group, True, pygame.sprite.collide_circle)
    if collision:
        ship_monster.ready_to_fire = False
        player.shield -= 40
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

    # check to see if enemy hit player (check for collision)
    collision = pygame.sprite.spritecollide(player, enemies_group, True, pygame.sprite.collide_circle)
    if collision:
        ship_monster.ready_to_fire = False
        player.shield -= 40
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

        if player.shield <= 0:
            expl = Explosion(player.rect.center, "lg")
            all_sprites_group.add(expl)
            explosion_sound.play()

    # check to see if lobster hit the player
    hit = pygame.sprite.spritecollide(player, lobsters_group, False, pygame.sprite.collide_circle)
    if hit:
        player.shield -= 100
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

        if player.shield <= 0:
            expl = Explosion(player.rect.center, "lg")
            all_sprites_group.add(expl)
            explosion_sound.play()
            sys.exit(0)

    # check to see if snake hit the player
    hit = pygame.sprite.spritecollide(player, snake_group, False, pygame.sprite.collide_circle)
    if hit:
        player.shield -= 100
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        explosion_sound.play()

        if player.shield <= 0:
            expl = Explosion(player.rect.center, "lg")
            all_sprites_group.add(expl)
            explosion_sound.play()
            sys.exit(0)

    # ship Monster shooting
    for item in ship_monsters_list:
        item.madness = random.randint(0, 100)
        if item.madness == 3:
            if item.rect.x < WIDTH:
                item.shoot(item.rect.x - 10, item.rect.y + 20)
                pygame.display.update()

    # RENDER
    # Background image
    screen.blit(background, (backgroundX, backgroundY))
    backgroundX -= 1

    # draw everything
    all_sprites_group.draw(screen)
    # after drawing everything, flip the display
    pygame.display.update()

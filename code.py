import pygame, sys, random
import time
from pygame import mixer

#Initalize
pygame.init()
WIDTH = 900
HEIGHT = 630
FPS = 60
clock = pygame.time.Clock()
score = 0


# define colors(RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)
RED = (200, 0, 0)


#Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#Background
background = pygame.image.load("background.png")
# background position
backgroundX = 0
backgroundY = 0


#Title and Icon (później się zmieni :D)
pygame.display.set_caption("nazwa")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


# Load all sounds 

bullet_sound = mixer.Sound("laser.wav")
ship_monster_bullet_sound = mixer.Sound("laser_ship_m.wav")
teleport_sound = mixer.Sound("teleport.wav")
enemy_explosion_sound = mixer.Sound("explosion_enemy.wav")
player_explosion_sound = mixer.Sound("explosion_player.wav")
game_over_sound = mixer.Sound("over.wav")

# music
mixer.music.load("music.mp3")
mixer.music.play(-1)


# Load all images (później się zmieni :D )
bulletImg = pygame.image.load("pocisk.png")
playerImg = pygame.image.load("player.png")
ship_monsterImg = pygame.image.load("ship_monster.png")
ship_monster_bulletImg = pygame.image.load("pocisk_enemy_niebieski.png")
cthulhu_lg = pygame.image.load("cthulhu.png")
cthulhuImg = pygame.transform.scale(cthulhu_lg, (90, 90))
lobsterImg = pygame.image.load("lobster.png")
pasekImg = pygame.image.load("pasek.png")
teleportImg = pygame.image.load("teleport.png")
plansza1 = pygame.image.load("plansza_poczatek.png")
text1 = pygame.image.load("text1.png")
sterowanie = pygame.image.load("sterowanie.png")

# boost animation
boost_anim = {}
boost_anim["bo"] = []
for i in range(3):
    filename = "turbo0{}.png".format(i)
    img = pygame.image.load(filename)
    boost_anim["bo"].append(img)

    
# explosion animation
explosion_anin = {}
# lista z grafikami dużymi
explosion_anin["lg"] = []
# lista z grafikami małymi
explosion_anin["sm"] = []

# dodajemy 5 grafik do ich list
for i in range(5):
    filename = "eksplozja_player0{}.png".format(i)
    img = pygame.image.load(filename)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anin["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (35, 35))
    explosion_anin["sm"].append(img_sm)

    
# FUNCTIONS 
# zielony pasek osłony
# (screen, x i y, procenty)
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 7
    fill = (pct/ 100) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    
# wyświetlanie doweolnego tekstu (na czym, tekst, rozmiar, x, y)    
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("font.ttf", size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)   
    
# wyswietlanie pasku temperatury silnika
def draw_engine_temp_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    BAR_LENGTH = 220
    BAR_HEIGHT = 5
    fill = (pct/ 100) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH + 50, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    
    
def lose_text():
    font = pygame.font.Font("font.ttf", 60)
    text_surface = font.render("GAME OVER", False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2, HEIGHT /2)
    screen.blit(text_surface, text_rect)
    
    
def handle_events():
    for event in pygame.event.get():
        # jeśli wydardzenie to "wyjście -> wyłącz program"
        if event.type == pygame.QUIT:
            sys.exit(0)
        # jeśli wydarzenie to wcziśniecie klawisza
        if event.type == pygame.KEYDOWN:
            # jeśli wciśnęty kalawisz to espace -> wyłącz program
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
                
    
   #funkcja uruchamiająca intro nieklikalne z historią i logiem
def intro():
        text1x = 0
        time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - time < 2500:
            handle_events()
            screen.blit(plansza1, (0, 0))
            pygame.display.update()
        time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - time < 28500:
            handle_events()
            screen.blit(text1, (text1x, 100))
            text1x -=1.5
            pygame.display.update()
        time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - time < 5500:
            handle_events()
            screen.blit(sterowanie, (0, 0))
            pygame.display.update() 
intro()
# PLAYER
class Player(pygame.sprite.Sprite):
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg
        
#         tworze prostokąt, żeby łatwiej nim manipulować (rect. = rectangle)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT /2
        
#         to jest taki jakby jak hit box w kształcie okręgu, łatwiej dzięki temu dopracować kolizje
        self.radius = 12
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.speedX = 0
        self.speedY = 0
        
#         poziom osłony
        self.shield = 100
        # temperatura silnika
        self.engine_temp = 20

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

        if self.rect.bottom > HEIGHT - 150:
            self.rect.bottom = HEIGHT - 150
        if self.rect.top < 70:
            self.rect.top = 70

    def shoot(self):
        bullet = Bullet(self.rect.right - 2, self.rect.bottom - 6)
        all_sprites_group.add(bullet)
        bullets_group.add(bullet)
        
# pociski gracza
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImg, (20,10))
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
        self.radius = int(self.rect.width /2 - 12)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.x = random.randint(5000, 20000)
        self.rect.y = random.randint(60, HEIGHT - 230)
        # poziom osłony
        self.shield = 100
        self.speedX = 0
        # wskaźnik gotowości do strzału            
        self.ready_to_fire = True
        #zmienna decydująca czy strzela         
        self.madness = 0
        self.alive = True
        
        
    def update(self):
        self.rect.x -= 1.5
       
    
    def shoot(self, x, y):
        #add to the Ship_monster_bullet class           
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
        self.radius = int(self.rect.width /2 )
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        self.rect.x = random.randint(1000, 22000)
        self.rect.y = random.randint(50, HEIGHT - 250)
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
        self.radius = int(self.rect.width /2 - 12)
        # pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
        # self.rect.x = random.randint(1000, 1500)
        # self.rect.y = random.randint(50, HEIGHT - 50)
        self.rect.x = random.randint(5300, 9300)
        self.rect.y = -100
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
                
                
class Boost(pygame.sprite.Sprite):
    def __init__(self, posx, y,  item):
        pygame.sprite.Sprite.__init__(self)
        self.image = boost_anim[item][0]
        self.rect = self.image.get_rect()
        self.rect.right = posx
        self.rect.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(boost_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = boost_anin[self.item][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            
            
# Create sprites group
all_sprites_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
lobsters_group = pygame.sprite.Group()
ship_monsters_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# add player to class and sprite
player = Player()
player_group.add(player)
all_sprites_group.add(player)


# add Ship Monster to his sprite and class
num_of_ship_monster = 80
ship_monster = Ship_monster()

ship_monsters_list = []
for i in range (num_of_ship_monster):
    ship_monster_i = Ship_monster()
    ship_monsters_list.append(ship_monster_i)

for item in ship_monsters_list:
    all_sprites_group.add(item)
    ship_monsters_group.add(item)

    
# add Cthulhu to his sprite and class
num_of_cthulhu = 200
for i in range (num_of_cthulhu):
    ct = Cthulhu()
    all_sprites_group.add(ct)
    enemies_group.add(ct)


# add Lobster to his sprite and class
num_of_lobsters = 30
for i in range (num_of_lobsters):
    lo = Lobster()
    all_sprites_group.add(lo)
    lobsters_group.add(lo)


# Game Loop (wykonuje się, dopóki program jest włączony)
while True:
    # keep loop running at the right speed
    clock.tick(FPS)
    

    #CHECKING INPUTS
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
                
            #  jeśli naciśnięto spacje, uruchamia się metoda boost, wyświetla grafika i odtwarza dźwiek            if event.key == pygame.K_LSHIFT:
            if event.key == pygame.K_LSHIFT:
                if player.engine_temp < 30:
                    screen.blit(teleportImg, (player.rect.x + 50, player.rect.y - 25))
                    pygame.display.update()
                    player.rect.x += 250
                    player.engine_temp += 100
                    boost = Boost(player.rect.left + 10, player.rect.y - 20 , "bo")
                    all_sprites_group.add(boost)
                    teleport_sound.play()
                

                
    #UPDATE
    #odświerza wszystkie elementy znajdujące się w grupię all_sprites (wszystko)     
    all_sprites_group.update()
    
   #spadek temperatury silników
    if player.engine_temp >= 20:
        player.engine_temp -= 0.3
    
    
    # chceck to see if bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(hit.rect.center, "lg")
        all_sprites_group.add(expl)
        enemy_explosion_sound.play()
        score += 10
       
        
    # chceck to see if bullet hit a lobster
    hits = pygame.sprite.groupcollide(lobsters_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        # dodanie ekspozji do klasy i all_sprites by było ją widać
        expl = Explosion(hit.rect.center, "lg")
        all_sprites_group.add(expl)
        enemy_explosion_sound.play()
        score += 50
       
        
        
    # chceck to see if bullet hit a Ship Monster
    for item in ship_monsters_list:
        if item.alive == True:
            collisions = pygame.sprite.spritecollide(item, bullets_group, True, pygame.sprite.collide_circle)
            for collision in collisions:
                expl = Explosion(collision.rect.center, "lg")
                all_sprites_group.add(expl)
                enemy_explosion_sound.play()
                item.kill()
                item.alive = False
                item.ready_to_fire = False
                score += 30
            
        
        
    # check for player collision with ship monster
    for item in ship_monsters_list:
        if item.alive == True:
            collisions = pygame.sprite.spritecollide(item, player_group, False, pygame.sprite.collide_circle)
            for collision in collisions:
                item.kill()
                item.alive = False
                item.ready_to_fire = False
                player.shield -= 40
                expl = Explosion(collision.rect.center, "lg")
                all_sprites_group.add(expl)
                player_explosion_sound.play()
                
                if player.shield <= 0:
                    mixer.music.stop()
                    expl = Explosion(player.rect.center, "lg")
                    all_sprites_group.add(expl)
                    game_over_sound.play()
                    lose_text()
                    pygame.display.update()
                    time.sleep(3)
                    sys.exit(0) 

       
                
                
    # check to see if enemy hit player (check for collision)
    collision = pygame.sprite.spritecollide(player, enemies_group, True, pygame.sprite.collide_circle)
    if collision:
        ship_monster.ready_to_fire = False
        player.shield -= 40
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        player_explosion_sound.play()   
     
        if player.shield <= 0:
            mixer.music.stop()
            expl = Explosion(player.rect.center, "lg")
            all_sprites_group.add(expl)
            game_over_sound.play()
            lose_text()
            pygame.display.update()
            time.sleep(3)
            sys.exit(0) 
            
     # check to see if lobster hit the player
    hit = pygame.sprite.spritecollide(player, lobsters_group, False, pygame.sprite.collide_circle)
    if hit:
        player.shield -= 90
        expl = Explosion(player.rect.center, "lg")
        all_sprites_group.add(expl)
        player_explosion_sound.play()
        
        if player.shield <= 0:
            mixer.music.stop()
            expl = Explosion(player.rect.center, "lg")
            all_sprites_group.add(expl)
            game_over_sound.play()
            lose_text()
            pygame.display.update()
            time.sleep(3)
            sys.exit(0) 
            
            
    # ship Monster shooting
    for item in ship_monsters_list:
        if item.ready_to_fire == True:
            item.madness = random.randint(0,100)
            if item.madness == 3:
                if item.rect.x < WIDTH:
                    if item.rect.x > 0:
                        item.shoot(item.rect.x-10, item.rect.y + 20)
                        ship_monster_bullet_sound.play()

            
            
    # RENDER
    #Background image
    screen.blit(background, (backgroundX, backgroundY))
    backgroundX -= 1

    # draw everything
    all_sprites_group.draw(screen)
    
    #rysowanie całego paska paska
    screen.blit(pasekImg, (13, 602))
    
    # rysowanie poziomu osłon
    draw_shield_bar(screen, 59, 611, player.shield)
    
    #rysowanie pkt
    draw_text(screen, str(score), 10, 860, 610)
    
    #rysowanie poziomu temperatury silnika
    draw_engine_temp_bar(screen, 437, 612 , player.engine_temp)
    
    
    # after drawing everything, flip the display
    pygame.display.update()

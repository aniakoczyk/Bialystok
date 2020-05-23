import pygame, sys, random

#Initalize
pygame.init()
WIDTH = 900
HEIGHT = 600
FPS = 60


# define colors(RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)


#Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#Background
background = pygame.image.load("background2.png")
# background position
backgroundX = 0
backgroundY = 0


#Title and Icon (później się zmieni :D)
pygame.display.set_caption("nazwa")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


# Load all images (później się zmieni :D )
explosionImg = pygame.image.load("explosion.png")
bulletImg = pygame.image.load("bullet.png")
playerImg = pygame.image.load("spaceship.png")
ship_monsterImg = pygame.image.load("ship.png")
ship_monster_bulletImg = pygame.image.load("fire.png")
cthulhuImg = pygame.image.load("cthulhu.png")
lobsterImg = pygame.image.load("lobster.png")


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
        self.image = pygame.transform.scale(bulletImg, (20,10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.radius = 5
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
        self.rect.x = random.randint(800, 3000)
        self.rect.y = random.randint(50, HEIGHT - 50)
        # poziom osłony
        self.shield = 100
        self.speedX = 0
        # wskaźnik gotowości do strzału            
        self.ready_to_fire = True
        
        
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
        self.radius = int(self.rect.width /2 - 12)
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
            
            
# Create sprites group
all_sprites_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
lobsters_group = pygame.sprite.Group()
ship_monsters_group = pygame.sprite.Group()


# add player to class and sprite
player = Player()
all_sprites_group.add(player)


# add enemies to their sprite and class
num_of_ship_monster = 10
for i in range (num_of_ship_monster):
    ship_monster = Ship_monster()
    all_sprites_group.add(ship_monster)
    enemies_group.add(ship_monster)
    ship_monsters_group.add(ship_monster)


num_of_cthulhu = 10
for i in range (num_of_cthulhu):
    ct = Cthulhu()
    all_sprites_group.add(ct)
    enemies_group.add(ct)


num_of_lobsters = 10
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
                

                
    #UPDATE
    #odświerza wszystkie elementy znajdujące się w grupię all_sprites (wszystko)     
    all_sprites_group.update()
    
    
    # chceck to see if bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        print("ekslpozje i takie tam")
       
        
    # chceck to see if bullet hit a lobster
    hits = pygame.sprite.groupcollide(lobsters_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        print("eksplozje i takie tam")
        
        
    # chceck to see if bullet hit a Ship Monster
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        print("eksplozje i takie tam")
        
        # Ship Monster nie może strzelać         
        ship_monster.ready_to_fire = False
        
        
    # ship Monster shooting
    ship_monster_mad = random.randint(0,80)
    if ship_monster_mad == 3:
        if ship_monster.rect.x < 2000:
            if ship_monster.ready_to_fire:
                ship_monster.shoot(ship_monster.rect.centerx - 55, ship_monster.rect.y - 3)
                pygame.display.update()
                
                
    # check to see if enemy hit player (check for collision)
    collision = pygame.sprite.spritecollide(player, enemies_group, True, pygame.sprite.collide_circle)
    if collision:
        ship_monster.ready_to_fire = False
        player.shield -= 40
        expl2 = Explosion(player.rect.center)
        all_sprites_group.add(expl2)
        if player.shield <= 0:
            sys.exit(0)
            
            
     # check to see if lobster hit the player
    lobster_attack = pygame.sprite.spritecollide(player, lobsters_group, False, pygame.sprite.collide_circle)
    if lobster_attack:
        player.shield -= 100
        expl2 = Explosion(player.rect.center)
        all_sprites_group.add(expl2)
        if player.shield <= 0:
            sys.exit(0)
            
            
            
    # RENDER
    #Background image
    screen.blit(background, (backgroundX, backgroundY))
    backgroundX -= 1

    # draw everything
    all_sprites_group.draw(screen)
    # after drawing everything, flip the display
    pygame.display.update()

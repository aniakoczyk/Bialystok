import pygame, sys, random

#Initalize the pygame
pygame.init()


#Create the screen
screen = pygame.display.set_mode((900, 600))


#Background
background = pygame.image.load("background2.png")
# background position
backgroundX = 0
backgroundY = 0


#Title and Icon (później się zmieni :D)
pygame.display.set_caption("nazwa")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


#Player
player_image = pygame.image.load("spaceship.png")
# start position
playerX = 10
playerY = 340
playerY_change = 0

# funkcja wyświetlająca (blit) gracza na ekranie
def player(x,y):
    screen.blit((player_image),(x, y))


#Enemy
enemy_image = pygame.image.load("monster.png")
#start position
enemyX = random.randint(750, 900)
enemyY = random.randint(50, 650)
enemyX_change = -2


# funkcja wyświetlająca (blit) wroga na ekranie
def enemy(x, y):
    screen.blit((enemy_image), (x, y))

# Game Loop (wykonuje się, dopóki program jest włączony)
while True:

    #Background image
    screen.blit(background, (backgroundX, backgroundY))
    backgroundX -= 1


    #Handle events
    for event in pygame.event.get():
        # jeśli wydardzenie to "wyjście -> wyłącz program"
        if event.type == pygame.QUIT:
            sys.exit(0)
        # jeśli wydarzenie to wcziśniecie klawisza
        if event.type == pygame.KEYDOWN:
            # jeśli wciśnęty kalawisz to espace -> wyłącz program
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
                
                
        #player movements - jeśli strzałka-góra->ruch góra, strzałka-dół->ruch dół
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -2
            if event.key == pygame.K_DOWN:
                playerY_change = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

                
    #screen borders player - żeby player nie wyjeżdał poza screen
    if playerY <=-10:
        playerY = -10
    elif playerY >= 520:
        playerY = 520   
        
    #ruch player, ruch enemy
    playerY += playerY_change
    enemyX += enemyX_change        
                
        
    # wywołanie funkcji enemy i gracza
    enemy(enemyX, enemyY)
    player(playerX, playerY)
    
    # refresh screen
    pygame.display.update()

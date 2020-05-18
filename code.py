import pygame, sys, random

#Initalize the pygame
pygame.init()


# Creat the screen
screen = pygame.display.set_mode((900, 600))


# Background
background = pygame.image.load("background.png")
# background position
backgroundX = 0
backgroundY = 0


#Title and Icon (później się zmieni :D)
pygame.display.set_caption("nazwa")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load("spaceship.png")
# start position
playerX = 10
playerY = 340

# funkcja wyświetlająca (blit) gracza na ekranie
def player(x,y):
    screen.blit((playerImg),(playerX, playerY))


#Enemy
enemyImg = pygame.image.load("monster.png")
# start position
enemyX = random.randint(50, 800)
enemyY = random.randint(0, 570)
enemyX_change = 2
enemyY_change = 0

# funkcja wyświetlająca (blit) wroga na ekranie
def enemy(x, y):
    screen.blit((enemyImg), (x, y))

# Game Loop (wykonuje się, dopóki program jest włączony)
running = True
while running:

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

    # wywołanie funkcji enemy i gracza
    enemy(enemyX, enemyY)
    player(playerX, playerY)
    # refresh screen
    pygame.display.update()

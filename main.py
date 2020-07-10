import pygame
import random
import sys
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = '/gallery/sprites/bird.png'
BACKGROUND = '/gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def WelcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_height())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {
            'x': SCREENWIDTH+200,
            'y': newPipe1[0]['y']
        },
        {
            'x': SCREENWIDTH+200+int(SCREENWIDTH/2),
            'y': newPipe2[1]['y']
        }
    ]
    lowerPipes = [
        {
            'x': SCREENWIDTH+200,
            'y': newPipe1[0]['y']
        },
        {
            'x': SCREENWIDTH+200+int(SCREENWIDTH/2),
            'y': newPipe2[1]['y']
        }
    ]
    pipeVeloX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        playerMidPos = playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos+4:
                score += 1
                print("your score is ", score)
            GAME_SOUNDS['point'].play()
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery+min(playerVelY, GROUNDY-playery-playerHeight)


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset+random.randrange(0, int(SCREENHEIGHT +
                                        GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH+10
    y1 = pipeHeight-y2+offset
    pipe = [
        {'x': pipex, 'y': -y1},  # upper pipe
        {'x': pipex, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['nubmer'] = (
        pygame.image.load("gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/sprites/9.png").convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load(
        "gallery/sprites/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        "gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(
        "gallery/sprites/background.png").convert()
    GAME_SPRITES['player'] = pygame.image.load(
        "gallery/sprites/bird.png").convert_alpha()
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wind'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    while True:
        WelcomeScreen()
        mainGame()

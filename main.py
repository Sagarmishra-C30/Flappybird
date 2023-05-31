#Flappy Bird Game
# Licensed under the MIT License - see LICENSE file for details

import random
import sys
import pygame
from pygame.locals import *

#Global variables for FlappyBird
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bluebird.png'
PIPE = 'gallery/sprites/pipe.jpg'
ICON = 'gallery/sprites/bird-icon.png' 
BG_LIST = ['bgphone.jpg', 'bgphone2.jpg', 'bgstarphone.png']
def welcomeScreen():
    """Shows the welcome screen"""
    # player x and y co-ordinate
    #playerx = int(SCREENWIDTH/5)
    #playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)
    BACKGROUND = 'gallery/sprites/' + random.choice(BG_LIST)
    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert()
    # message x and y co-ordinate
    messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_width())/2)
    messagey = 0  #int(SCREENHEIGHT*0.13)
    # base x co-ordinate
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button or escapes exit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses start or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                return
            #if no event is generated, show the message screen by blitting all neccessary elements on the screen
            else:
                # blitting the sprites on the screen. blit method takes image or element and its co-ordinates as a tuple
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                #SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)) #
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                #display screen is updated and only now the blit becomes visible
                pygame.display.update()
                #setting/ fixing the fps to the FPS value
                FPSCLOCK.tick(FPS)


def getRandomPipe():
    """generate random positions for two pipes (upper and lower) for blitting on the screen"""
    pipeHeight = GAME_SPRITES["pipe"][0].get_height() 
    offset = SCREENHEIGHT/3
    # y of lower pipe
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES["base"].get_height() - 1.2*offset)) 
    # here x co-ordinate of randomly generated pipes are kept at 10 pixel ahead of screen initially
    pipeX = SCREENWIDTH + 10
    # y of upper pipe
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x': pipeX, 'y': -y1}, #upper pipe - y is above the screen so it's taken negative
        {'x': pipeX, 'y': y2}   #lower pipe
    ]
    return pipe
    
def isCollide(playerx, playery, upperPipes, lowerPipes):
    """checks if the player has crashed into the sky, or ground or the pipe"""
    # if player body touches the ground or the sky/top, means player has collided and is crashed
    if playery > GROUNDY - 30 or playery < 0:
        # GAME_SOUNDS["hit"].play()
        return True

    #check if player collides with the pipes
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES["pipe"][0].get_height()
        # if player is inside the pipe or touches the pipe crash it
        if (playery < (pipeHeight + pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            # GAME_SOUNDS["hit"].play()
            return True

    for pipe in lowerPipes:
        # if player is inside the pipe or touches the pipe crash it
        if ((playery + GAME_SPRITES['player'].get_height()) > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            # GAME_SOUNDS["hit"].play()
            return True    

    return False

def mainGame():
    """Main game engine"""
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery= int(SCREENWIDTH/2)
    basex = 0
    
    # create two pipes for blitting on the screen
    newPipe1 = getRandomPipe() #contains one upper and one lower pipe
    newPipe2 = getRandomPipe() #contains one upper and one lower pipe

    # list of upper pipes
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
    ]

    # list of lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4     #pipe's velocity in x direction
    #player speed
    playerVelY = -9     #player's velocity in Y direction
    playerMaxVelY = 10  #player's maximum velocity in Y direction
    playerMinVelY = -8  #player's minimum velocity in Y direction
    playerAccY = 1     #player's acceleration in Y direction

    playerFlappAccv = -8    #palyer's velocity while flapping 
    playerFlapped = False   #True only when bird is flapping

    while True:
        """main game loop"""
        for event in pygame.event.get():
            #exit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #play game
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: #if palyer is inside the screen
                    playerVelY = playerFlappAccv    #giving player the flapping velocity in y direction
                    playerFlapped = True    #as player in inside the screen means its flapping
                    # GAME_SOUNDS["wing"].play()

        # checks if player is crashed or not
        crashed = isCollide(playerx, playery, upperPipes, lowerPipes)
        #if player crashed exit the main loop
        if crashed:
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES["player"].get_width()/2   #center point of bird/player
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES["pipe"][0].get_width()/2  #center point of pipe
            #if player's center point crosses the center of pipe give it a score
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                # GAME_SOUNDS["point"].play()

        #if player has not yet reached its max velocity and is not flapping currently add acceleration to player's velocity to make it fall
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        # if player has flapped make it false coz flapping is done only when up or space key is pressed and if not pressed no flapping occurs
        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES["player"].get_height()
        # if the player has reached the ground it should remain on the ground meaning y of player should not increase any further
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipe to the left - that is towards the screen (reducing x of pipe)
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        # Add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()   #generate a new pipe 
            upperPipes.append(newPipe[0])   #adding upper pipe to upperPipes list
            lowerPipes.append(newPipe[1])   #adding lower pipe to lowerPipes list

        #if the pipe is outside the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #blit the sprites to the screen         
        SCREEN.blit(GAME_SPRITES['background'], (0, 0)) #blit the bg
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))  #blit the upper pipe
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))  #bit the lower pipe
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY)) #blit the base
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)) #blit the player
        #blitting the score
        myDigits = [int(x) for x in list(str(score))]   #separating the digits of a score   e.g  21 -> [2, 1] 
        width = 0   
        for digit in myDigits:
                width += GAME_SPRITES["numbers"][digit].get_width()/2   #adding width of diff number images
        
        Xoffset = (SCREENWIDTH - width)/2   #setting offset to centre of the screen for the score
        for digit in myDigits:
            #blitting the digit number on the screen
            SCREEN.blit(GAME_SPRITES["numbers"][digit], (Xoffset, SCREENHEIGHT*0.12))
            #inscrease offset to place next digit after the first digit
            Xoffset += GAME_SPRITES["numbers"][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)  #setting the fps of clock to FPS


if __name__ == "__main__":
    pygame.init() #initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock() 
    pygame.display.set_caption('Flappy Bird')
    pygame.display.set_icon(pygame.image.load(ICON))
    #game sprites(images)
    GAME_SPRITES["numbers"] = []
    for i in range(10):
        img = pygame.transform.scale(pygame.image.load(f'gallery/sprites/numbers/{i}.png').convert_alpha(), (30, 50))
        GAME_SPRITES["numbers"].append(img)
    
    GAME_SPRITES["message"] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES["player"] =  pygame.transform.scale(pygame.image.load(PLAYER).convert_alpha(), (61, 28))

    '''
    #game sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound('gallery/sounds/die.wav')
    GAME_SOUNDS["hit"] = pygame.mixer.Sound('gallery/sounds/hit.wav')
    GAME_SOUNDS["point"] = pygame.mixer.Sound('gallery/sounds/point.wav')
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound('gallery/sounds/swoosh.wav')
    GAME_SOUNDS["wing"] = pygame.mixer.Sound('gallery/sounds/wing.wav')
    '''
    
    while True:
        welcomeScreen()
        mainGame()



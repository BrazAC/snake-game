"""
Author: Braz Amorim
Date: 20/09/24
Project: Snake game
"""
#Algoritm
'''
0 - Step
Make the basic pygame structure
Implement the grid on the pygame screen

1 - Step
(The head of the snake and the body parts, will be a simple square)
Create the snake (the snake will be a vector with the snake parts)
The game begins with the head of the snake centered in the screen without movement
The game will begin when the player press some of the arrow keys 
The snake head will begin his movement (change the square position on the grid) in the direction of the arrow pressed
If the player press another arrow the head will change the movement direction

2 - Step
Generate a square (the fruit) in a random position of the grid
If the snake head position is the same as the fruit:
    Remove the fruit from the grid
    Add new body part to the end of the snake
    Create a new fruit in another random location of the grid

3 - Step
If the snake hit a wall, or hit any of his body part the player loses the game

4 - Make this sh@* looks good somehow
I realy dont no how to do it yet :(
'''
import pygame
import random

def soundPlayer(filePath):
    #Load the sound
    pygame.mixer.music.load(filePath)
    #Play the sound
    pygame.mixer.music.play()

def gridInitializer(screen, resolution, lineDistance):
    #Design the grid
    x = 0
    y = 0
    screen.fill("black")
    for i in range(resolution // lineDistance):
        y += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [0, y], [resolution, y])
        x += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [x, 0], [x, resolution])

def gridDesigner(screen, resolution, lineDistance, snake, fruitSize, fruitColor, fruitPosition):
    screen.fill("black")
    #Design the grid
    x = 0
    y = 0
    for i in range(resolution // lineDistance):
        y += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [0, y], [resolution, y])
        x += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [x, 0], [x, resolution])

    #Design the snake
    snakeDesigner(screen, snake)

    #Design the fruit
    gridFruitPosition = fruitDesigner(screen, fruitSize, fruitColor, fruitPosition)
    
    pygame.display.flip()
    pygame.time.wait(snake[0].speed)
    
    return gridFruitPosition

def snakeDesigner(screen, snake):
    #Desenhar partes da cobra
        #Iterar por snake, obter informações de cada parte da cobra, desenhar parte
    for snakePart in snake:
        if snakePart != 0:
            rect = pygame.Rect((0,0), snakePart.size)
            rect.center = snakePart.position
            pygame.draw.rect(screen, snakePart.color, rect)

def fruitDesigner(screen, fruitSize, fruitColor, pixelFruitPosition):
    #Setting some variables
    gridFruitPosition = ((pixelFruitPosition[0] // fruitSize[0]) + 1, (pixelFruitPosition[1] // fruitSize[0]) + 1)

    #Calculating the new center position for the fruit
    centerx = gridFruitPosition[0] * fruitSize[0] - (fruitSize[0] // 2)
    centery = gridFruitPosition[1] * fruitSize[0] - (fruitSize[0] // 2)

    #Design fruit
    rect = pygame.Rect((0,0), fruitSize)
    rect.center = (centerx, centery)
    pygame.draw.rect(screen, fruitColor, rect)

    #Return fruit position
    return (centerx, centery)

def snakeUpdater(snake, direction, distance, gridFruitPosition, score):
    #Making a deepcopy of the old snake
    oldSnake = [0]*len(snake)
    for i in range(len(oldSnake)):
        if snake[i] != 0 :
            #color, position, size, speed, direction
            color = snake[i].color
            position = snake[i].position
            size = snake[i].size
            speed = snake[i].speed
            directionC = snake[i].direction
            oldSnake[i] = Snake(color, position, size, speed, directionC)

    #Update de position of the head of the new snake
    if direction == "UP":
        #update y position
        x, y = snake[0].position
        snake[0].position = (x, y - distance)
    elif direction == "DOWN":
        #update y position
        x, y = snake[0].position
        snake[0].position = (x, y + distance)
    elif direction == "LEFT":
        #update x position
        x, y = snake[0].position
        snake[0].position = (x - distance, y)
    else: #direction == "RIGHT"
        #update x position
        x, y = snake[0].position
        snake[0].position = (x + distance, y)

    #Verify if the head hit a body part
    for i in range(1, len(snake)):
        if snake[i] != 0:
            if snake[0].position == snake[i].position:
                gameContinues = False
                #Play the game-over sound
                soundPlayer("./sounds/8-bit-game-over-sound.mp3")
                break
            else:
                gameContinues = True
        else:
            gameContinues = True
            break

    #Verify if the head hit a wall
    if snake[0].position[0] < 0 or snake[0].position[0] > 1000 or snake[0].position[1] < 0 or snake[0].position[1] > 1000:
        gameContinues = False
        #Play the game-over sound
        soundPlayer("./sounds/8-bit-game-over-sound.mp3")

    #Update the position of the parts of the new snake
    if oldSnake[1] != 0:
        for i in range(1, len(oldSnake)):
            if oldSnake[i] != 0:
                #The current snakePart assumes the position of the antecessor snakePart
                snake[i].position = oldSnake[i - 1].position
                lastSnakeBody = i
    else:
        lastSnakeBody = 0

    #Verify if the snake had find a fruit
        #If yes, add a new snakePart to the snakeVector
    if snake[0].position == gridFruitPosition:
        snake[lastSnakeBody + 1] = Snake("green", oldSnake[lastSnakeBody].position, snake[0].size, None, None)
        fruitStatus = True
        score += 1
        #Play the score sound
        soundPlayer("./sounds/8-bit-score-sound.mp3")
    else:
        fruitStatus = False

    return snake, fruitStatus, gameContinues, score

def menuScreen(screen):
    #create a font object
    font = pygame.font.Font('freesansbold.ttf', 22)
    font1 = pygame.font.Font('freesansbold.ttf', 42)

    # create a text surface object
    text1 = font1.render('SNAKE GAME', True, (0, 255, 0))
    text = font.render('PRESS ANY ARROW TO BEGIN', False, (255, 255, 255))

    # create a rectangular object for the text surface object
    textRect1 = text1.get_rect()
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect1.center = (500, 450)
    textRect.center = (500, 500)

    # copying the text surface object to the display surface object at the center coordinate.
    screen.blit(text1, textRect1)
    screen.blit(text, textRect)

    pygame.display.update()
    
def gameOverScreen(screen, score):
    #create a font object
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object
    text0 = font.render('GAME OVER', True, (255, 0, 0))
    text1 = font.render(f'SCORE {score}', True, (255, 255, 255))

    # create a rectangular object for the text surface object
    textRect0 = text0.get_rect()
    textRect1 = text1.get_rect()

    # set the center of the rectangular object.
    textRect0.center = (500, 450)
    textRect1.center = (500, 500)

    # copying the text surface object to the display surface object at the center coordinate.
    screen.blit(text0, textRect0)
    screen.blit(text1, textRect1)

    pygame.display.update()

def main():
    #Some useful variables
    resolution = 1000
    gridLineDistance  = resolution // 36
    screenUpdateSpeed = 125
    gridWidth = resolution // gridLineDistance
    gameBegins = False
    snakeDirection = None
    fruitColor = "red"
    fruitSize = (gridLineDistance, gridLineDistance)
    score = 0
    alreadyBegun = 0

    #Initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((resolution, resolution))
    pygame.display.set_caption('Snake Game')

    #Initialize grid
    gridInitializer(screen, resolution, gridLineDistance)

    #Initializing the snake
    snake = [0] * (gridWidth ** 2)
    head = Snake(pygame.Color(0, 99, 18), (resolution//2, resolution//2), (gridLineDistance, gridLineDistance), screenUpdateSpeed, None)
    snake[0] = head
    #snakeDesigner(screen, snake)    

    #Initializing fruit
    range = (gridLineDistance // 2, resolution - (gridLineDistance // 2))
    pixelFruitPosition = (random.randint(range[0], range[1]), random.randint(range[0], range[1]))
    gridFruitPosition = ((pixelFruitPosition[0] // gridLineDistance) + 1, (pixelFruitPosition[1] // gridLineDistance) + 1)

    #GAME LOOP
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                #If some key was pressed, verify if it was an arrow an what arrow it was
                if event.key == pygame.K_UP:
                    gameBegins = True
                    snakeDirection = "UP"
                elif event.key == pygame.K_DOWN:
                    gameBegins = True
                    snakeDirection = "DOWN"
                elif event.key == pygame.K_LEFT:
                    gameBegins = True
                    snakeDirection = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    gameBegins = True
                    snakeDirection = "RIGHT"        

        #Caso saiu do menu/jogo iniciou, iniciar jogo
        if gameBegins:
            #Reset the score
            score = 0

            #Play the game-begins sound
            soundPlayer("./sounds/8-bit-game-begins-sound.mp3")

            while gameBegins:
                alreadyBegun = 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        #If some key was pressed, verify if it was an arrow an what arrow it was
                        if event.key == pygame.K_UP:
                            gameBegins = True
                            snakeDirection = "UP"
                        elif event.key == pygame.K_DOWN:
                            gameBegins = True
                            snakeDirection = "DOWN"
                        elif event.key == pygame.K_LEFT:
                            gameBegins = True
                            snakeDirection = "LEFT"
                        elif event.key == pygame.K_RIGHT:
                            gameBegins = True
                            snakeDirection = "RIGHT"

                #Update the snake parts position
                snake, fruitStatus, gameBegins, score = snakeUpdater(snake, snakeDirection, gridLineDistance, gridFruitPosition, score)

                #Design the grid (design: grid, snake, fruit)
                #If the snake not ate the fruit
                if not fruitStatus:
                    #Design the fruit in the same location
                    gridFruitPosition = gridDesigner(screen, resolution, gridLineDistance, snake, fruitSize, fruitColor, pixelFruitPosition)
                #If the snake ate the fruit
                else:
                    #Design the fruit in a new location
                    generate = True
                    while generate:
                        #Generate a random position
                        range = (gridLineDistance // 2, resolution - (gridLineDistance // 2))
                        pixelFruitPosition = (random.randint(range[0], range[1]), random.randint(range[0], range[1]))
                        gridFruitPosition = ((pixelFruitPosition[0] // gridLineDistance) + 1, (pixelFruitPosition[1] // gridLineDistance) + 1)

                        for bodyPart in snake:
                            if bodyPart != 0:
                                #If equals, generate another position and test again
                                if gridFruitPosition == bodyPart.position:
                                    break
                                #If the generated position does not equal to any of the snake bodyPart position proceed
                                else:
                                    generate = False
                        print(generate)

                    
                    gridFruitPosition = gridDesigner(screen, resolution, gridLineDistance, snake, fruitSize, fruitColor, pixelFruitPosition)
        #Caso perdeu o jogo/jogo nao iniciou, iniciar menu
        else:
            if alreadyBegun == 0:
                menuScreen(screen)
            else:
                #Show game-over screen
                gameOverScreen(screen, score)
                #Reset the snake
                snake = [0] * (gridWidth ** 2)
                head = Snake(pygame.Color(0, 99, 18), (resolution//2, resolution//2), (gridLineDistance, gridLineDistance), screenUpdateSpeed, None)
                snake[0] = head
    pygame.quit()

class Snake:
    def __init__(self, color, position, size, speed, direction):
        self.color = color
        self.position = position
        self.size = size
        self.speed = speed
        self.direction = direction

if __name__ == "__main__":
    main()
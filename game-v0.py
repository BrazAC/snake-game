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

3 - Make this sh@* looks good somehow
I realy dont no how to do it yet :(
'''
import pygame
import random

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
    #Design the grid
    x = 0
    y = 0
    screen.fill("black")
    for i in range(resolution // lineDistance):
        y += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [0, y], [resolution, y])
        x += lineDistance
        pygame.draw.line(screen, pygame.Color(30,30,30), [x, 0], [x, resolution])

    #Design the snake
    snakeDesigner(screen, snake)

    #Design the fruit
    fruitDesigner(screen, fruitSize, fruitColor, fruitPosition)
    
    pygame.display.flip()

def snakeDesigner(screen, snake):
    #Desenhar partes da cobra
        #Iterar por snake, obter informações de cada parte da cobra, desenhar parte
    for snakePart in snake:
        if snakePart != 0:
            rect = pygame.Rect((0,0), snakePart.size)
            rect.center = snakePart.position
            pygame.draw.rect(screen, snakePart.color, rect)
    pygame.display.flip()

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
    pygame.display.flip()

    #Return fruit position
    return (centerx, centery)

def snakeUpdater(snake, direction, distance):
    #Update de position of the head
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

    """#Update the position of the snakeParts
    for i in range(1, len(snake)):
        if snake[i] != 0:
            #The current snakePart assumes the position of the antecessor snakePart
            #From the head to the "tail"""

    return snake

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
    
    #Initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((resolution, resolution))

    #Initialize grid
    gridInitializer(screen, resolution, gridLineDistance)

    #Initializing the snake
    snake = [0] * (gridWidth ** 2)
    head = Snake(pygame.Color(0, 99, 18), (resolution//2, resolution//2), (gridLineDistance, gridLineDistance), screenUpdateSpeed, None)
    snake[0] = head
    snakeDesigner(screen, snake)    

    #Initializing fruit
    range = (gridLineDistance // 2, resolution - (gridLineDistance // 2))
    pixelFruitPosition = (random.randint(range[0], range[1]), random.randint(range[0], range[1]))

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
        
        if gameBegins:
            #Update the snake parts position
            snake = snakeUpdater(snake, snakeDirection, gridLineDistance)

            #Design the grid (design: grid, snake, fruit)
            gridDesigner(screen, resolution, gridLineDistance, snake, fruitSize, fruitColor, pixelFruitPosition)
            pygame.time.wait(snake[0].speed)
            
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
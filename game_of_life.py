import time
import random
import pygame

display_width = 1430
display_height = 770 

# Defines the size of each cell in the grid
grid_x = 0
grid_y = 0
grid_width = 10
grid_height = 10 
grid_margin = 1

# Defines the size of the array and thus the number of cells in the grid
array_width = 130
array_height = 70

# Basic colors 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


# Grid functions
## function that changes an empty list into a 2D array

def make2darray(list_name, row, colomn):
    for row in range(row):
        list_name.append([]) 
        for column in range(colomn):
            list_name[row].append(0)
            # Comment line 34 and uncomment line 36 (command below) to randomize the setup of alive cells
            #list_name[row].append(random.randint(0,1))

## function that draws the grid in the display
def cell(cellx, celly, cellw, cellh, color):
    pygame.draw.rect(gameDisplay,color,[cellx,celly,cellw,cellh],0)

# The Game of Life

## Function that counts and adds the value of the adjacent cells, return the total

def count_adjacent_cells(array, row, column): 
          
    total = 0 

    # Defines a range of values that x and y can take to recover count of alive cells adjacent to array[row][column]
    x_start_value = (row - 1 + len(array)) % len(array)
    x_mid_value = (row + len(array)) % len(array)
    x_end_value = (row + 1 + len(array)) % len(array)
    y_start_value = (column - 1 + len(array[0])) % len(array[0])
    y_mid_value = (column + len(array[0])) % len(array[0])
    y_end_value = (column + 1 + len(array[0])) % len(array[0])

    list_x = [x_start_value, x_mid_value, x_end_value]
    list_y = [y_start_value, y_mid_value, y_end_value]
    
    # Append each possible combination of x and y as tuples in a list
    list_xy = [(x,y) for x in list_x for y in list_y]
    
    # Count the number of (x, y) for which the value is one and add them to total
    for (x, y) in list_xy:
        total += array[x][y]
    # Remove the value of the cells for which we are counting the neighbours - array[row][column] - to avoid mistakenly counting it.
    total -= array[row][column]
    
    return total

# Game Loops functions

## Define framerate
def framerate_setup():
    try:
        max_fps = input("Define your game's max FPS (default is 60): ")
    except SyntaxError:
        max_fps = 60
    return max_fps

## Presetup function
def pre_setup():
    print("Please define the size of your game. It should be a grid of x by y, where x is the number of row and y the number of columns.")
    
    try:
        x = input("Number of rows (default is 70)? Should be an integer between 1 and 70: ")
    except SyntaxError:
        x = 0
    
    try:
        y = 0 + input("Number of columns (default is 70)? Should be an integer between 1 and 130: ")
    except SyntaxError:
        y = 0
    
    if x == 0:
        x = 70
    elif x > 70:
        x = 70
    elif x < 1:
        x = (-1 * x)
        if x > 70:
            x = 70

    if y == 0:
        y = 130
    elif y > 130:
        y = 130
    elif y < 1:
        y = (-1 * y)
        if y > 130:
            y = 130

    return [x,y]

## Setup loop
## This function allow the "player" to setup the starting value of each of the cells in the grid.

def setup_loop(array1, frame_rate):

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # get out of the set up loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gol_loop(grid, frame_rate)
            
            # changes the value of a cell if the player clicks on it and prints the coordinates
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (grid_width + grid_margin)
                row = pos[1] // (grid_height + grid_margin)
                if array1[row][column] == 1:
                    array1[row][column] = 0
                else:
                    array1[row][column] = 1 


                
                #print("Click", pos, "Grid coordinates", row, column)

        gameDisplay.fill(black)

        # creates the graphic grid based on the data in the 2D array
        for row in range(len(array1)):
            color = white
            for column in range(len(array1[0])):
                if grid[row][column] == 1:
                    color = blue
                else:
                     color = white

                cell((grid_width+grid_margin)*column,(grid_height+grid_margin)*row, grid_width, grid_height, color)

        
        pygame.display.update()
        clock.tick(frame_rate)

## Game of Life loop
## This function plays out the game of life for the predefined setup.

def gol_loop(array1, frame_rate):

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                game_exit = True
            
            # get out of the set up loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    setup_loop(grid, frame_rate)

        grid_2 = []
        make2darray(grid_2, array_height, array_width)

        # The Game of Life  
        for row in range(len(array1)):
            for column in range(len(array1[0])):
                total = count_adjacent_cells(array1, row, column)
                if total == 3 or (total == 2 and array1[row][column] == 1):
                    grid_2[row][column] = 1
                else:
                    grid_2[row][column] = 0
                

        array1 = grid_2

        gameDisplay.fill(black)

        # creates the graphic grid based on the data in the 2D array
        for row in range(len(array1)):
            color = white
            for column in range(len(array1[0])):
                if array1[row][column] == 1:
                    color = blue
                else:
                     color = white

                cell((grid_width+grid_margin)*column,(grid_height+grid_margin)*row, grid_width, grid_height, color)

        
        pygame.display.update()
        clock.tick(frame_rate)


# Runs the game
## presetup
print("\n")
print("Hello! Welcome to Conway's Game of Life\n")
print("When the display appears, click on cells to activate or deactivate them. Press ENTER when done to launch the game. Press ENTER again to stop the game.\n")
print("""Commands:
RETURN = Lauch the game or go back to the setup step
CMD+Q or ALT+F4 = Exit the game""")

framerate = framerate_setup()
setup_data = pre_setup()

array_width = setup_data[1]
array_height = setup_data[0]

# Defines the size of each cell in the grid
grid_x = 0
grid_y = 0
grid_width = 10
grid_height = 10 
grid_margin = 1

display_width = array_width * (grid_width + grid_margin) 
display_height = array_height * (grid_height + grid_margin)

## create 2D array
grid = []
make2darray(grid, array_height, array_width)

# Defines the display and the clock for pygame and initialises pygame
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

## setup
setup_loop(grid, framerate) 
##game
gol_loop(grid, framerate)
pygame.quit()
#Tetris
#Nicholas Faria
#Jan 25, 2018
#Recreation of the famous game tetris

import pygame, random, time #Import the modules needed

pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init() #Call this function so the pygame library can initialize itself

screen_width = 800
screen_height = 800 #Create variables for the screen's width and height

screen = pygame.display.set_mode([screen_width, screen_height]) #Create the display screen using the width and height

pygame.display.set_caption("Tetris") #Sets the caption of the display window to Tetris

button_lightgrey = (173, 173, 173)
button_darkgrey = (140, 140, 140)
background_grey = (242, 242, 242)
outline = (110, 110, 110)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
orange = (255, 155, 0)
lightblue = (0, 255, 250)
lightgreen = (85, 255, 0)
darkblue = (0, 35, 255)
pink = (255, 0, 255) #Assign variables for each RGB colour value used

#Images
logoImage = pygame.image.load("TetrisLogo.png")
logo = pygame.transform.scale(logoImage, (400, 140))
smallLogo = pygame.transform.scale(logoImage, (240, 70))
Leftkey = pygame.image.load("leftkey.png")
leftkey = pygame.transform.scale(Leftkey, (100, 100))
Rightkey = pygame.image.load("rightkey.png")
rightkey = pygame.transform.scale(Rightkey, (100, 100))
Upkey = pygame.image.load("upkey.png")
upkey = pygame.transform.scale(Upkey, (100, 100))
Downkey = pygame.image.load("downkey.png")
downkey = pygame.transform.scale(Downkey, (100, 100))
Spacekey = pygame.image.load("spacekey.png")
spacekey = pygame.transform.scale(Spacekey, (175, 50))
Arrow = pygame.image.load("arrow.png")
arrow = pygame.transform.scale(Arrow, (50, 50))
#Creates a variable for each image used, and also assignes a different variable to a resized version

#FONTS
text = pygame.font.Font("Tetris.ttf", 75)
smallerText = pygame.font.Font("Tetris.ttf", 60)
evenSmallerText = pygame.font.Font("Tetris.ttf", 40)
reallySmallText = pygame.font.Font("Tetris.ttf", 30)
#Creates variables for each of the different font sizes

pygame.mixer.music.load("Tetris.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
#Loads and plays the music

#FUNCTIONS####################################################################################################################################################################################################

#Function that draws the display screen
def gameScreen(): 
    screen.fill(background_grey) #Fills the background
    pygame.draw.rect(screen, outline, [15, 20, 510, 760], 5)
    pygame.draw.rect(screen, outline, [540, 170, 240, 200], 5) #Draws rectangles outlining the different sections of the screen
    pygame.draw.rect(screen, outline, [540, 440, 240, 200], 5)
    screen.blit(smallLogo, (540, 30)) #Draws the tetris logo

#Function that checks if the player has completed a row
def checkrow(grid):
    for row in grid: #For each row in the grid keeping track of the previously placed block positions,
        count = 0 #Create a varable for use inside the function as a counter
        for tile in row: #For each grid position in that row
            if tile > 0: #If there is a block occupying that spot,
                count += 1 #Add one to the count variable
        if count >= 10: #If the count variable is greater than or equal to 10, meaning there is a block in each spot on that row
            grid.remove(row) #Remove the row from the list, effectively destroying the blocks on that row
            grid.insert(0, [0,0,0,0,0,0,0,0,0,0]) #Add a new, empty row to the top, so all the other rows fall down into place
            return True

#Function that checks to see if the player has lost, meaning the blocks have gone too far up the play screen
def checklose(grid):
    for tile in grid[1]: #For each spot on the grid in the row the blocks cannot go past,
        if tile > 0: #Check to see if there is a block in that spot
            return True #If so, the user has lost and True is returned

#Function that displays the next tetrimino to drop in the top right corner of the screen
def drawNextTetrimino(nextShape, block):
    if nextShape == 0 or nextShape == 2:
        x = 610
        y = 215
    else:
        x = 635
        y = 215
    block.drawTetrimino(nextShape, x, y, 0, block.colours[nextShape])

#Function that handles drawing everything to the screen just before the display is updated
def Update(block, currentShape, orientation, nextShape, grid, score):
    
    gameScreen() #Call the function to draw the game screen
    
    block.drawTetrimino(currentShape, block.x, block.y, orientation, block.colours[currentShape]) #Draw the block in the new updated position
    
    #For loop that goes through each position on the grid. If a previously fallen tetrimino has a block who's position has been recorded in that square,
    #it scales the grid position up by the blocksizeand draws the block with pygame's draw.rect function in that position on the screen
    for row in range(0, 15, 1):
            for tile in range(0, len(grid[row]), 1):
                if grid[row][tile] > 0:
                    pygame.draw.rect(screen, block.colours[grid[row][tile] -1], [tile*block.blocksize + 20, row*block.blocksize + 25, block.blocksize, block.blocksize], 0)
                    pygame.draw.rect(screen, black, [tile*block.blocksize + 20, row*block.blocksize + 25, block.blocksize, block.blocksize], 5)
                    
    drawNextTetrimino(nextShape, block) #Call the function to draw the next tetrimino that will dropin the corner of the screen

    textSurf, textRect = text_objects("score", smallerText)
    textRect.center = (635, 420)
    screen.blit(textSurf, textRect)

    textSurf, textRect = text_objects(str(score), smallerText)
    textRect.center = (650, 520)
    screen.blit(textSurf, textRect)

    textSurf, textRect = text_objects("next", smallerText)
    textRect.center = (630, 140)
    screen.blit(textSurf, textRect)

    textSurf, textRect = text_objects("By Nick F.", evenSmallerText)
    textRect.center = (650, 750)
    screen.blit(textSurf, textRect)
    
    pygame.display.update() #Update the pygame screen display

def text_objects(text, font): #Function that helps with displaying text
    textSurface = font.render(text, True, black) #Creates a surface (image of text) in order to blit it on a surface, as just text on its own cannot be blitted
    return textSurface, textSurface.get_rect() #Returns the values of the surface
    

##############################################################################################################################################################################################################

#Block Class
class Block():
    
    #O, T, I, S, Z, L, J = 0, 1, 2, 3, 4, 5, 6
    #^List of all the block types and their corresponding integer value for reference^
    
    def __init__(self): #Initialize function, runs automatically


        self.x = 220
        self.y = 25 #Create variables for the x and y coordinates of the block, making them equal to the blocks starting position on the screen
        
        self.blocksize = 50 #Create a variable for the size of a block

        self.startinglist = [0, 1, 2, 5, 6] #List of block shapes that can be first dropped, as some blocks if dropped first will make it impossible to get a first row

        self.colours = [red, yellow, orange, lightblue, lightgreen, darkblue, pink] #List of block colours, corresponding to the order of the block types and their integer values

        #Creates big list of all the possible block types and their possible orientations, using a system that compares individual blocks' relative position to a center cell of the tetrimino(0, 0)
        #Basically, (1, 1) means that the position of that block in the tetrimino is one block to the right and one block down from the block that is the center of rotation in that tetrimino
        self.tetriminoTypes = [[ [ [0, 0], [ 1, 0], [ 0, 1], [ 1, 1] ],
                             [ [0, 0], [ 1, 0], [ 0, 1], [ 1, 1] ], ##
                             [ [0, 0], [ 1, 0], [ 0, 1], [ 1, 1] ], ##
                             [ [0, 0], [ 1, 0], [ 0, 1], [ 1, 1] ], 
                             ], #O shape list of orientations: there is only one possible orientation so each list is the same
                           [ [ [0, 0], [-1, 0], [ 1, 0], [ 0, 1] ],
                             [ [0, 0], [-1, 0], [0, -1], [ 0, 1] ], ###
                             [ [0, 0], [-1, 0], [1, 0],  [0, -1] ],  #
                             [ [0, 0], [0, -1], [ 1, 0], [ 0, 1] ],
                             ], #T shape list of orientations: 4 different rotations, so there are 4 different lists
                           [ [ [0, 0], [-1, 0], [ 1, 0], [ 2, 0] ], #
                             [ [0, 0], [0, -1], [ 0, 1], [ 0, 2] ], #
                             [ [0, 0], [-1, 0], [ 1, 0], [ 2, 0] ], #
                             [ [0, 0], [0, -1], [ 0, 1], [ 0, 2] ], #
                             ], #I shape list of orientations: 2 different rotations, so there are 2 different lists each repeated twice
                           [ [ [0, 0], [ 1, 0], [ 0, 1], [-1, 1] ],
                             [ [0, 0], [0, -1], [ 1, 0], [ 1, 1] ],  ##
                             [ [0, 0], [ 1, 0], [ 0, 1], [-1, 1] ], ##
                             [ [0, 0], [0, -1], [ 1, 0], [ 1, 1] ], 
                             ], #S shape list of orientations: 2 different rotations, so there are 2 different lists each repeated twice
                           [ [ [0, 0], [-1, 0], [ 0, 1], [ 1, 1] ],
                             [ [0, 0], [1, -1], [ 1, 0], [ 0, 1] ], ##
                             [ [0, 0], [-1, 0], [ 0, 1], [ 1, 1] ],  ##
                             [ [0, 0], [1, -1], [ 1, 0], [ 0, 1] ],
                             ], #Z shape list of orientations: 2 different rotations, so there are 2 different lists each repeated twice
                           [ [ [0, 0], [-1, 0], [-1, 1], [ 1, 0] ], #
                             [ [0, 0], [0, -1], [-1,-1], [ 0, 1] ], #
                             [ [0, 0], [1, -1], [ 1, 0], [-1, 0] ], ##
                             [ [0, 0], [0, -1], [ 0, 1], [ 1, 1] ],
                             ], #L shape list of orientations: 4 different rotations, so there are 4 different lists
                           [ [ [0, 0], [-1, 0], [ 1, 0], [ 1, 1] ],  #
                             [ [0, 0], [0, -1], [ 0, 1], [-1, 1] ],  #
                             [ [0, 0], [-1, 0], [-1,-1], [ 1, 0] ], ##
                             [ [0, 0], [0, -1], [1, -1], [ 0, 1] ], 
                            ] ] #J shape list of orientations: 4 different rotations, so there are 4 different lists
                            #The reason why sometimes rotations are repeated is for consistency as each different shape must have a list of possible rotations the same length
                            #This is to avoid list indexes being out of range and the ability to have a just single class that handles every block

    #Key function that draws an entire tetrimino
    def drawTetrimino(self, tetrimino, x, y, orientation, colour): 
        for cell in self.tetriminoTypes[tetrimino][orientation % 4]:
            #Uses a for loop to cycle through a specified list from the lists of tetrimino types based on the type of tetrimino and orientation that are accepted as parameters.
            #Using pygame's draw rectangle function, this takes the x and y position of the tetrimino, which is really the x and y coordinates of the top left of the cell in the tetrimino
            #that is the center of rotation, usually the middle one. Then draws the other cells outward from this according to the lists, taking into account that if the list says a block must be drawn one
            #block away from the center block in a certain direction, the parameter passed into the draw.rect function is multiplyed by the blocksize (50) to scale to the size of the screen.
                pygame.draw.rect(screen, colour, [x + cell[0]*self.blocksize, y + cell[1]*self.blocksize,
                                                 self.blocksize, self.blocksize], 0) #Draws a single cell in the tetrimino, filling it with a colour value that matches the value of the tetrimino shape
                pygame.draw.rect(screen, black, [x + cell[0]*self.blocksize, y + cell[1]*self.blocksize,
                                                 self.blocksize, self.blocksize], 5) #Draws the black outline of the cell in the tetrimino for added visual affect

    #Function that handles what happens when the block cannot fall anymore, and a new block must drop from the top
    def reset(self, grid, currentShape, rotation):
        for cell in self.tetriminoTypes[currentShape][rotation % 4]:
            grid[int((self.y + cell[1]*self.blocksize - 25)/ 50) -1][int((self.x + cell[0]*self.blocksize - 20)/ 50)] = currentShape + 1
            #For each cell in the tetrimino, divide its x and y positions by the blcoksize and update the values in a 10 by 15 scaled down grid of the screen
            #to keep track of where previous tetriminos have fallen. This ensures that multiple tetriminos can be present on the screen at the same time, while having only one that the player can move
        self.y = 25
        self.x = 220 #Reset the tetrimino being controlled by the player's x and y coordinates to the starting point so that the next tetrimino drops from the top

#Next three functions work the same, just dealing with different directions but running on the same principle
#They return a value of how far the farthest spot on the specified side (either down, left, or right) is away from the x and y coordinates of the center block of the tetrimino
#This is used in collision detection, as it must be done with the outermost sides of the tetrimino to work properly
#################################################################
    def down(self, tetrimino, rotation):
        y = self.tetriminoTypes[tetrimino][rotation % 4][0][1]
        for cell in self.tetriminoTypes[tetrimino][rotation % 4]:
            if cell[1] > y:
                y = cell[1]
        return y*self.blocksize

    def right(self, tetrimino, rotation):
        x = self.tetriminoTypes[tetrimino][rotation % 4][0][0]
        for cell in self.tetriminoTypes[tetrimino][rotation % 4]:
            if cell[0] > x:
                x = cell[0]
        return x*self.blocksize

    def left(self, tetrimino, rotation):
        x = self.tetriminoTypes[tetrimino][rotation % 4][0][0]
        for cell in self.tetriminoTypes[tetrimino][rotation % 4]:
            if cell[0] < x:
                x = cell[0]
        return x*self.blocksize
#################################################################

#End of block class

##############################################################################################################################################################################################################
#####LOOPS#####
#These functions each run a different loop for different variations of the game screen, so they are separate from the other functions

def introScreen(block):

    Exit = False #Create a variable to check in the while loop

    colour = random.choice(block.colours) #Choose a random colour for the blocks lining the borders
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        screen.fill(background_grey) #Fill the screen with the background colour

        #Next two for loops draw the blocks going alongthe top and bottom of the screen
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 0, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 0, 50, 50], 5)
            
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 750, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 750, 50, 50], 5)
            
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed

        #Draw play button, when hovered over change colour slightly, when clicked run the game loop
        if 600 > mouse[0] > 200 and 350 > mouse[1] > 250:
            pygame.draw.rect(screen, button_lightgrey, [150, 250, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 250, 500, 100], 5)
            if click[0] == 1:
                gameLoop()
        else:
            pygame.draw.rect(screen, button_darkgrey, [150, 250, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 250, 500, 100], 5)

        #Draw instructions button, when hovered over change colour slightly, when clicked go to instructions page
        if 600 > mouse[0] > 200 and 500 > mouse[1] > 400:
            pygame.draw.rect(screen, button_lightgrey, [150, 400, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 400, 500, 100], 5)
            if click[0] == 1:
                instructionsScreen(block)
        else:
            pygame.draw.rect(screen, button_darkgrey, [150, 400, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 400, 500, 100], 5)

        #Draw quit button, when hovered over change colour slightly, when clicked quit the game
        if 600 > mouse[0] > 200 and 650 > mouse[1] > 550:
            pygame.draw.rect(screen, button_lightgrey, [150, 550, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 550, 500, 100], 5)
            if click[0] == 1:
                Exit = True
        else:
            pygame.draw.rect(screen, button_darkgrey, [150, 550, 500, 100], 0)
            pygame.draw.rect(screen, black, [150, 550, 500, 100], 5)

        textSurf, textRect = text_objects("Play", text)
        textRect.center = (400, 300)
        screen.blit(textSurf, textRect) #Creates the play text and blits it to the screen

        textSurf, textRect = text_objects("Instructions", smallerText)
        textRect.center = (400, 450)
        screen.blit(textSurf, textRect) #Creates the instructions text and blits it too the screen

        textSurf, textRect = text_objects("Quit", text)
        textRect.center = (400, 600)
        screen.blit(textSurf, textRect) #Creates the quit text and blits it to the screen
        
        screen.blit(logo, (200, 75)) #Puts the logo onto the screen
        pygame.display.update() #Updates the pygame display
    pygame.quit()

def instructionsScreen(block):

    Exit = False #Create a variable to check in the while loop

    colour = random.choice(block.colours) #Choose a random colour for the blocks lining the borders
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        screen.fill(background_grey) #Fill the screen with the background colour

        #Next two for loops draw the blocks going alongthe top and bottom of the screen
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 0, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 0, 50, 50], 5)
            
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 750, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 750, 50, 50], 5)

        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed
        
        pygame.draw.rect(screen, button_darkgrey, [60, 60, 260, 130], 0)
        pygame.draw.rect(screen, black, [60, 60, 260, 130], 5)
        screen.blit(leftkey, (75, 75))
        screen.blit(rightkey, (200, 75))
        #Draw the boxes surrounding the left and right arrow keys, and blit the images of the keys onto the screen

        pygame.draw.rect(screen, button_darkgrey, [110, 200, 150, 150], 0)
        pygame.draw.rect(screen, black, [110, 200, 150, 150], 5)
        screen.blit(upkey, (135, 220))
        #Draw the box surrounding the up arrow key, and blit the image of the key onto the screen
        
        pygame.draw.rect(screen, button_darkgrey, [110, 365, 150, 150], 0)
        pygame.draw.rect(screen, black, [110, 365, 150, 150], 5)
        screen.blit(downkey, (135, 385))
        #Draw the box surrounding the down arrow key, and blit the image of the key onto the screen

        pygame.draw.rect(screen, button_darkgrey, [85, 535, 200, 100], 0)
        pygame.draw.rect(screen, black, [85, 535, 200, 100], 5)
        screen.blit(spacekey, (97.5, 560))
        #Draw the box surrounding the space bar, and blit the image of it onto the screen

        pygame.draw.rect(screen, black, [50, 650, 700, 80], 5)
        #Draw the box surrounding the object of the game text

        #Draw the back button, if hovered over change colour slightly
        if 75 > mouse[0] > 25 and 425 > mouse[1] > 375:
            pygame.draw.rect(screen, button_lightgrey, [25, 375, 50, 50], 0)
            pygame.draw.rect(screen, black, [25, 375, 50, 50], 5)
            if click[0] == 1:
                introScreen(block)
        else:
            pygame.draw.rect(screen, button_darkgrey, [25, 375, 50, 50], 0)
            pygame.draw.rect(screen, black, [25, 375, 50, 50], 5)

        screen.blit(arrow, (25, 375)) #blit the back arrow onto the screen
        
        textSurf, textRect = text_objects("Make full rows, don't let the blocks pile up.", reallySmallText)
        textRect.center = (400, 685)
        screen.blit(textSurf, textRect)
        #Add text describing the object of the game
        
        textSurf, textRect = text_objects("Move left and right", evenSmallerText)
        textRect.center = (550, 125)
        screen.blit(textSurf, textRect)
        #Add text 'Move left and right'

        textSurf, textRect = text_objects("Rotate", text)
        textRect.center = (550, 275)
        screen.blit(textSurf, textRect)
        #Add text 'Rotate'
        
        textSurf, textRect = text_objects("Drop Faster", text)
        textRect.center = (550, 435)
        screen.blit(textSurf, textRect)
        #Add text 'Drop Faster'

        textSurf, textRect = text_objects("Drop Instantly", smallerText)
        textRect.center = (550, 585)
        screen.blit(textSurf, textRect)
        #Add text 'Drop Instantly
        
        pygame.display.update() #Updates the pygame display
    pygame.quit()

def losingScreen(block, score):

    Exit = False #Create a variable to check in the while loop

    colour = random.choice(block.colours) #Choose a random colour for the blocks lining the borders
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        screen.fill(background_grey) #Fill the screen with the background colour

        #Next two for loops draw the blocks going alongthe top and bottom of the screen
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 0, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 0, 50, 50], 5)
            
        for pos in range(0, 801, 50):
            pygame.draw.rect(screen, colour, [pos, 750, 50, 50], 0)
            pygame.draw.rect(screen, black, [pos, 750, 50, 50], 5)
            
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed

        pygame.draw.rect(screen, button_lightgrey, [150, 200, 500, 200], 0)
        pygame.draw.rect(screen, black, [150, 200, 500, 200], 5)
        #Draw the center rectangle where the score is displayed

        #Draw retry button, when hovered over change colour sligjtly, when clicked restart the game loop
        if 350 > mouse[0] > 150 and 550 > mouse[1] > 450:
            pygame.draw.rect(screen, button_lightgrey, [150, 450, 200, 100], 0)
            pygame.draw.rect(screen, black, [150, 450, 200, 100], 5)
            if click[0] == 1:
                gameLoop()
        else:
            pygame.draw.rect(screen, button_darkgrey, [150, 450, 200, 100], 0)
            pygame.draw.rect(screen, black, [150, 450, 200, 100], 5)

        #Draw quit button, when hovered over change colour slightly, when clicked quit the game
        if 650 > mouse[0] > 450 and 550 > mouse[1] > 450:
            pygame.draw.rect(screen, button_lightgrey, [450, 450, 200, 100], 0)
            pygame.draw.rect(screen, black, [450, 450, 200, 100], 5)
            if click[0] == 1:
                Exit = True
        else:
            pygame.draw.rect(screen, button_darkgrey, [450, 450, 200, 100], 0)
            pygame.draw.rect(screen, black, [450, 450, 200, 100], 5)
            

        textSurf, textRect = text_objects("Retry", smallerText)
        textRect.center = (250, 500)
        screen.blit(textSurf, textRect) #Creates the retry text and blits it to the screen

        textSurf, textRect = text_objects("Quit", text)
        textRect.center = (550, 500)
        screen.blit(textSurf, textRect) #Creates the quit text and blits it to the screen
        
        textSurf, textRect = text_objects("You Lose!", text)
        textRect.center = (400, 150)
        screen.blit(textSurf, textRect) #Creates the 'You lose!' text and blits it too the screen

        scoreMessage = ("Score: " + str(score))
        textSurf, textRect = text_objects(scoreMessage, text)
        textRect.center = (400, 300)
        screen.blit(textSurf, textRect) #Creates the 'Score: _' text and blits it too the screen

        screen.blit(smallLogo, (280, 625)) #Blits the logo onto the screen

        pygame.display.update() #Updates the pygame display
    pygame.quit()

def gameLoop(): #Loop for the main playing screen of the game
    
    block = Block() #This creates the block class and attaches it to the variable block

    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
    #Empty list of the grid that's values are changed in correspondance to the previously fallen tetriminos to keep track of where to redraw them on the screen

    nextShape = random.randint(0, 6) #Create a variable for the next block shape to drop, and randomly choose a value from a range representing all of the blocks

    currentShape = random.choice(block.startinglist) #Create a variable for the current block that is dropping, and assign a random value to it from the list of possible starting blocks

    orientation = 0 #Create a variable used with modulus 4 to keep track of the rotation of a tetrimino, as it must stay as an integer between 0 and 3 to navigate the rotation lists.
                    #One is added to this variable each time the tetrimino is rotated, and the modulus 4 keeps it within the required range

    sleep = 0.5 #Frequency in seconds of when the screen is updated, to delay the falling of the tetrimino to a playable speed

    start_time = time.clock() #Makes use of the time.clock function from the time module to set a start time for the time cycle of the game, used in determining how often to update

    score = 0 #Create a variable to keep track of the score

    running = True #While this variable is true, the gameloop will continue to run
    
    #Everything in this continuously runs, constantly updating the screen and allowing the game to keep running and be played
    while running:
        
        t = time.clock() #Varable that is constantly being updated that keeps track of the current time in the time cycle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #If x is pressed on the pygame window, stop running the gameloop
                
            if event.type == pygame.KEYDOWN: #If any key is pressed down
                
                if event.key == pygame.K_RIGHT: #If that key is the right arrow key,
                    if int((block.x + block.right(currentShape, orientation)) / 50) + 1 < 10: #Detect if the tetrimino has collided with the edge of the play area, and if not
                        block.x += block.blocksize #Move the tetrimino one block to the right
                        #For instant update without the delay from the update cycle, as that will affect the precision of the controls, immediately update the entire game screen with the new tetrimino position
                        Update(block, currentShape, orientation, nextShape, grid, score) #Call the function to update the screen

                if event.key == pygame.K_LEFT: #If that key is the right arrow key
                    if int((block.x + block.left(currentShape, orientation)) / 50) - 1 >= 0: #Detect if the tetrimino has collided with the edge of the play area, and if not
                        block.x -= block.blocksize #Move the tetrimino one block to the left
                        #For instant update without the delay from the update cycle, as that will affect the precision of the controls, immediately update the entire game screen with the new tetrimino position
                        Update(block, currentShape, orientation, nextShape, grid, score) #Call the function to update the screen

                if event.key == pygame.K_SPACE: #If that key is the spacebar
                    sleep = 0 #Make the duration of how long it waits to update 0, so the block falls completely to the bottom
                    
                if event.key == pygame.K_DOWN: #If that key is the down arrow key
                    sleep = 0.05 #Make the duration of how long it waits to update shorter, so the block falls faster

                if event.key == pygame.K_UP: #If that key is the up arrow key
                    orientation += 1 #Change the variable for the orientation of the block
                    #For instant update without the delay from the update cycle, as that will affect the precision of the controls, immediately update the entire game screen with the new tetrimino orientation
                    Update(block, currentShape, orientation, nextShape, grid, score) #Call the function to update the screen
                    
            if event.type == pygame.KEYUP: #If any key is released
                
                if event.key == pygame.K_SPACE: #If that key is the spacebar, set the amount of time between updates back to default
                    sleep = 0.5
                if event.key == pygame.K_DOWN: #If that key is the down arrow key, set the amount of time between updates back to default
                    sleep = 0.5
                    
        pygame.event.pump() #Clears events so that multiple events do not build up if the key is pressed multiple times, to make controls smoother. Keys cannot be held because of this, but it is much better

        if t - start_time >= sleep: #If the amount of time between updates has passed

            if block.down(currentShape, orientation) + block.y >= 775: #Collision detection to see if the position the tetrimino will be updated into is off the bottom of the screen. If it is,
                Update(block, currentShape, orientation, nextShape, grid, score) #Call the function to update the screen
                block.reset(grid, currentShape, orientation) #Call the reset function from the block class to record the positions of all the blocks of the tetrimino in the grid as it is done falling
                #Everything from this point on deals with the new tetrimino that will drop next, so all the variables must be reset 
                orientation = 0 #Reset the orientation to the starting one
                currentShape = nextShape #Make the new current shape equal to what the next shape is, which is previously determined randomly each time
                nextShape = random.randint(0, 6) #Choose a new next shape
                sleep = 0.5 #Reset the amount of time between updates to 0, in case spacebar or down arrow key was used to drop the old tetrimino, so the new tetrimino is going at the correct starting speed

            for cell in range(4): #Collision detecting between tetrimino dropping and previously fallen blocks. For each cell in the tetrimino, which is always composed of 4 blocks,
                if grid[int((block.y + block.tetriminoTypes[currentShape][orientation % 4][cell][1] * 50)/50)]\
                [int((block.x + block.tetriminoTypes[currentShape][orientation % 4][cell][0] * 50)/50)] > 0: #Scale the current x and y position down to a position on the grid, and see if the spot it will be
                    #updated to is already occupied by another block dropped previously. If it is,
                    block.drawTetrimino(currentShape, block.x, block.y - block.blocksize, orientation, block.colours[currentShape]) #Draw the tetrimino one block above the old position, ie old position
                    block.reset(grid, currentShape, orientation) #Call the reset function from the block class to record the positions of all the blocks of the tetrimino in the grid as it is done falling
                #Everything from this point on deals with the new tetrimino that will drop next, so all the variables must be reset
                    orientation = 0 #Reset the orientation to the starting one
                    currentShape = nextShape #Make the new current shape equal to what the next shape is, which is previously determined randomly each time
                    nextShape = random.randint(0, 6) #Choose a new next shape
                    sleep = 0.5 #Reset the amount of time between updates to 0, in case spacebar or down arrow key was used to drop the old tetrimino, so the new tetrimino is going at the correct starting speed
                    break #Break the loop, as the for loop will run this multiple times creating issues if more than one cell collides, as it will reset and draw to the grid more than necessary
            else: #If no collisons have occured
                Update(block, currentShape, orientation, nextShape, grid, score)
            block.y += block.blocksize #Update the y coordinates of the block so the position changes for next loop, making it fall down by one block at a time
            if checkrow(grid) == True:#Call the function to check to see if the player has completed a row, and it will act accordingly deleting the row
                score += 100
            if checklose(grid) == True: #Call the function to check to see if the player has lost the game, and if they have
                losingScreen(block, score)
            start_time = time.clock() #Reassign the start time of the duration between updates to whatever the current time is for the next loop
    pygame.quit()

introScreen(Block())

pygame.quit() #If the loop has been broken, close the pygame window


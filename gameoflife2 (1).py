import time
from itertools import product
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import RegularPolygon

#relative coordinates
hex_neighbors = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]


class ConwaysGame():
    def __init__(self):         #initialisation
        self.map = [[]]
        self.size = 0
        self.size = 0
        self.genCount = 1           # stores the current generation no
        self.deadList = []          # stores records of the dying cells in the format [x coord, y coord, gen no of death, method of death(id)]
        self.resList = []           # stores records of ressurected cells in the same format as deadList

    def set_world_size(self, size):        #to set the dimensions of game
        self.size = size
        self.map = [[0 for i in range(size)] for i in range(size)]

    def randomly_generate(self) :       #function to randomly generate initial pattern
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.map[x][y] = random.randint(0,1)

    def populate(self, x, y):            #function to revive a cell
        self.map[x][y] = 1

    def cell_is_alive(self, x, y):          #function to check the status of a cell
        return self.map[x][y] == 1

    def number_of_live_neighbours(self, x, y):      #function to count no of living neighbors
        live_neighbors = 0
        for k in range(6):
            nx = x + hex_neighbors[k][0]
            ny = y + hex_neighbors[k][1]
            if 0 <= nx < self.size and 0 <= ny < self.size:
                live_neighbors += self.map[nx][ny]
        return live_neighbors


    def step(self):                  #function to create the next generation
        new_map = [[0 for i in range(self.size)] for i in range(self.size)]
        for x in range(0, self.size):
            for y in range(0, self.size):
                # rule 1
                if self.cell_is_alive(x, y) == True and \
                    self.number_of_live_neighbours(x, y) < 2:
                    if self.resList == [] :              # to start the loop initially
                        new_map[x][y] = 0
                        id = 0                      # id for underpopulation death = 0
                        self.deadList += [[x,y,self.genCount,id]]       #save current death record
                    else :
                        for i in self.resList :
                            if i[0] == x and i[1] == y and i[3] == 0 :
                                break
                            else :
                                new_map[x][y] = 0
                                id = 0
                                for i in self.deadList :
                                    if i[0] == x and i[1] == y :
                                        self.deadList.remove(i)     # remove prev records of the same cell, if any
                                for i in self.resList :
                                    if i[0] == x and i[1] == y :
                                        self.resList.remove(i)
                                self.deadList += [[x,y,self.genCount,id]]       #save current death record
                    
                # rule 2
                if self.cell_is_alive(x, y) == True and \
                   (self.number_of_live_neighbours(x, y) == 2 or \
                   self.number_of_live_neighbours(x, y) == 3):
                    new_map[x][y] = 1
                # rule 3
                if self.cell_is_alive(x, y) == True and \
                   self.number_of_live_neighbours(x, y) > 3:
                    if self.resList == [] :
                        new_map[x][y] = 0
                        id = 1                  # id for overpopulation death = 1
                        self.deadList += [[x,y,self.genCount,id]]       #save current death record
                    else :
                        for i in self.resList :
                            if i[0] == x and i[1] == y and i[3] == 1 :
                                break           # rule 6 (avoid death by underpopulation)
                            else :
                                new_map[x][y] = 0       #kill
                                id = 1
                                for i in self.deadList :
                                    if i[0] == x and i[1] == y :
                                        self.deadList.remove(i)        # remove prev records of the same cell, if any
                                for i in self.resList :
                                    if i[0] == x and i[1] == y :
                                        self.resList.remove(i)
                                self.deadList += [[x,y,self.genCount,id]]       #save current death record
                # rule 4
                if self.cell_is_alive(x, y) == False and \
                   self.number_of_live_neighbours(x, y) == 3:
                    new_map[x][y] = 1           #survive
                    for i in self.deadList :
                        if i[0] == x and i[1] == y :
                            self.deadList.remove(i)         # remove the death records of this cell, if any
                    for i in self.resList :
                        if i[0] == x and i[1] == y :
                            self.resList.remove(i)
                # rule 5
                for i in self.deadList :
                    if self.genCount-i[2] == 6 :
                        new_map[i[0]][i[1]] = 1
                        self.resList += [i]              #save current ressurected record
                
        # rule 7 -> The most interesting part of the whole task..
        if self.genCount % 4 == 0 :
            x1 = random.randint(0, self.size-1)
            y1 = random.randint(0, self.size-1)
            while self.cell_is_alive(x1, y1) == True :
                x1 = random.randint(0, self.size-1)
                y1 = random.randint(0, self.size-1)
            new_map[x1][y1] = 1
            for i in self.deadList :
                if i[0] == x and i[1] == y :
                    self.deadList.remove(i)          # remove prev records of the same cell, if any
            for i in self.resList :
                if i[0] == x and i[1] == y :
                    self.resList.remove(i)


                    
                

        self.map = new_map          # update the map for next gen
        return

    

if __name__ == '__main__':
    game = ConwaysGame()
    
    #user input
    s = int(input("Enter the side of the world: "))
    game.set_world_size(s)

    print("\nPick a choice: \n1. Run a sample case \n2. Randomly generate initial case \n3. Manually input initial generation ")
    u = int(input ("Enter your choice(1/2/3): "))
    if u == 1 :
        game.populate(2, 1)
        game.populate(3, 2)
        game.populate(1, 3)
        game.populate(2, 3)
        game.populate(3, 3)

    elif u == 2 :
        game.randomly_generate()

    else :
        n = int(input("\nEnter no of live cells: "))
        for i in range (n) :
            x,y = map(int,input("Enter the coordinates of the live cells #"+str(i+1)+": ").split())
            game.populate(x-1, y-1)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot initial state
    hex_size = 0.5
    hex_patches = []
    for i in range(game.size):
        for j in range(game.size):
            x = j * np.sqrt(3) + (i % 2) * np.sqrt(3) / 2
            y = i * 1.5
            hexagon = RegularPolygon((x, y), numVertices=6, radius=hex_size, orientation=np.pi / 2, edgecolor='k', lw=1, facecolor='white' if game.map[i][j] == 0 else 'black')
            hex_patches.append(hexagon)
            ax.add_patch(hexagon)

    ax.set_aspect('equal')
    ax.autoscale_view()
    ax.axis('off')

    # Function to update the plot for each frame
    def update(frame):
        global hex_patches
        game.step()
        game.genCount+=1
        for i in range(game.size):
            for j in range(game.size):
                hex_patches[i * game.size + j].set_facecolor('white' if game.map[i][j] == 0 else 'black')
        return hex_patches

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=range(100), interval=200)

    plt.show()      # enjoy the game !

    # Save the animation as GIF
    ani.save('game_of_life.gif', writer='pillow')
    print ("\nGIF file saved successfully, thank you !!")

    


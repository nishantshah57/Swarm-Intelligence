import numpy as np
from matplotlib import pyplot
import matplotlib as mpl

class Schelling:
    def __init__(self, width, height, threshold):
        self.width = width
        self.height = height
        self.threshold = threshold
        self.middle = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.empty = 0
        self.world = []

    def initial_world(self):
        self.world = np.random.choice(3, size = (self.width, self.height), p = [0.5,0.25,0.25]) * 5
        return self.world

    # Finds the neighbor cells of the Agent
    def neighbors_check(self,row,col):
        check = self.middle
        if row <= self.width-1 and col <= self.height-1:
            not_needed_cells = [] # not_needed_cells collects the index of the negative indices
            for k in range(len(check)):
                try:
                    if (row + check[k][0] < 0) or (col + check[k][1] < 0):
                        not_needed_cells.append(k)
                    # Imagine the last row and last column where the index will be out of bound
                    self.world[row + check[k][0], col + check[k][1]]
                except IndexError:
                    not_needed_cells.append(k)
                    pass
            check = np.delete(check, not_needed_cells, axis = 0)
            return check

    # Compares to the threshold value and finds if agent is happy or not
    # Agent = color = (5 = Black) and (10 = Blue)
    def satisfied(self,check,Agent,row,col):
        count_similar = 0
        count_different = 0
        empty_cell = 0

        for i in range(len(check)):
            if self.world[row + check[i][0]][col + check[i][1]] == Agent:
                count_similar += 1
            elif self.world[check[i][0] + row][check[i][1] + col] == self.empty:
                empty_cell += 1
            else:
                count_different += 1
        if count_similar+count_different == 0:
            return False
        else:
            return float(count_similar)/(count_similar + count_different) >= self.threshold

    # Creates a flagged empty world of unsatisfied_world agents
    def unsatisfied_world(self,row,col):
        unhappy_world = np.zeros(self.world.shape)
        for i in range(self.world.shape[0]):
            for j in range(self.world.shape[1]):
                Agent = self.world[i][j]
                if Agent:
                    neighbors = self.neighbors_check(i,j)
                    if not self.satisfied(neighbors,Agent,i,j):
                        unhappy_world[i][j] = 1
        return unhappy_world

    # Creates a flagged empty world for empty space in the original world
    def empty_world(self):
        sad_world = np.zeros(self.world.shape)
        for i in range(len(self.world)):
            for j in range(len(self.world[1])):
                if self.world[i][j] == 0:
                    sad_world[i][j] = 1
        return sad_world

    # Finds a happy neighborhood for the unsatisfied_world agent
    # There are some glitches in this part, need to improve this part
    def find_neighborhood(self,empty_space,Agent,row,col,iteration):
        if row == (self.width - 1) and col == (self.width - 1):
            row,col = 0,0
        for i in range(row,self.width):
            for j in range(col,self.height):
                if empty_space[i][j]:
                    neighbors = self.neighbors_check(i,j)
                    if self.satisfied(neighbors,Agent,i,j):
                        empty_space[i][j] == 0
                        return i,j
                    else:
                        iteration += 1
                        if iteration > max(self.world.shape):
                            return i,j
                        return self.find_neighborhood(empty_space,Agent,i,j,iteration)

    # Updates the current world by more satisfied world
    def new_world(self, unhappy_world,empty_space):
        i1, j1 = [], []
        for i in range(unhappy_world.shape[0]):
            for j in range(unhappy_world.shape[1]):
                Agent = unhappy_world[i,j]
                if Agent:
                    Color = self.world[i][j]
                    iteration = 0
                    i1,j1 = self.find_neighborhood(empty_space,Agent,i,j,iteration)
                    self.world[i,j] = 0
                    self.world[i1,j1] = Color # = Color # = Agent
        return self.world


def main():
    # Initialize instance of class Schelling
    Schelling_Model = Schelling(50,50, 0.3)
    Schelling_Model.initial_world()
    # Display initial disordered world
    pyplot.figure(figsize = (10,10))
    cmap = mpl.colors.ListedColormap(['white', 'black', 'blue'])
    bounds = [-1, 2.5, 7.5, 11]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    # tell imshow about color map so that only set colors are used
    img = pyplot.imshow(Schelling_Model.world,interpolation='nearest',cmap = cmap,norm=norm)
    pyplot.title("Initial World without Segregation having grid size {0}x{1} with threshold {2}%".format(int(Schelling_Model.width),
        int(Schelling_Model.height),int(Schelling_Model.threshold * 100)), fontsize = 20)
    pyplot.show()
    iterations = 0
    row = 0
    col = 0
    while True:
        unhappy_world = Schelling_Model.unsatisfied_world(row, col)
        empty_space = Schelling_Model.empty_world()
        empty_space = empty_space.astype(int)
        if ((np.count_nonzero(unhappy_world)==0) or iterations>500):
           break
        world = Schelling_Model.new_world(unhappy_world,empty_space)
        iterations += 1
    pyplot.figure(figsize = (10,10))
    cmap = mpl.colors.ListedColormap(['white', 'black', 'blue'])
    bounds = [-1, 2.5, 7.5, 11]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    img = pyplot.imshow(Schelling_Model.world,interpolation='nearest',cmap = cmap,norm=norm)
    pyplot.title("Segregated World after {0} Iterations having grid size {1}x{2} with threshold {3}%".format(iterations,
        int(Schelling_Model.width),int(Schelling_Model.height),int(Schelling_Model.threshold*100)), fontsize = 20)
    pyplot.show()


if __name__ == "__main__":
    main()

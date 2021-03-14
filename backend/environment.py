class Environment:
    """Environment class for shape operations
    ...
    Attributes
    ----------
    GRID_SIZE : int
        The size of GRID, predefined 4.
    SHAPES : list(str)
        The valid list of shapes that can be inserted in GRID.
    COLORS : list(str)
        The valid list of colors that can be added to GRID.
    CLAW_POS: (int,int)
        Used to hold the position of a shape. By default initialises at middle of grid.
    GRID : list(list(tuple(str,str,int)))
        A 2D array of tuples containing shape, color, height.

    Methods
    -------
    findShape(shape,color=None,height=0)
        Returns a list of all matching shapes present in GRID.
    addShape(row,column,shape,color,height)
        Add a shape to specified (row,column) of GRID.
    delShape(row,column)
        Delete the shape from specified (row,column) of GRID.
    moveShape(x1,y1,x2,y2)
        Moves the shape from (x1,y1) to (x2,y2).
    holdShape(row,col)
        Hold the shape at specified (row,column).
    clearBoard
        Clear the Grid
    showGrid
        Print the grid"""

    def __init__(self):
        self.GRID_SIZE = 4
        self.SHAPES = ["CUBE", "PYRAMID", "BOX"]
        self.COLORS = ["RED", "BLUE", "GREEN"]
        self.CLAW_POS = (self.GRID_SIZE//2, self.GRID_SIZE//2)
        self.GRID = [[("", "", 0) for i in range(self.GRID_SIZE)] for j in range(self.GRID_SIZE)]  # Tuple is (shape, color, height)

    def findShape(self,shape, color=None, height=0):
        """Returns all shapes found based on given parameters"""
        foundShapes = []

        for y, row in enumerate(self.GRID):
            for x, pos in enumerate(row):
                found = True
                if shape != pos[0]:
                    found = False
                    continue
                if color:
                    if color in self.COLORS:
                        if color != pos[1]:
                            found = False
                            continue
                    else:
                        found = False
                        continue
                if height:
                    if height != pos[2]:
                        found = False

                if found:
                    foundShapes.append((y, x))

        return foundShapes

    def addShape(self,row: int,col: int, shape: str, color: str, height = 0) -> None:
        """Add a shape to the grid at specified row and column
        """
        if shape in self.SHAPES and color in self.COLORS:
            self.GRID[row][col] = (shape, color, height)

    def delShape(self,row: int,col: int)-> None:
        """Deletes the shape at (row,col) position of grid.
        :raise ValueError if row and col does not lie within grid."""
        try:
            self.GRID[row][col] = ("", "", 0)
        except:
            raise ValueError('Enter values of within range(0,%d)'%self.GRID_SIZE)


    #x1,y1 is moving from
    #x2,y2 is moving to
    def moveShape(self,x1: int,y1: int,x2: int,y2: int)-> None:
        """Move the shape from (x1,y1) -> (x2,y2)
        :raise ValueError if row and col does not lie within grid."""
        try:
            self.GRID[x2][y2] = self.GRID[x1][y1]
            self.delShape(x1, y1)
        except:
            raise ValueError('Enter values of within range(0,%d)'%self.GRID_SIZE)


    def holdShape(self,row: int,col: int)-> None:
        """Hold the shape at (row,col) in self.CLAW_POS.
        :raise ValueError if row and col does not lie within grid."""
        try:
            self.CLAW_POS = row, col
        except:
            raise ValueError('Enter values of within range(0,%d)'%self.GRID_SIZE)

    def clearBoard(self)-> None:
        """Clears the GRID"""
        # instead of using nested for loops initialing the grid as empty
        self.GRID = [[("", "", 0) for i in range(self.GRID_SIZE)] for j in range(self.GRID_SIZE)]  # Tuple is (shape, color, height)

    def showGrid(self)-> None:
        """Print the GRID."""
        print(*self.GRID,sep='\n')

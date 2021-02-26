GRID_SIZE = 4
#Tuple is (shape, color, height)
GRID = [[("", "", 0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

SHAPES = set(["CUBE", "PYRAMID", "BOX"])
COLORS = set(["RED", "BLUE", "GREEN"])
CLAW_POS = GRID_SIZE // 2, GRID_SIZE // 2

#Change height parameter in functions to a lambda to check for comparison words:
#ie. Find a block that is TALLER than this pyramid

#returns all shapes found based on given parameters
def findShape(shape, color = None,height = 0):
    foundShapes = []

    for y, row in enumerate(GRID):
        for x, pos in enumerate(row):
            found = True
            if SHAPES[shape] != pos[0]:
                found = False
            if color:
                if color in COLORS:
                    if COLORS[color] != pos[1]:
                        found = False
                else:
                    found = False
            if height:
                if height != pos[2]:
                    found = False

            if found:
                foundShapes.append((x, y))

    return foundShapes

def addShape(row,col, shape, color, height = 0):
    global GRID

    if shape in SHAPES and color in COLORS:
        GRID[row][col] = (SHAPES[shape], COLORS[color], height)

def delShape(row,col):
    global GRID

    GRID[row][col] = (0, 0, 0)


#x1,y1 is moving from
#x2,y2 is moving to
def moveShape(x1,y1,x2,y2):
    global  GRID

    GRID[x2][y2] = GRID[x1][y1]
    delShape(x1, y1)


def holdShape(row,col):
    global CLAW_POS
    CLAW_POS = row, col


def showGrid():
    for i in GRID:
        print(i)


GridSize = 4
#Tuple is (shape, color, height)
Grid = [[(0,0,0) for i in range(GridSize)] for j in range(GridSize)]

shapes = {"cube": 1, "pyramid": 2, "box": 3}
colors = {"red": 1, "blue": 2, "green": 3}
claw_pos = GridSize // 2, GridSize // 2

#Change height parameter in functions to a lambda to check for comparison words:
#ie. Find a block that is TALLER than this pyramid

def findShape(shape, color = None,height = 0):
    foundShapes = []

    for y, row in enumerate(Grid):
        for x, pos in enumerate(row):
            found = True
            if shapes[shape] != pos[0]:
                found = False
            if color:
                if color in colors:
                    if colors[color] != pos[1]:
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
    global Grid

    if shape in shapes and color in colors:
        Grid[row][col] = (shapes[shape],colors[color],height)

def delShape(row,col):
    global Grid

    Grid[row][col] = (0,0,0)


#x1,y1 is moving from
#x2,y2 is moving to
def moveShape(x1,y1,x2,y2):
    global  Grid

    Grid[x2][y2] = Grid[x1][y1]
    delShape(x1, y1)


def holdShape(row,col):
    global claw_pos
    claw_pos = row,col


def showGrid():
    for i in Grid:
        print(i)

def test():
    x = 1
    y = 2
    shape = 'cube'
    color = 'red'

    addShape(x,y,shape, color)

    showGrid()

    print(findShape(shape))


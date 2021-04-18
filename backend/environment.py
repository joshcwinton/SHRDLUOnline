from render import renderEnvironment

GRID_SIZE = 4
# Tuple is (shape, color, height)
GRID = [[("", "", 0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

SHAPES = set(["CUBE", "PYRAMID", "SPHERE"])
COLORS = set(["RED", "BLUE", "GREEN"])
CLAW_POS = GRID_SIZE // 2, GRID_SIZE // 2
MESSAGES = []  # Stores a list of messages
HISTORY = []  # Stores a list of grids


def findShape(shape, color=None, height=0):
    """ Returns all shapes found based on given parameters
    TODO: Change height parameter in functions to a lambda to check for comparison words:
    ie. Find a block that is TALLER than this pyramid
    """
    foundShapes = []

    for y, row in enumerate(GRID):
        for x, pos in enumerate(row):
            found = True
            if shape != pos[0]:
                found = False
            if color:
                if color in COLORS:
                    if color != pos[1]:
                        found = False
                else:
                    found = False
            if height:
                if height != pos[2]:
                    found = False

            if found:
                foundShapes.append((y, x))

    return foundShapes


def addShape(row, col, shape, color, height=0):
    global GRID

    if shape in SHAPES and color in COLORS:
        GRID[row][col] = (shape, color, height)

    renderEnvironment(GRID)


def delShape(row, col):
    global GRID

    GRID[row][col] = ("", "", 0)

    renderEnvironment(GRID)


def moveShape(x1, y1, x2, y2):
    """x1,y1 is moving from
    x2,y2 is moving to"""
    global GRID

    GRID[x2][y2] = GRID[x1][y1]

    delShape(x1, y1)

    renderEnvironment(GRID)


def holdShape(row, col):
    global CLAW_POS
    CLAW_POS = row, col


def clearBoard():
    global GRID
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            GRID[x][y] = ("", "", 0)

    renderEnvironment(GRID)


def undo():
    global GRID

    if len(HISTORY) != 0:
        GRID = HISTORY.pop()
        MESSAGES.append({"name": "Me", "Undo Action": inputMessage})
        MESSAGES.append({"name": "SHRDLU", "Okay": outputMessage})
        return True
    else:
        MESSAGES.append({"name": "Me", "Undo Action": inputMessage})
        MESSAGES.append(
            {"name": "SHRDLU", "No Actions to undo": outputMessage})

    return False


renderEnvironment(GRID)


def showGrid():
    for i in GRID:
        print(i)

    renderEnvironment(GRID)


def getEnvironment():
    return(GRID)


def updateHistory(currentEnv, inputMessage, outputMessage, parsedMessage):
    """"Adds information about a single interaction with SHRDLU to the history

    Args:
        currentEnv: Resulting grid after interaction
        inputMessage (str): Message sent by the user
        outputMessage (str): Response from SHRDLU
        parsedMessage (tuple): (shape, color, action, row, col)
    """

    # TODO: Update this to update database instead of global variable
    MESSAGES.append({"name": "Me", "text": inputMessage})
    MESSAGES.append({"name": "SHRDLU", "text": outputMessage})
    HISTORY.append(currentEnv)


def getMessages():
    return(MESSAGES)


def getEnvironmentHistory():
    return(HISTORY)

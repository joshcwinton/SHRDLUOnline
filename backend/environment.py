from render import renderEnvironment
import copy
from dbqueries import test, storeField, retrieveField


GRID_SIZE = 4

# Tuple is (shape, color, height)
GRID = [[("", "", 0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

SHAPES = set(["CUBE", "PYRAMID", "SPHERE"])
COLORS = set(["RED", "BLUE", "GREEN"])
CLAW_POS = GRID_SIZE // 2, GRID_SIZE // 2
MESSAGES = []   # Stores a list of messages
HISTORY = []    # Stores a list of grids


INSTANCES = [
    {
        "name": "Josh's World",
        "creator": "Josh",
        "size": 4,
        "lastUpdated": "??",
        "url": "/",
    },
    {
        "name": "Donald's World",
        "creator": "Donald",
        "size": 5,
        "lastUpdated": "??",
        "url": "/",
    },
    {
        "name": "Saurav's World",
        "creator": "Saurav",
        "size": 6,
        "lastUpdated": "??",
        "url": "/",
    },
    {
        "name": "Jasper's World",
        "creator": "Jasper",
        "size": 7,
        "lastUpdated": "??",
        "url": "/",
    },
]


def findShape(shape, color=None, height=0):
    """Returns all shapes found based on given parameters
    TODO: Change height parameter in functions to a lambda to check for
    comparison words:
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
    """x1,y1 is moving  from
    x2,y2 is moving to"""
    global GRID

    GRID[x2][y2] = GRID[x1][y1]

    delShape(x1, y1)

    renderEnvironment(GRID)


def holdShape(row, col):
    global CLAW_POS
    CLAW_POS = row, col


def clearBoardAppStart():
    """Used to clear the board on app start"""
    global GRID
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            GRID[x][y] = ("", "", 0)
    renderEnvironment(GRID)


def clearBoard():
    """used for clear board route."""
    global GRID, HISTORY, MESSAGES
    ret = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            GRID[x][y] = ("", "", 0)

    MESSAGES.append({"name": "Me", "text": "Clear board"})
    MESSAGES.append({"name": "SHRDLU", "text": "Board cleared"})
    ret.append({"name": "Me", "text": "Clear board"})
    ret.append({"name": "SHRDLU", "text": "Board cleared"})
    HISTORY = []
    renderEnvironment(GRID)
    return ret


def undo():
    global GRID, HISTORY, MESSAGES
    ret = []
    MESSAGES.append({"name": "Me", "text": "Undo Action"})
    ret.append({"name": "Me", "text": "Undo Action"})
    # Don't do anything if there is no history
    if len(HISTORY) == 0:
        MESSAGES.append({"name": "SHRDLU", "text": "No action to undo"})
        ret.append({"name": "SHRDLU", "text": "No action to undo"})

    else:
        # special case if there is only one prev env.
        if len(HISTORY) == 1:
            HISTORY.pop()
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    GRID[x][y] = ("", "", 0)
        else:
            HISTORY.pop()
            GRID = HISTORY[-1]
        MESSAGES.append({"name": "SHRDLU", "text": "Okay"})
        ret.append({"name": "SHRDLU", "text": "Okay"})
    renderEnvironment(GRID)
    return ret


def getPosition(row, col):
    return GRID[row][col]


def showGrid():
    for i in GRID:
        print(i)

    renderEnvironment(GRID)


def getEnvironment():
    """Get a deepcopy"""
    return copy.deepcopy(GRID)


def updateHistory(currentEnv, inputMessage, outputMessage, parsedMessage):
    global HISTORY
    """"Adds information about a single interaction with SHRDLU to the history

    Args:
        currentEnv: Resulting grid after interaction
        inputMessage (str): Message sent by the user
        outputMessage (str): Response from SHRDLU
        parsedMessage (tuple): (shape, color, action, row, col)
    """
    # TODO: Update this to update database instead of global variable
    updateMessage(inputMessage, outputMessage)
    HISTORY.append(currentEnv)


def updateMessage(inputMessage, outputMessage):
    global MESSAGES

    MESSAGES.append({"name": "Me", "text": inputMessage})
    MESSAGES.append({"name": "SHRDLU", "text": outputMessage})


def getGridSize():
    return GRID_SIZE


def getGrid():
    return GRID


def getMessages():
    return MESSAGES


def getHistory():
    return HISTORY


'''
Use set methods: 
setGrid, setMessages, setHistory 

With data source (query method based on instance that should be passed into the route)
And initalize the globals to what they should be inside the route
'''


def setGridSize(data):
    global GRID_SIZE
    GRID_SIZE = int(data)


def setGrid(data):
    global GRID
    GRID = list(list(sub) for sub in data)


def setMessages(data):
    global MESSAGES
    MESSAGES = list(dict(sub) for sub in data)


def setHistory(data):
    global HISTORY
    res = list(list(sub) for sub in data)
    HISTORY = res


def getInstances():
    return INSTANCES

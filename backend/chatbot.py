import spacy
from environment import SHAPES, COLORS, addShape, delShape, findShape, moveShape, holdShape, GRID_SIZE, GRID, showGrid, getEnvironment, updateHistory

# Create function for conjunctions(and) to make sentences easier to read

nlp = spacy.load('en_core_web_sm')

ACTIONS = {
    'FIND': findShape,
    'DELETE': delShape,
    'ADD': addShape,
    'MOVE': moveShape,
    'HOLD': holdShape}

# @Param sentence- string
# Sentence - Takes the format "[action] [adj] [noun] [x] [y]"
# Extracts the semantics of the sentences and then returns it
# Specifically looks for shape,color,action,row,col


def readSentence(sentence):

    sentence = sentence.lower()

    processed_sentence = nlp(sentence)

    color, shape, action = '', '', ''
    row, col = -1, -1,
    for token in processed_sentence:
        if token.pos_ == 'VERB':
            action = token.text.upper()
        if token.pos_ == 'ADJ':
            color = token.text.upper()
        if token.pos_ == 'NOUN':
            shape = token.text.upper()
        if token.pos_ == 'NUM':
            if row == -1:
                row = int(token.text)
            else:
                col = int(token.text)
        # For relative
        if token.pos_ == 'SCONJ':
            conj = token.text.upper()

        #print(token, token.tag_, token.pos_, spacy.explain(token.tag_), token.head.text, token.dep_)
        # example output "Add VB VERB verb, base form Add ROOT"

    return(shape, color, action, row, col)


def checkShape(noun):
    return noun in SHAPES


def checkColor(adj):
    return adj in COLORS


def checkAction(action):
    return action in ACTIONS


def checkLocation(row, col):
    return not (row > GRID_SIZE - 1 or col > GRID_SIZE - 1
                or row < 0 or col < 0)


def emptyPosition(row, col):
    return getEnvironment()[row][col] == ("", "", 0)


# Next to, Above, Below, Left, Right, Near
def doRelativeAction():
    pass

# @Param flags- the check from @func checkSemantics
# Returns the reponse_number based on what conditions are met
# TODO: Would be good to make the code more readable.


def doAction(action, shape, color, row, col):

    if not checkShape(shape) == 1:  # Check if shape is valid
        return 2
    elif not checkAction(action) == 1:  # Check if action is valid
        return 3

    if action == 'ADD':
        if not checkColor(color):
            return 4

        elif not checkLocation(row, col):
            return 10
        elif emptyPosition(row, col):
            addShape(shape=shape, color=color, row=row, col=col)
            return 0
        else:
            return 1  # Say location is taken

    foundShape = []
    if row != -1 and col != -1 and action != 'MOVE':
        if emptyPosition(row=row, col=col):
            return 6
        else:
            if color in COLORS:
                if getEnvironment()[row][col] == (shape, color, 0):
                    foundShape.append((row, col))
                else:
                    return 6
            else:
                return 4
    else:
        foundShape = findShape(shape=shape, color=color)

    if len(foundShape) == 0:
        return 6

    if len(foundShape) > 1:
        if color in COLORS:
            return 5  # Change to ask for location
        else:
            return 4
    else:
        if action == 'MOVE':
            if not checkLocation(row, col) == 1:
                return 7
            else:
                moveShape(
                    x1=foundShape[0][0],
                    y1=foundShape[0][1],
                    x2=row,
                    y2=col)

        row = foundShape[0][0]
        col = foundShape[0][1]

        if action == 'FIND':
            return 8
        if action == 'DELETE':
            delShape(row, col)
        if action == 'HOLD':
            holdShape(foundShape[0][0], foundShape[0][1])

    return 0


def response(response_number):
    responses = {
        0: "Done",
        1: "Sorry, I can't",
        2: "What kind of shape is that?",
        3: "I do not know how to do that. Please try a different action.",
        4: "What color?",
        5: "There are duplicates of that.",  # Change to specify location
        6: "Not found",
        7: "Location please.",
        8: "Found",
        9: "Deleted",
        10: "Location does not exist."
    }

    return responses[response_number]

# Takes string parameter and outputs response based on the string


def chatbot(sentence):
    shape, color, action, row, col = readSentence(sentence)

    response_number = doAction(
        action=action,
        shape=shape,
        color=color,
        row=row,
        col=col)

    # Update board when grid is changed
    currentEnv = getEnvironment()
    updateHistory(currentEnv, sentence, response(
        response_number), (shape, color, action, row, col))

    return(response(response_number))

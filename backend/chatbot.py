import spacy
from environment import shapes, colors, addShape,delShape,findShape,moveShape,holdShape, GridSize, Grid,showGrid

#Create function for conjunctions(and) to make sentences easier to read


nlp = spacy.load('en_core_web_sm')

actions = {'find':findShape,'delete':delShape,'add':addShape,'move':moveShape,'pick':holdShape}

#Takes the format "[action] [adj] [noun] [x] [y]"
def readSentence(sentence):

    x = nlp(sentence)

    color,shape,action = '','',''
    row,col = -1,-1,
    for token in x:
        if token.pos_ == 'VERB':
            action = token.text.lower()
        if token.pos_ == 'ADJ':
            color = token.text.lower()
        if token.pos_ == 'NOUN':
            shape = token.text.lower()
        if token.pos_ == 'NUM':
            if row == -1:
                row = int(token.text)
            else:
                col = int(token.text)

        #print(token, token.tag_, token.pos_, spacy.explain(token.tag_), token.head.text, token.dep_)
        #example output "Add VB VERB verb, base form Add ROOT"

    return(shape,color,action,row,col)


#Checks to see if the semantics are in our lists:
#check[noun,adjective,verb,location]
#0 -> no error, 1 -> error
def checkSemantics(noun,adj,verb,row,col):
    check = [0,0,0,0]
    if noun not in shapes:
        check[0] = 1
    if adj not in colors:
        check[1] = 1
    if verb not in actions:
        check[2] = 1
    if row > GridSize or col > GridSize \
        or row < 0 or col < 0:
        check[3] = 1

    return check


#Returns the reponse_number based on what conditions are met
def doAction(action,shape,color,row,col,flags):

    if action == 'add':
        if flags[1] == 1:
            return 4
        elif flags[3] == 1:
            return 10
        elif Grid[row][col] == (0,0,0):
            addShape(shape=shape,color = color,row = row,col=col)
            return 0
        else:
            return 1 #Say location is taken

    foundShape = findShape(shape=shape,color=color)
    if len(foundShape) > 1:
        if color in colors:
            return 5  # Change to ask for location
        else:
            return 4
    elif len(foundShape) == 0:
        return 6
    else:
        if action == 'move':
            if flags[3] == 1:
                return 7
            else:
                moveShape(x1= foundShape[0][0],y1=foundShape[0][1],x2=row,y2=col)
        if action == 'find':
            return 8
        if action == 'delete':
            if row != -1 and col != -1: #Case: Coordinates are given
                if Grid[row][col] == (shapes[shape],colors[color],0):
                    delShape(row,col)
                else:
                    return 6
            else:
                delShape(foundShape[0][0],foundShape[0][1])
        if action == 'pick':
            holdShape(foundShape[0][0], foundShape[0][1])

    return 0

def response(response_number):
    responses = {
        0 : "Done",
        1 : "Sorry, I can't",
        2 : "What kind of shape is that?",
        3 : "I do not know how to do that. Please try a different action.",
        4 : "What color?",
        5 : "There are duplicates of that.", #Change to specify location
        6 : "Not found",
        7 : "Location please.",
        8 : "Found",
        9 : "Deleted",
        10 : "Location does not exist."
    }

    return responses[response_number]

def chatbot(sentence):
    shape, color, action, row, col = readSentence(sentence)
    flags = checkSemantics(shape,color,action,row,col)

    response_number = -1

    showGrid()

    if flags[0] == 1: # Check if shape is valid
        response_number = 2
    elif flags[2] == 1: #Check if action is valid
        response_number = 3
    else:
        response_number = doAction(action=action,shape=shape,color=color,row=row,col=col,flags=flags)

    print('-----------------------------------')
    showGrid()
    print(response(response_number))
    print('-----------------------------------')


    return(response(response_number))


def test():
    test3 = "Add the red cube 2 2"
    test4 = "Add the green cube 2 3"
    test5 = "Delete the cube"

    chatbot(test3)
    #chatbot(test4)
    chatbot(test5)

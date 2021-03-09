import chatbot
import environment
from chatbot import emptyPosition,chatbot,doAction
from environment import  GRID, clearBoard


#Check responses
"""
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
"""
def chatbot_test():

    results = []

    ###Add
    test1a = "Add the red cube 2 2"
    test1b = "Add the pyramid"
    test1c = "Add the green"
    test1d = "Add the green pyramid"
    test1e = "Add the green pyramid 2 2"
    chatbot(test1a)
    res1b,res1c,res1d,res1e=doAction(action="ADD", shape="PYRAMID", color="", row=-1, col=-1),\
                            doAction(action="ADD", shape="", color="GREEN", row=-1, col=-1), \
                            doAction(action="ADD", shape="PYRAMID", color="GREEN", row=-1, col=-1),\
                            doAction(action="ADD", shape="PYRAMID", color="GREEN", row=2, col=2)

    #res1b = no color, res1c= no shape, res1d = no coordinates res1e = space is already taken
    results.append((GRID[2][2]) == ('CUBE', 'RED', 0) and res1b == 4 and res1c == 2 and res1d == 10 and res1e == 1)


    ###Delete
    #Delete a shape with coordinates
    chatbot(test1a)
    test2a = "Delete the red cube 2 2"
    chatbot(test2a)
    res2a = emptyPosition(row=2,col=2)
    #Delete a shape without coordinates but there is only one copy of that shape
    chatbot(test1a)
    test2b = "Delete the red cube"
    chatbot(test2b)
    res2b = emptyPosition(row=2,col=2)
    #Delete a shape without coordinates but there are multiple of that shape
    chatbot(test1a)
    chatbot("Add the red cube 2 3")
    res2c = doAction(action="DELETE",shape="CUBE",color="RED",row=-1,col=-1)
    #Shape not found
    res2d = doAction(action="DELETE", shape="BOX", color="BLUE", row=-1, col=-1)

    results.append(res2a == 0 and res2b == 0 and res2c == 5 and res2d == 6)


    ###Clear Board
    test3a = "Add the red cube 2 2"
    test3b = "Add the green pyramid 1 1"
    test3c = "Add the blue box 0 1"
    chatbot(test3a)
    chatbot(test3b)
    chatbot(test3c)
    clearBoard()
    results.append(emptyPosition(row=2,col=2) and emptyPosition(row=1,col=1) and emptyPosition(row=0,col=1))


    ###Move
    #Move a shape with coordinates
    test4a = "Add the green pyramid 2 3"
    test4b = "Move the green pyramid to 1 1"
    chatbot(test4a)
    chatbot(test4b)
    #Move a shape without coordinates
    test4c = "Move the green pyramid"
    res4c = doAction(action="MOVE",shape="PYRAMID",color="GREEN",row=-1,col=-1)
    results.append(emptyPosition(row=2, col=3) and GRID[1][1] == ('PYRAMID', 'GREEN', 0) and res4c == 7)
    clearBoard()


    ###Find
    #Find a shape with coordinates
    chatbot(test1a)
    test5a = "Find the red cube 2 2"
    res5a = doAction(action="FIND", shape="CUBE", color="RED",row=2,col=2)
    #Find a shape without coordinates(only 1 of the shape)
    test5b = "Find the red cube"
    res5b = doAction(action="FIND", shape="CUBE", color="RED",row=-1,col=-1)
    #Find a shape without coordinates(multiple of that shape)
    test5c = "Add a red cube 3 3"
    chatbot(test5c)
    res5c = doAction(action="FIND", shape="CUBE", color="RED",row=-1,col=-1)

    results.append(res5a == 8 and res5b == 8 and res5c == 5)
    clearBoard()


    ###Hold
    test6a = "Add the blue box 1 3"
    test6b = "Hold the blue box"
    chatbot(test6a)
    chatbot(test6b)
    results.append(environment.CLAW_POS == (1,3))
    clearBoard()

    print(results)
    return results


#Find add move hold show
def environment_test():

    results = []
    #Add
    test1 = "Add the red cube 2 2"
    environment.addShape(shape="CUBE", color= "RED",row=2,col=2)
    results.append((GRID[2][2]) == ('CUBE', 'RED', 0))
    #Delete
    test2 = "Delete the red cube 2 2"
    environment.delShape(row = 2, col = 2)
    results.append(emptyPosition(row=2,col=2))
    #Clear Board
    test3a = "Add the red cube 2 2"
    test3b = "Add the green pyramid 1 1"
    test3c = "Add the blue box 0 1"
    environment.addShape(shape="CUBE", color="RED", row=2, col=2)
    environment.addShape(shape="PYRAMID", color="GREEN", row=1, col=1)
    environment.addShape(shape="BOX", color="BLUE", row=0, col=1)
    clearBoard()
    results.append(emptyPosition(row=2,col=2) and emptyPosition(row=1,col=1) and emptyPosition(row=0,col=1))
    #Move
    test4a = "Add the green pyramid 2 3"
    test4b = "Move the green pyramid to 1 1"
    environment.addShape(shape="PYRAMID",color="GREEN",row=2,col=3)
    environment.moveShape(x1=2,y1=3,x2=1,y2=1)
    results.append(emptyPosition(row=2,col=3) and GRID[1][1] == ('PYRAMID','GREEN',0))
    clearBoard()
    #Find
    test5a = "Add the red cube 1 2"
    environment.addShape(shape="CUBE",color="RED",row=1,col=2)
    results.append(environment.findShape(shape = "CUBE",color = "RED")[0] == (1,2))
    clearBoard()
    #Hold
    test6a = "Add the blue box 1 3"
    test6b = "Hold the blue box"
    environment.addShape(shape="BOX", color="BLUE", row=1, col=3)
    environment.holdShape(row=1,col=3)
    results.append(environment.CLAW_POS == (1,3))
    clearBoard()

    print(results)
    return results

#Delete with a capital D is recognized as a noun and will not work
#delete only works with lowercase d
def AddandDelete():
    print(chatbot("Add the red cube"))
    print(chatbot("Add the red cube 2 2"))
    print(chatbot("Find the red cube"))
    print(chatbot("Add the red cube 1 2"))
    print(chatbot("Find the red cube"))
    print(chatbot("Find the red cube 2 2"))
    print(chatbot("delete the red cube"))
    print(chatbot("delete the red cube 1 2"))
    print(chatbot("Find the red cube"))

    clearBoard()



#All variables should return true in the lists
#environment_test()
#chatbot_test()

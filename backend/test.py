import chatbot
import environment

def chatbot_test():
    test3 = "Add the red cube 2 2"
    test4 = "Add the green cube 2 3"
    test5 = "Delete the cube"

    chatbot(test3)
    # chatbot(test4)
    chatbot(test5)

def environment_test():
    x = 1
    y = 2
    shape = 'cube'
    color = 'red'

    environment.addShape(x, y, shape, color)

    environment.showGrid()

    print(environment.findShape(shape))




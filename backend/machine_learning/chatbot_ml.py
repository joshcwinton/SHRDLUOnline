from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from transformers import BertTokenizer, TFBertForTokenClassification
import tensorflow as tf
import numpy as np

from environment import (
    SHAPES,
    COLORS,
    addShape,
    delShape,
    findShape,
    moveShape,
    getGridSize,
    getGrid,
    getPosition,
    updateHistory,
    updateMessage,
)
import random
from datetime import datetime

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
INPUT_SIZE = 20

# Target Fields - used to convert nn output to target output
COLORS_LIST = {0: "none", 1: "red", 2: "blue", 3: "green"}
ACTIONS_LIST = {0: "none", 1: "add", 2: "find", 3: "delete", 4: "move"}
REL_ACTIONS_LIST = {0: "none", 1: "above",
                    2: "below", 3: "near", 4: "right", 5: "left"}
NOUN_LIST = {0: "none", 1: "cube", 2: "pyramid", 3: "sphere"}


#Used to create neural network architecture and load weights from "Weights.h5"
#Returns the created model
#Not used because we are loading from model file
def createModel():
    # Load pretrained model
    model = TFBertForTokenClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=INPUT_SIZE,
        output_attentions=False,
        output_hidden_states=False,
    )

    # Create architecture and load weights
    nn_input = Input(shape=(INPUT_SIZE,), dtype="int64")
    x = model(nn_input)
    x = x[0]
    x = tf.keras.layers.Flatten()(x)
    x = Dense(128, activation="relu")(x)
    x = Dense(64, activation="sigmoid")(x)
    x = Dense(16, activation="sigmoid")(x)

    action_pred = Dense(len(ACTIONS_LIST), name="Action",
                        activation="softmax")(x)
    shape_pred = Dense(len(NOUN_LIST), name="Noun", activation="softmax")(x)
    color_pred = Dense(len(COLORS_LIST), name="Color", activation="softmax")(x)
    rel_action_pred = Dense(
        len(REL_ACTIONS_LIST), name="Rel_Action", activation="softmax"
    )(x)
    rel_shape_pred = Dense(
        len(NOUN_LIST), name="Rel_Noun", activation="softmax")(x)
    rel_color_pred = Dense(
        len(COLORS_LIST), name="Rel_Color", activation="softmax")(x)

    full_model = Model(
        inputs=nn_input,
        outputs=[
            action_pred,
            shape_pred,
            color_pred,
            rel_action_pred,
            rel_shape_pred,
            rel_color_pred,
        ],
    )

    full_model.summary()

    full_model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0
        ),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy("accuracy")],
    )

    full_model.load_weights("Weights.h5")

    return full_model


def checkShape(noun):
    return noun in SHAPES


def checkColor(adj):
    return adj in COLORS


# Return if location is valid on the grid
# If valid returns true


def checkLocation(row, col):
    return not (
        row > getGridSize() - 1 or col > getGridSize() - 1 or row < 0 or col < 0
    )


def emptyPosition(row, col):
    return getGrid()[row][col] == ("", "", 0)


# Grabs coordinates based on the relative action and relative shape
# Returns the coordinates
# Only used for Above, Below, Right, Left
# ie relative action == left -> return coordinates left of relative shape


def doRelativeAction(rel_action, rel_shape, rel_color):
    # Above, Below, Right, Left
    x, y = findShape(shape=rel_shape, color=rel_color)[0]

    if rel_action == "ABOVE":
        y = y - 1

    if rel_action == "BELOW":
        y = y + 1

    if rel_action == "RIGHT":
        x = x + 1

    if rel_action == "LEFT":
        x = x - 1

    return x, y


def nearAction(shape, color, action, rel_action, rel_shape, rel_color):
    random.seed(datetime.now())
    positions = []

    x, y = findShape(shape=rel_shape, color=rel_color)[0]

    x = x - 1
    y = y - 1
    # Store every possible coordinate within 1 square radius into positions
    for i in range(3):
        for j in range(3):
            temp_x = x + i
            temp_y = y + j
            if (
                temp_x > -1
                and temp_y > -1
                and temp_x < getGridSize()
                and temp_y < getGridSize()
            ):
                positions.append((temp_x, temp_y))

    pos = random.randint(0, len(positions) - 1)
    x, y = positions.pop(pos)

    # Chooses one randomly depending on the aciton
    if action == "ADD":  # Find empty space near relative object
        while not emptyPosition(x, y) and len(positions) != 0:
            pos = random.randint(0, len(positions) - 1)
            x, y = positions.pop(pos)

    if action == "DELETE":  # Find matching block near relative object
        while getPosition(x, y) != [shape, color, 0] and len(positions) != 0:
            pos = random.randint(0, len(positions) - 1)
            x, y = positions.pop(pos)

    if action == "MOVE":  # Find empty space near relative object
        while not emptyPosition(x, y) and len(positions) != 0:
            pos = random.randint(0, len(positions) - 1)
            x, y = positions.pop(pos)

    if (
        action == "FIND"
    ):  # Find matching blocks near relative object -> Only returns one right now
        while getPosition(x, y) != [shape, color, 0] and len(positions) != 0:
            pos = random.randint(0, len(positions) - 1)
            x, y = positions.pop(pos)

    return x, y


def addAction(shape, color, x, y):
    if not checkColor(color):
        return 4
    if not checkShape(shape):
        return 2

    if emptyPosition(x, y):
        addShape(row=x, col=y, shape=shape, color=color)
        return 0
    else:
        return 1


def deleteAction(shape, color, x, y):
    if not checkColor(color):
        return 4
    if not checkShape(shape):
        return 2

    if emptyPosition(x, y):
        return 6
    else:
        if getPosition(x, y) == (shape, color, 0):  # Action can be done
            delShape(row=x, col=y)
            return 0
        else:  # shape and/or color does not match
            return 1  # Change to say incorrect color and/or shape


def moveAction(shape, color, x, y):
    if not checkColor(color):
        return 4
    if not checkShape(shape):
        return 2

    foundShapes = findShape(shape=shape, color=color)
    if len(foundShapes) == 0:  # Case: No shape
        return 6

    if len(foundShapes) > 1:  # Case: More than one shape
        return 5

    old_x, old_y = foundShapes[0]
    if old_x == x and old_y == y:  # Shape is already in the right spot
        return 0
    else:
        if not emptyPosition(x, y):  # Spot is not empty:
            return 1
        else:  # We good
            moveShape(x1=old_x, y1=old_y, x2=x, y2=y)
        return 0


def findAction(shape, color=None, x=-1, y=-1):
    if color:
        if not checkColor(color):
            return 4
    if not checkShape(shape):
        return 2

    if x == -1 and y == -1:  # Coordinates are not given
        foundShapes = findShape(shape, color)
        if len(foundShapes) == 0:  # Case: No shape
            return 6

        if len(foundShapes) > 1:  # Case: More than one shape
            return 5

        if len(foundShapes) == 1:
            return 8
    else:  # Coordinates are given
        if getPosition(x, y) == (shape, color, 0):
            return 8
        else:
            return 6


# @Param flags- the check from @func checkSemantics
# Returns the reponse_number based on what conditions are met


def doAction(action, shape, color, rel_action=None, rel_shape=None, rel_color=None):

    action = action.upper()
    shape = shape.upper()
    color = color.upper()
    rel_action = rel_action.upper()
    rel_shape = rel_shape.upper()
    rel_color = rel_color.upper()

    # No relative stuff given
    if not rel_action or not rel_shape or not rel_color:
        if action == "ADD":
            return 7  # Location please
        if action == "DELETE":
            foundShape = findShape(shape=shape, color=color)
            if len(foundShape) != 0:
                for found in foundShape:
                    deleteAction(shape=shape, color=color,
                                 x=found[0], y=found[1])
                    return 0
            else:
                return 6
        if action == "MOVE":
            return 7  # Location please
        if action == "FIND":
            return findAction(shape=shape, color=color)

    # Relative stuff given
    foundShape = findShape(shape=rel_shape, color=rel_color)

    if len(foundShape) == 0:  # Case: No relative shape
        return 6

    if len(foundShape) > 1:  # Case: More than one relative shape
        # Add response to clarify which relative shape
        return 5

    # Case: relative shape found
    # doRelativeAction returns the coordinates for the relative action
    x, y = doRelativeAction(
        rel_action=rel_action, rel_shape=rel_shape, rel_color=rel_color
    )
    if rel_action == "NEAR":
        x, y = nearAction(
            shape=shape,
            color=color,
            action=action,
            rel_action=rel_action,
            rel_shape=rel_shape,
            rel_color=rel_color,
        )

    # Case:relative action is out of bounds
    if not checkLocation(x, y):
        return 10

    # Case x,y is valid -> Action is completed
    if action == "ADD":
        return addAction(shape=shape, color=color, x=x, y=y)

    if action == "DELETE":
        return deleteAction(shape=shape, color=color, x=x, y=y)

    if action == "MOVE":
        return moveAction(shape=shape, color=color, x=x, y=y)

    if action == "FIND":
        return findAction(shape=shape, color=color, x=x, y=y)

    return 0


def response(response_number, action, shape, color):
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
        10: "Location does not exist.",
    }

    return responses[response_number]


def chatbot_ml(res, sentence):
    # model = createModel() #Model is moved to app.py so the models won't be instanced

    action = ACTIONS_LIST[np.argmax(res[0])]
    noun = NOUN_LIST[np.argmax(res[1])]
    color = COLORS_LIST[np.argmax(res[2])]
    rel_action = REL_ACTIONS_LIST[np.argmax(res[3])]
    rel_noun = NOUN_LIST[np.argmax(res[4])]
    rel_color = COLORS_LIST[np.argmax(res[5])]

    response_num = doAction(
        action=action,
        shape=noun,
        color=color,
        rel_action=rel_action,
        rel_shape=rel_noun,
        rel_color=rel_color,
    )

    resp = response(response_num, action=action, shape=noun, color=color)
    if response_num == 0 or response_num == 8 or response_num == 9:
        updateHistory(getGrid(), sentence, resp, (noun, color, action))
    else:
        updateMessage(sentence, resp)
    return resp

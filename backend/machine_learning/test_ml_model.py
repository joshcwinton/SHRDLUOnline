from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from transformers import BertTokenizer, TFBertForTokenClassification
import tensorflow as tf
import numpy as np

# Create architecture and load weights

# Load pretrained model
INPUT_SIZE = 20

# Target Fields
COLORS_LIST = {0: 'none', 1: 'red', 2: 'blue', 3: 'green'}
ACTIONS_LIST = {0: 'none', 1: 'add', 2: 'find', 3: 'delete', 4: 'move'}
REL_ACTIONS_LIST = {0: 'none', 1: 'above',
                    2: 'below', 3: 'near', 4: 'right', 5: 'left'}
NOUN_LIST = {0: 'none', 1: 'cube', 2: 'pyramid', 3: 'sphere'}

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Used to create neural network architecture and load weights from "Weights.h5"
# Returns the created model
# Not used because we are loading from model file


def createModel():
    model = TFBertForTokenClassification.from_pretrained("bert-base-uncased",
                                                         num_labels=INPUT_SIZE,
                                                         output_attentions=False,
                                                         output_hidden_states=False)
    # Create architecture and load weights
    nn_input = Input(shape=(INPUT_SIZE,), dtype='int64')
    x = model(nn_input)
    x = x[0]
    x = tf.keras.layers.Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(64, activation='sigmoid')(x)
    x = Dense(16, activation='sigmoid')(x)

    action_pred = Dense(len(ACTIONS_LIST), name="Action",
                        activation='softmax')(x)
    shape_pred = Dense(len(NOUN_LIST), name="Noun", activation='softmax')(x)
    color_pred = Dense(len(COLORS_LIST), name="Color", activation='softmax')(x)
    rel_action_pred = Dense(len(REL_ACTIONS_LIST),
                            name="Rel_Action", activation='softmax')(x)
    rel_shape_pred = Dense(
        len(NOUN_LIST), name="Rel_Noun", activation='softmax')(x)
    rel_color_pred = Dense(
        len(COLORS_LIST), name="Rel_Color", activation='softmax')(x)

    full_model = Model(inputs=nn_input,
                       outputs=[action_pred, shape_pred, color_pred, rel_action_pred, rel_shape_pred, rel_color_pred])

    full_model.summary()

    full_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0),
                       loss=tf.keras.losses.SparseCategoricalCrossentropy(
                           from_logits=True),
                       metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])

    full_model.load_weights("Weights.h5")


full_model = tf.keras.models.load_model("Model.h5")
# Test model

# Model will predict on each sentence in pred_sentences
pred_sentences = ["Can you add the red cube next to the green sphere",
                  "Delete the green circle to the left of the red pyramid",
                  "Add the green pyramid to the right of the blue circle",
                  "Move the blue pyramid on top the green pyramid",
                  "Find the orange cube by the green cube",
                  "Hold the red pyramid below the blue sphere",
                  "Add the red cube",
                  "Where is the green circle",
                  "Is there a blue sphere"]

for sentence in pred_sentences:
    tokenize_sentence = tokenizer.encode(
        sentence, padding='max_length', max_length=INPUT_SIZE)
    res = full_model.predict([tokenize_sentence])
    print("Sentence: ", sentence)
    print("Tokenized Sentence: ", tokenize_sentence)
    print("Action: ", ACTIONS_LIST[np.argmax(
        res[0])], np.argmax(res[0]), res[0])
    print("Noun: ", NOUN_LIST[np.argmax(res[1])], np.argmax(res[1]), res[1])
    print("Color: ", COLORS_LIST[np.argmax(res[2])], np.argmax(res[2]), res[2])
    print("Rel_Action: ", REL_ACTIONS_LIST[np.argmax(
        res[3])], np.argmax(res[3]), res[3])
    print("Rel_Noun: ", NOUN_LIST[np.argmax(
        res[4])], np.argmax(res[4]), res[4])
    print("Rel_Color: ", COLORS_LIST[np.argmax(
        res[5])], np.argmax(res[5]), res[5])

    print("-------------------------")

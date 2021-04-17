from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from transformers import BertTokenizer, TFBertForTokenClassification
import tensorflow as tf
import numpy as np
from .create_model import INPUT_SIZE

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Target Fields
COLORS_LIST = {0: 'none', 1: 'red', 2: 'blue', 3: 'green'}
ACTIONS_LIST = {0: 'none', 1: 'add', 2: 'find', 3: 'delete', 4: 'move'}
REL_ACTIONS_LIST = {0: 'none', 1: 'above', 2: 'below', 3: 'near', 4: 'right', 5: 'left'}
NOUN_LIST = {0: 'none', 1: 'cube', 2: 'pyramid', 3: 'sphere'}


# Create neural network architecture and load weights
def createModel():
    # Load pretrained model
    model = TFBertForTokenClassification.from_pretrained("bert-base-uncased")

    #Create architecture and load weights
    nn_input =  Input(shape=(15,), dtype= 'int64')
    x = model(nn_input)
    x = x[0]
    x = Dense(64,activation='relu')(x)
    x = Dense(16,activation='sigmoid')(x)

    action_pred = Dense(len(ACTIONS_LIST), name="Action", activation='softmax')(x)
    shape_pred = Dense(len(NOUN_LIST), name="Noun", activation='softmax')(x)
    color_pred = Dense(len(COLORS_LIST), name="Color", activation='softmax')(x)
    rel_action_pred = Dense(len(REL_ACTIONS_LIST), name="Rel_Action", activation='softmax')(x)
    rel_shape_pred = Dense(len(NOUN_LIST), name="Rel_Noun", activation='softmax')(x)
    rel_color_pred = Dense(len(COLORS_LIST), name="Rel_Color", activation='softmax')(x)

    full_model = Model(inputs=nn_input,
                       outputs = [action_pred,shape_pred,color_pred,rel_action_pred,rel_shape_pred,rel_color_pred])

    full_model.summary()

    full_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])

    full_model.load_weights("Weights.h5")

    return full_model

def chatbot(sentence):
    model = createModel()

    sentence = sentence.lower()
    tokenize_sentence = tokenizer.encode(sentence, padding='max_length', max_length=INPUT_SIZE)
    res = model.predict([tokenize_sentence])

    action = ACTIONS_LIST[np.argmax(res[0])]
    noun = NOUN_LIST[np.argmax(res[1])]
    color = COLORS_LIST[np.argmax(res[2])]
    rel_action = REL_ACTIONS_LIST[np.argmax(res[3])]
    rel_noun = NOUN_LIST[np.argmax(res[4])]
    rel_color = COLORS_LIST[np.argmax(res[5])]

    #doAction()



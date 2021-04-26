import numpy as np
import tensorflow as tf
import pandas as pd

# https://towardsdatascience.com/sentiment-analysis-in-10-minutes-with-bert-and-hugging-face-294e8a04b671

from transformers import BertTokenizer, TFBertForTokenClassification
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input

# Load pretrained model
INPUT_SIZE = 20

model = TFBertForTokenClassification.from_pretrained("bert-base-uncased",
                                                     num_labels=INPUT_SIZE,
                                                     output_attentions=False,
                                                     output_hidden_states=False)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model.summary()

DATA_FILE = 'data/training_data.csv'

# Read Data
raw_data = open(DATA_FILE, 'rt')
data = pd.read_csv(raw_data)
data = data.replace(np.nan, "")
print(data.shape)

# Convert data to numpy and shuffle data
np_data = data.to_numpy()
np.random.shuffle(np_data)

# Split and shuffle data in training and validation data
TRAIN_SIZE = .8
VAL_SIZE = .2

SPLIT_SIZE = round(len(np_data)*TRAIN_SIZE)
train_data = np_data[:SPLIT_SIZE]
val_data = np_data[:len(np_data)-SPLIT_SIZE]

train_data = np.asarray(train_data)
val_data = np.asarray(val_data)

print(train_data.shape)
print(val_data.shape)

# Split training data into separate categories
sentences = []
for sentence in train_data[:, 0]:
    sentences.append(tokenizer.encode(
        sentence, padding='max_length', max_length=INPUT_SIZE))

sentences = np.asarray(sentences)

actions = train_data[:, 1].astype(int)
shapes = train_data[:, 2].astype(int)
colors = train_data[:, 3].astype(int)
rel_actions = train_data[:, 4].astype(int)
rel_shapes = train_data[:, 5].astype(int)
rel_colors = train_data[:, 6].astype(int)

# Create model and train

nn_input = Input(shape=(INPUT_SIZE,), dtype='int64')
x = model(nn_input)
x = x[0]
x = tf.keras.layers.Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dense(64, activation='sigmoid')(x)
x = Dense(16, activation='sigmoid')(x)

# Target Fields
COLORS_LIST = {0: 'none', 1: 'red', 2: 'blue', 3: 'green'}
ACTIONS_LIST = {0: 'none', 1: 'add', 2: 'find', 3: 'delete', 4: 'move'}
REL_ACTIONS_LIST = {0: 'none', 1: 'above',
                    2: 'below', 3: 'near', 4: 'right', 5: 'left'}
NOUN_LIST = {0: 'none', 1: 'cube', 2: 'pyramid', 3: 'sphere'}

action_pred = Dense(len(ACTIONS_LIST), name="Action", activation='softmax')(x)
shape_pred = Dense(len(NOUN_LIST), name="Noun", activation='softmax')(x)
color_pred = Dense(len(COLORS_LIST), name="Color", activation='softmax')(x)
rel_action_pred = Dense(len(REL_ACTIONS_LIST),
                        name="Rel_Action", activation='softmax')(x)
rel_shape_pred = Dense(len(NOUN_LIST), name="Rel_Noun",
                       activation='softmax')(x)
rel_color_pred = Dense(len(COLORS_LIST), name="Rel_Color",
                       activation='softmax')(x)

full_model = Model(inputs=nn_input,
                   outputs=[action_pred, shape_pred, color_pred, rel_action_pred, rel_shape_pred, rel_color_pred])

full_model.summary()

full_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0),
                   loss=tf.keras.losses.SparseCategoricalCrossentropy(
                       from_logits=True),
                   metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])

full_model.fit(sentences,
               {"Action": actions, "Noun": shapes, "Color": colors,
                   "Rel_Action": rel_actions, "Rel_Noun": rel_shapes, "Rel_Color": rel_colors},
               epochs=20, batch_size=64)

full_model.save_weights("Weights.h5")


# Evaluate model

val_sentences = []
val_actions = []
val_shapes = []
val_colors = []
val_rel_actions = []
val_rel_shapes = []
val_rel_colors = []

for x in val_data:
    val_sentences.append(np.asarray(x[0]))
    val_actions.append(np.asarray(x[1]))
    val_shapes.append(np.asarray(x[2]))
    val_colors.append(np.asarray(x[3]))
    val_rel_actions.append(np.asarray(x[4]))
    val_rel_shapes.append(np.asarray(x[5]))
    val_rel_colors.append(np.asarray(x[6]))

val_sentences = np.asarray(sentences)
val_actions = np.asarray(actions)
val_shapes = np.asarray(shapes)
val_colors = np.asarray(colors)
val_rel_actions = np.asarray(rel_actions)
val_rel_shapes = np.asarray(rel_shapes)
val_rel_colors = np.asarray(rel_colors)

print(full_model.evaluate(val_sentences,
                          {"Noun": val_shapes, "Action": val_actions, "Color": val_colors, "Rel_Noun": val_rel_shapes,
                           "Rel_Action": val_rel_actions, "Rel_Color": val_rel_colors})
      )

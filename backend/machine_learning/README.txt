Chatbot_ML:
Contains the logic of the chatbot

Create_Model:
Creates the neural network architecture and trains the data based on the training_data.csv in data/
The weights are saved as Weights.h5 and then can be used in test_ml_model and app.py.
The current model takes a sentence of input 20 and outputs action,noun,color,rel_action,rel_noun,rel_color

Test_ML_Model:
Loads weights from Weights.h5 and can be used to test specific sentences

Data_Creation:
To create data, input the data into sentences_to_train_on.txt under the fields header:
The input should follow the fields
Sentence,Target_Action,Noun,Color,Relative_Action,Relative_Object,Relative_Object_Color
ie.
Add the red cube below the green sphere,add,cube,red,below,sphere,green

The file will call the create_sentences function which will create unique sentence variations 
for "Add the red cube below the green sphere". This is done by replacing the nouns,colors,actions,
and relative actions

The sentence "Add the red cube below the green sphere" will be seen as 
(target_action) the (color) (noun) (rel_action) the (rel_object_color) (rel_object)
and all the unique combinations of that will be created


"Add the red cube below the green sphere" will have the variations:
->
"Add the red cube below the blue sphere"
"Add the red cube below the red sphere"
"Add the red cube near the green sphere"
...
"Add the blue cube below the green sphere"
...
"Find the red cube below the green sphere"
...
"Delete the red cube below the green sphere"
...
...


The file will then replace synonyms of the nouns and actions in each unique sentence
and add it into the training_data.csv

"Add the red cube below the green sphere" 
->
"Put in the red cube below the green sphere"
"Add the red box below the green sphere"
"Add the red cube behind the green sphere"
...

TLDR:
put input sentence and target fields into sentences_to_train_on.txt
the sentence structure will be used to create unique sentences
	sentence:"Add the red cube below the green sphere" -> 
	sentence structure: (target_action) the (color) (noun) (rel_action) the (rel_object_color) (rel_object)
Unique sentences are unique because they have different target data
words in the unique sentences will be replaced for synonyms to create more sentences
sentences will be added into training_data
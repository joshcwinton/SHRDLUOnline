import csv
import os.path
import json

### Synonym Lists ###

ADD_SYNONYMS = ["add", "put in"]
FIND_SYNONYMS = ["find", "look for"]
DELETE_SYNONYMS = ["delete"]
MOVE_SYNONYMS = ["move"]
HOLD_SYNONYMS = ["hold","pick up","pick","pick-up","grasp"]

#Relative Actions
ABOVE_SYNONYMS = ["above", "on top"]
BELOW_SYNONYMS = ["below", "behind"]
NEAR_SYNONYMS = ["near", "besides", "next", "next to", "around"]
RIGHT_SYNONYMS = ["right"]
LEFT_SYNONYMS = ["left"]

#Shapes
CUBE_SYNONYMS = ["cube", "box", "square"]
PYRAMID_SYNONYMS = ["pyramid", "triangle"]
SPHERE_SYNONYMS = ["sphere", "circle"]

#Dictionaries to map words to synonym lists
ACTIONS = {'ADD': ADD_SYNONYMS, 'FIND': FIND_SYNONYMS,
           'DELETE': DELETE_SYNONYMS, 'MOVE': MOVE_SYNONYMS, 'HOLD': HOLD_SYNONYMS}

RELATIVE_ACTIONS = {'ABOVE': ABOVE_SYNONYMS, 'BELOW': BELOW_SYNONYMS,
                    'NEAR':NEAR_SYNONYMS, 'RIGHT':RIGHT_SYNONYMS, 'LEFT':LEFT_SYNONYMS}

NOUNS = {'CUBE': CUBE_SYNONYMS, 'PYRAMID': PYRAMID_SYNONYMS, 'SPHERE':SPHERE_SYNONYMS}

#List of actions and colors
#Used in create_sentences() to get different variations of a sentence_structure
COLORS_LIST = ['red','blue','green']
ACTIONS_LIST = ['add','find','delete','move','hold']
REL_ACTIONS_LIST = ['above','below','near','right','left']

#Statistics to be updated into the file
total_sentences = 0
total_unique_sentences = 0
STATS_DATA = {'ADD': 0,'FIND': 0,'DELETE': 0,
              'MOVE': 0,'HOLD': 0,'ABOVE': 0,
              'BELOW': 0,'NEAR': 0,'RIGHT': 0,
              'LEFT': 0,}




###                   ###
### Create test cases ###
###                   ###


#Takes each unique_sentence and grabs the synonyms of the nouns and actions
#These sentences are NOT unique because the target data will remain the same
#The created sentences will be added to the list data which is directly appended
#   to training_data.txt
def create_Data(action,noun,color,sentence,relative_action=None,
                relative_object=None, relative_object_color= None):
    global total_sentences, total_unique_sentences, STATS_DATA

    sentence = sentence.lower()
    action = action.lower()
    noun = noun.lower()
    color = color.lower()

    total_unique_sentences += 1

    #Grabs each synonym for nouns, actions and rel_object, relative actions and creates a sentence with it
    #The target data remains the same
    for noun_synonym in NOUNS[noun.upper()]:
        new_sentence = sentence.replace(noun, noun_synonym, 1)
        for action_synonym in ACTIONS[action.upper()]:
            if relative_action:
                relative_action = relative_action.lower()
                relative_object = relative_object.lower()
                relative_object_color = relative_object_color.lower()
                for rel_noun_synonym in NOUNS[relative_object.upper()]:
                    new_sentence1 = new_sentence.replace(relative_object,rel_noun_synonym)
                    for rel_action_synoynm in RELATIVE_ACTIONS[relative_action.upper()]:
                        new_sentence2 = new_sentence1.replace(action, action_synonym)
                        new_sentence2 = new_sentence2.replace(relative_action,rel_action_synoynm)
                        data.append([new_sentence2,action,noun,color,relative_action,
                                     relative_object,relative_object_color])
                        total_sentences += 1
                        STATS_DATA[action.upper()] += 1

            else: #Case no relative actions
                new_sentence1 = new_sentence.replace(action.lower(), action_synonym.lower())
                data.append([new_sentence1, action, noun, color, relative_action,
                             relative_object,relative_object_color])
                total_sentences += 1
                STATS_DATA[action.upper()] += 1

#This creates unique sentences
#unique sentences are unique because they have different target data
def create_Sentences(action,noun,color,sentence,relative_action=None,
                relative_object=None, relative_object_color= None):

    sentence = sentence.lower()
    action = action.lower()
    noun = noun.lower()
    color = color.lower()

    unique_sentences = []

    #Grabs each possible variation of color, action, relative action and relative object
    #These are all unique sentences because the target data will be changed
    for COLOR in COLORS_LIST:
        new_sentence = sentence.replace(color,COLOR,1)
        for ACTION in ACTIONS_LIST:
            new_sentence1 = new_sentence.replace(action,ACTION)

            if relative_action:
                relative_action = relative_action.lower()
                relative_object = relative_object.lower()
                relative_object_color = relative_object_color.lower()
                for REL_ACTION in REL_ACTIONS_LIST:
                    new_sentence2 = new_sentence1.replace(relative_action,REL_ACTION)
                    for REL_COLOR in COLORS_LIST:
                        li = new_sentence2.rsplit(relative_object_color,1)
                        new_sentence3 = REL_COLOR.join(li)

                        unique_sentences.append([new_sentence3,ACTION,noun,COLOR,
                                                REL_ACTION,relative_object,REL_COLOR])

            else: #Case no relative action
                unique_sentences.append([new_sentence1,ACTION,noun,COLOR,
                                                relative_action,relative_object,relative_object_color])

    return unique_sentences

###                            ###
### Create files and Save data ###
###                            ###
UNIQUE_SENTENCES_FILE = 'data/unique_sentences.txt'
TRAINING_SENTENCES_FILE = 'data/sentences_to_train_on.txt' #Incoming sentences to create into data
SENTENCE_STRUCTURES_FILE = 'data/sentence_structures.txt'
DATA_FILE = 'data/training_data.csv'
STATS_FILE = 'data/stats.json'
FIELDS = ['Sentence','Target_Action','Noun','Color',
          'Relative_Action','Relative_Object', 'Relative_Object_Color']

def createFiles():
    files = [UNIQUE_SENTENCES_FILE,TRAINING_SENTENCES_FILE,DATA_FILE]

    for file in files:
        if not os.path.isfile(file):
            with open(file, 'w', newline='') as outfile:
                csv.writer(outfile).writerow(FIELDS)
                outfile.close()

    if not os.path.isfile(SENTENCE_STRUCTURES_FILE):
        with open(SENTENCE_STRUCTURES_FILE, 'w', newline='') as outfile:
            outfile.close()


    if not os.path.isfile(STATS_FILE):
        with open(STATS_FILE, 'w', newline= '') as outfile:
            stats = {'total_sentences' : 0,
                     'total_unique_sentences' : 0,
                     'sentence_samples' : {
                         'ADD': 0,
                         'FIND': 0,
                         'DELETE': 0,
                         'MOVE': 0,
                         'HOLD': 0,
                         'ABOVE': 0,
                         'BELOW': 0,
                         'NEAR': 0,
                         'RIGHT': 0,
                         'LEFT': 0,
                         }
                     }
            json.dump(stats,outfile,indent=4)

#Saves new sentence structures into sentence_structures.txt
#Input: "Add the red cube" -> Sentence Structure: <target_action> the <color> <cube>
#This helps to keep track of what sentence structures have been used so we do not repeat data
#Returns false if the sentence structure is found in sentence_structures.txt
#Returns true if not found and adds to sentence_structure.txt
def save_Sentence_Structure(action,noun,color,sentence,relative_action=None,
                relative_object=None, relative_object_color= None):

    #Get sentence_structure
    new_sentence_structure = sentence.replace(action, "<target_action>")
    new_sentence_structure = new_sentence_structure.replace(noun, "<noun>")
    new_sentence_structure = new_sentence_structure.replace(color, "<color>")
    if relative_action:
        new_sentence_structure = new_sentence_structure.replace(relative_action, "<rel_action>")
        new_sentence_structure = new_sentence_structure.replace(relative_object, "<rel_object>")
        new_sentence_structure = new_sentence_structure.replace(relative_object_color, "<rel_object_color>")

    #Check if structure is already used
    with open(SENTENCE_STRUCTURES_FILE,'r') as sentencefile:
        used_sentence_structures = sentencefile.readlines()
        for used_sentence_strucutre in used_sentence_structures:
            if used_sentence_strucutre.strip() == new_sentence_structure:
                return False

        sentencefile.close()

    #Save structure into file if not used
    with open(SENTENCE_STRUCTURES_FILE, 'a', newline='') as sentencefile:
        sentencefile.write(new_sentence_structure)
        sentencefile.write('\n')
        sentencefile.close()

    return True

def save_Unique_Sentence(data):
    with open(UNIQUE_SENTENCES_FILE, 'a', newline='') as sentencefile:
        csv.writer(sentencefile).writerow(data)
        sentencefile.close()

def save_Data():
    #Saves data into training_data
    with open(DATA_FILE, 'a',newline='') as datafile:
         csvwriter = csv.writer(datafile)

         csvwriter.writerows(data)
         datafile.close()

    #Grab and update the statistics in the file
    with open(STATS_FILE, 'r') as stats_file:
        global  total_sentences,total_unique_sentences,STATS_DATA

        json_data = json.load(stats_file)
        total_sentences += json_data['total_sentences']
        total_unique_sentences += json_data['total_unique_sentences']

        for sample in json_data['sentence_samples']:
            STATS_DATA[sample] += json_data['sentence_samples'][sample]

        stats_file.close()

    with open(STATS_FILE, 'w') as stats_file:
        stats = {'total_sentences': total_sentences,
                 'total_unique_sentences' : total_unique_sentences,
                 'sentence_samples': STATS_DATA}
        json.dump(stats, stats_file, indent=4)

    #Empty training_sentences file
    with open(TRAINING_SENTENCES_FILE, 'w', newline='') as datafile:
        csv.writer(datafile).writerow(FIELDS)
        datafile.close()





if __name__ == '__main__':

    createFiles()
    data = []  # create_Data stores everything in data

    with open(TRAINING_SENTENCES_FILE,'r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter = ',')

        #Target_fields = [Sentence,Target_Action,Noun,Color,
        #           Relative_Action,Relative_Object,Relative_Object_Color]

        target_fields = next(csv_reader)

        for row in csv_reader:

            if row == '\n':
                continue

            sentence = row[0].lower()
            action = row[1].lower()
            noun = row[2].lower()
            color = row[3].lower()
            relative_action = None
            relative_object = None
            relative_object_color = None
            if len(row) > 4:
                relative_action = row[4].lower()
                relative_object = row[5].lower()
                relative_object_color = row[6].lower()

            #Checks if sentence structure is already used.
            if not save_Sentence_Structure(action = action,noun = noun,color = color,sentence = sentence,
                   relative_action= relative_action,relative_object = relative_object,
                   relative_object_color =relative_object_color):
                print("Sentence structure used")
                continue

            unique_sentences = create_Sentences(action = action,noun = noun,color = color,sentence = sentence,
                    relative_action= relative_action,relative_object = relative_object,
                    relative_object_color =relative_object_color)

            for x in unique_sentences:
                sentence = x[0]
                action = x[1]
                noun = x[2]
                color = x[3]
                relative_action = None
                relative_object = None
                relative_object_color = None
                if len(row) > 4:
                    relative_action = x[4]
                    relative_object = x[5]
                    relative_object_color = x[6]

                create_Data(action = action,noun = noun,color = color,sentence = sentence,
                        relative_action= relative_action,relative_object = relative_object,
                        relative_object_color =relative_object_color)

                save_Unique_Sentence(x)

    save_Data()




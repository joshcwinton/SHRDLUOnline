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

#Statistics to be updated into the file
total_sentences = 0
total_unique_sentences = 0
STATS_DATA = {'ADD': 0,'FIND': 0,'DELETE': 0,
              'MOVE': 0,'HOLD': 0,'ABOVE': 0,
              'BELOW': 0,'NEAR': 0,'RIGHT': 0,
              'LEFT': 0,}


### Create test cases ###

#Input is sentence
#Target is comma seperated list with
#Action, Noun, Adjective, Relative Action / Relative Object, Relative Object Color

def create_Data(action,noun,color,sentence,relative_action=None,
                relative_object=None, relative_object_color= None):
    global total_sentences, total_unique_sentences, STATS_DATA

    sentence = sentence.lower()
    action = action.lower()
    noun = noun.lower()
    color = color.lower()

    total_unique_sentences += 1

    for noun_synonym in NOUNS[noun.upper()]:
        print(noun_synonym)
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
                        data.append([new_sentence2,action,noun_synonym,color,relative_action,
                                     relative_object,relative_object_color])
                        total_sentences += 1
                        STATS_DATA[action.upper()] += 1

            else:
                new_sentence = new_sentence.replace(action.lower(), action_synonym.lower())
                data.append([new_sentence, action, noun_synonym, color, relative_action,
                             relative_object,relative_object_color])
                total_sentences += 1
                STATS_DATA[action.upper()] += 1


### Create files and Save data ###
UNIQUE_SENTENCES_FILE = 'data/unique_sentences.txt'
TRAINING_SENTENCES_FILE = 'data/sentences_to_train_on.txt' #Incoming sentences to create into data
DATA_FILE = 'data/training_data.csv'
STATS_FILE = 'data/stats.json'
FIELDS = ['Sentence','Target_Action','Noun','Color',
          'Relative_Action','Relative_Object', 'Relative_Object_Color']

def createFiles():
    if not os.path.isfile(UNIQUE_SENTENCES_FILE):
        with open(UNIQUE_SENTENCES_FILE, 'w', newline='') as outfile:
            csv.writer(outfile).writerow(FIELDS)
            outfile.close()

    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as outfile:
            csv.writer(outfile).writerow(FIELDS)
            outfile.close()

    if not os.path.isfile(TRAINING_SENTENCES_FILE):
        with open(TRAINING_SENTENCES_FILE, 'w', newline='') as outfile:
            csv.writer(outfile).writerow(FIELDS)
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


def save_Unique_Sentence(data):
    with open(UNIQUE_SENTENCES_FILE, 'a', newline='') as sentencefile:
        csv.writer(sentencefile).writerow(data)
        sentencefile.close()

def save_Data():
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


createFiles()

data = [] #create_Data stores everything in data


with open(TRAINING_SENTENCES_FILE,'r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter = ',')

    #[Sentence,Target_Action,Noun,Color,Relative_Action,
    #           Relative_Object,Relative_Object_Color]
    target_fields = next(csv_reader)

    for row in csv_reader:
        sentence = row[0]
        action = row[1]
        noun = row[2]
        color = row[3]
        relative_action = row[4]
        relative_object = row[5]
        relative_object_color = row[6]

        create_Data(action = action,noun = noun,color = color,sentence = sentence,
                relative_action= relative_action,relative_object = relative_object,
                relative_object_color =relative_object_color)

        save_Unique_Sentence(row)

print(data)
save_Data()




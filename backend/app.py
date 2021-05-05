from flask import Flask, jsonify, request, send_from_directory
import os
from chatbot import chatbot

from transformers import BertTokenizer
import tensorflow as tf

from dbqueries import test, setMessages, getMess
import json


# import json
from flask_cors import CORS
from environment import (
    getEnvironment,
    getMessages,
    getEnvironmentHistory,
    clearBoard,
    undo,
    clearBoardAppStart,
)
from machine_learning.chatbot_ml import chatbot_ml

app = Flask(__name__)
CORS(app)

# dummy data
dummy = [
    {"sass": "sample_response_1"},
    {"sass": "sample_response_2"},
    {"sass": "sample_response_3"},
]

# clear board to clear image
clearBoardAppStart()

print("loading ml........")
model = tf.keras.models.load_model("Model.h5")
# main route (Landing Page)


@app.route("/", methods=["GET"])
def main_route():
    return jsonify({"about": "Default"})


# endpoint that returns dummy data above (Used For Testing)


@app.route("/dummy", methods=["GET"])
def return_dummy():
    return jsonify({"dummy": dummy})


# endpoint that echos input (Used For Testing)


@app.route("/repeat", methods=["GET", "POST"])
def repeat_route():
    if request.method == "POST":
        post_data = request.get_json()
        user_res = post_data["user"]
        return jsonify({"SHRDLU Echo: ": user_res})
    return jsonify({"get": "requested"})


# endpoint that calls chatbot function (SHRDLU Response)


@app.route("/chat", methods=["GET", "POST"])
def chatbot_route():
    if request.method == "POST":
        post_data = request.get_json()
        user_res = post_data["user"]
        bot_res = chatbot(user_res)
        test()
        return jsonify({"SHRDLU": bot_res})
    return jsonify({"get": "requested"})


# endpoint that returns environment array

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
INPUT_SIZE = 20


@app.route("/mlchat", methods=["GET", "POST"])
def chatbot_ml_route():
    if request.method == "POST":
        post_data = request.get_json()
        user_res = post_data["user"]
        sentence = user_res
        user_res = user_res.lower()
        tokenize_sentence = tokenizer.encode(
            user_res, padding="max_length", max_length=INPUT_SIZE
        )
        print(user_res)
        print(tokenize_sentence)
        res = model.predict([tokenize_sentence])
        resp = chatbot_ml(res, sentence)
        return jsonify({"SHRDLU": resp})
    return jsonify({"get": "requested"})


# endpoint that returns environment array


@app.route("/environment", methods=["GET"])
def environment_route():
    if request.method == "GET":
        env = getEnvironment()
        return jsonify({"env": env})
    return None


# endpoint that returns environment image file


@app.route("/environment_image", methods=["GET"])
def environment_image():
    if request.method == "GET":
        return send_from_directory("images", "env_image.png")
    return None


@app.route("/messages", methods=["GET"])
def messages():
    if request.method == "GET":
        globalList = jsonify({"messages": getMessages()})
        globalListJSON = globalList.get_json()
        #strings
        globalListString = json.dumps(globalListJSON)
        print("comparte1")
        print(globalListString)
        print(type(globalListString))
        #turn back no need cause string is json type string

        #can store to db
        #setMessages('instance1', globalListString)

        #can be used to get data from an instance in db
        print("comparte2")
        dbList = getMess('instance1')
        print(dbList)
        print(type(dbList))

        #this would append so i can put directly in chat route
        #if works move it to environment.py along with queries
        #get query string, cut off last 2 chars add a comma
        #print(dbList[:-2]) + , + below
        #get global string cut off all up to and including [
        #print(globalListString[14:])
        #add strings
        print("comparte3")
        concatedVers = dbList[:-2] + ', ' + globalListString[14:]
        print(concatedVers)
        jsonify(concatedVers)
        #this fails because string operation changes it from json string to normal string
        #can attempt to jsonfiy string (FAILED) OR 
        #return dict(convert to list and initalize global to that) from query and append to that in environment.py
        #^ FOR THAT turn this route back to normal and just put setMessages inside chat route
        print("checking")
        print(getMessages())
        print(type(getMessages()))
        print(concatedVers[13:-1])

        print("typ check")
        print(type(globalList))
        print(type(jsonify({"messages" : concatedVers})))
        #might be the fuckin comma but idk
        
        #return dbList returns messageList from db
        #return globalListString returns from global list
        #return concat fails which is supposed to be string concat of both List strings
        return concatedVers 
    return None


@app.route("/history", methods=["GET"])
def history():
    if request.method == "GET":
        return jsonify({"history": getEnvironmentHistory()})
    return None



@app.route("/instances", methods=["GET"])
def instance_list():
    if request.method == "GET":
        return jsonify({"instances": getInstances()})
    return None


@app.route("/clear", methods=["POST"])
def clear_route():
    if request.method == "POST":
        bot_res = clearBoard()
        bot_res = {res["name"]: res["text"] for res in bot_res}
        return jsonify(bot_res)
    return None


@app.route("/undo", methods=["POST"])
def undo_route():
    if request.method == "POST":
        bot_res = undo()
        bot_res = {res["name"]: res["text"] for res in bot_res}
        return jsonify(bot_res)
    return None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5555), debug=True)

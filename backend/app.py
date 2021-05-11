from flask import Flask, jsonify, request, send_from_directory
import os
from chatbot import chatbot

from transformers import BertTokenizer
import tensorflow as tf

from dbqueries import test, storeField, retrieveField, createInstanceStorage, getAllStoredInstances, createInstanceStorage
import json


from flask_cors import CORS
from environment import (
    getEnvironment,
    getGrid,
    getMessages,
    getHistory,
    clearBoard,
    undo,
    clearBoardAppStart,
    getInstances,
    setGrid,
    setMessages,
    setHistory,
    setGridSize
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
# clearBoardAppStart()

print("loading ml........")
model = tf.keras.models.load_model("Model.h5")
# model._make_predict_function()
# main route (Landing Page)

# '''
# this should be going in a route that fetches an instance here rn for testing
setMessages(eval(retrieveField('A7Rds3Sh8AQDESznBxqj', 'messages')))
setGrid(eval(retrieveField('A7Rds3Sh8AQDESznBxqj', 'grid')))
setHistory(eval(retrieveField('A7Rds3Sh8AQDESznBxqj', 'history')))
setGridSize(eval(retrieveField('A7Rds3Sh8AQDESznBxqj', 'size')))
# '''


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

        # writing grid to db, overwriting
        storeField('A7Rds3Sh8AQDESznBxqj', 'grid', str(getGrid()))

        # writing history to db, appended (prob can just do history[-1] for grid but for now store all)
        storeField('A7Rds3Sh8AQDESznBxqj', 'history', str(getHistory()))

        # writing messages to db, appended to prev
        storeField('A7Rds3Sh8AQDESznBxqj', 'messages', str(getMessages()))

        # testing queries now
        # createInstanceStorage('nightmare','kara','5')
        # print(getAllStoredInstances('instances'))

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

        # writing grid to db, overwriting
        storeField('A7Rds3Sh8AQDESznBxqj', 'grid', str(getGrid()))

        # writing history to db, appended (prob can just do history[-1] for grid but for now store all)
        storeField('A7Rds3Sh8AQDESznBxqj', 'history', str(getHistory()))

        # writing messages to db, appended to prev
        storeField('A7Rds3Sh8AQDESznBxqj', 'messages', str(getMessages()))

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
        return jsonify({"messages": getMessages()})
    return None


@app.route("/history", methods=["GET"])
def history():
    if request.method == "GET":
        return jsonify({"history": getEnvironmentHistory()})
    return None


@app.route("/instances", methods=["GET"])
def instance_list():
    if request.method == "GET":
        return jsonify({"instances": getAllStoredInstances('instances')})
    return None


@app.route('/createinstance', methods=["POST"])
def create():
    if request.method == "POST":
        post_data = request.get_json()
        worldName = post_data["instanceName"]
        creator = post_data["creatorName"]
        size = post_data["instanceSize"]
        createInstanceStorage(worldName, creator, size)
    return None


@app.route("/clear", methods=["POST"])
def clear_route():
    if request.method == "POST":
        bot_res = clearBoard()
        bot_res = {res["name"]: res["text"] for res in bot_res}

        # writing grid to db, overwriting
        storeField('A7Rds3Sh8AQDESznBxqj', 'grid', str(getGrid()))

        # writing history to db, appended (prob can just do history[-1] for grid but for now store all)
        storeField('A7Rds3Sh8AQDESznBxqj', 'history', str(getHistory()))

        # writing messages to db, appended to prev
        storeField('A7Rds3Sh8AQDESznBxqj', 'messages', str(getMessages()))

        return jsonify(bot_res)
    return None


@app.route("/undo", methods=["POST"])
def undo_route():
    if request.method == "POST":
        bot_res = undo()
        bot_res = {res["name"]: res["text"] for res in bot_res}

        # writing grid to db, overwriting
        storeField('A7Rds3Sh8AQDESznBxqj', 'grid', str(getGrid()))

        # writing history to db, appended (prob can just do history[-1] for grid but for now store all)
        storeField('A7Rds3Sh8AQDESznBxqj', 'history', str(getHistory()))

        # writing messages to db, appended to prev
        storeField('A7Rds3Sh8AQDESznBxqj', 'messages', str(getMessages()))

        return jsonify(bot_res)
    return None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5555), debug=True)

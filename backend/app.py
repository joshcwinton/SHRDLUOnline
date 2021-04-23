from flask import Flask, jsonify, request, send_from_directory
import os
from chatbot import chatbot
from flask_cors import CORS
from environment import (
    getEnvironment,
    clearBoard,
    getMessages,
    getEnvironmentHistory,
)


app = Flask(__name__)
CORS(app)

# dummy data
dummy = [
    {"sass": "sample_response_1"},
    {"sass": "sample_response_2"},
    {"sass": "sample_response_3"},
]

# clear board to clear image
clearBoard()

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
        return jsonify({"SHRDLU": bot_res})
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


@app.route("/instance_list", methods=["GET"])
def instance_list():
    if request.method == "GET":
        return jsonify({"instanceList": ["a", "b", "c"]})
    return None


if __name__ == "__main__":
    #    app.run(debug = True)
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5555), debug=True)

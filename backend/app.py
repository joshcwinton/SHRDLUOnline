from flask import Flask, jsonify, request, send_from_directory
import os
from chatbot import chatbot
import json
from flask_cors import CORS
from environment import getEnvironment, clearBoard, getMessages, getEnvironmentHistory, clearBoard, undo, clearBoardAppStart
from machine_learning.chatbot_ml import chatbot_ml

app = Flask(__name__)
CORS(app)

# dummy data
dummy = [{'sass': 'sample_response_1'},
         {'sass': 'sample_response_2'},
         {'sass': 'sample_response_3'}]

# clear board to clear image
clearBoardAppStart()

# main route (Landing Page)


@app.route('/', methods=['GET'])
def main_route():
    return jsonify({"about": "Default"})

# endpoint that returns dummy data above (Used For Testing)


@app.route('/dummy', methods=['GET'])
def return_dummy():
    return jsonify({'dummy': dummy})

# endpoint that echos input (Used For Testing)


@app.route('/repeat', methods=['GET', 'POST'])
def repeat_route():
    if request.method == 'POST':
        post_data = request.get_json()
        user_res = post_data["user"]
        return jsonify({"SHRDLU Echo: ": user_res})
    return jsonify({"get": "requested"})

# endpoint that calls chatbot function (SHRDLU Response)


@app.route('/chat', methods=['GET', 'POST'])
def chatbot_route():
    if request.method == 'POST':
        post_data = request.get_json()
        user_res = post_data["user"]
        bot_res = chatbot(user_res)
        return jsonify({"SHRDLU": bot_res})
    return jsonify({"get": "requested"})

# endpoint that returns environment array


@app.route('/mlchat', methods=['GET', 'POST'])
def chatbot_ml_route():
    if request.method == 'POST':
        post_data = request.get_json()
        user_res = post_data["user"]
        bot_res = chatbot_ml(user_res)
        return jsonify({"SHRDLU": bot_res})
    return jsonify({"get": "requested"})

# endpoint that returns environment array


@app.route('/environment', methods=['GET'])
def environment_route():
    if request.method == 'GET':
        env = getEnvironment()
        return jsonify({"env": env})
    return None

# endpoint that returns environment image file


@app.route('/environment_image', methods=['GET'])
def environment_image():
    if request.method == 'GET':
        return send_from_directory('images', 'env_image.png')
    return None


@app.route('/messages', methods=['GET'])
def messages():
    print(getMessages())
    if request.method == 'GET':
        return jsonify({"messages": getMessages()})
    return None


@app.route('/history', methods=['GET'])
def history():
    if request.method == 'GET':
        return jsonify({"history": getEnvironmentHistory()})
    return None


@app.route('/clear', methods=['POST'])
def clear_route():
    if request.method == 'POST':
        bot_res = clearBoard()
        bot_res = {res["name"]: res["text"] for res in bot_res}
        return jsonify(bot_res)
    return None


@app.route('/undo', methods=['POST'])
def undo_route():
    if request.method == 'POST':
        bot_res = undo()
        bot_res = {res["name"]: res["text"] for res in bot_res}
        return jsonify(bot_res)
    return None


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.getenv('PORT', 5555), debug=True)

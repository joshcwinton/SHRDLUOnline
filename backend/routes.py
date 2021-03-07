from flask import Flask, jsonify, request
import os
from chatbot import chatbot
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#dummy data
dummy = [{'sass' : 'sample_response_1'}, {'sass' : 'sample_response_2'}, {'sass' : 'sample_response_3'}]

#main route (Landing Page)
@app.route('/', methods = ['GET'])
def main_route():
        return jsonify({"about" : "Default"})

#endpoint that returns dummy data above (Used For Testing)
@app.route('/dummy', methods = ['GET'])
def return_dummy():
    return jsonify({'dummy' : dummy})
            
#endpoint that echos input (Used For Testing)
@app.route('/repeat', methods = ['GET','POST'])
def repeat_route():
        if request.method == 'POST':
                post_data = request.get_json()
                user_res = post_data["user"]
                return jsonify({"SHRDLU Echo: " : user_res})
        return jsonify({"get" : "requested"})

#endpoint that calls chatbot function (SHRDLU Response)
@app.route('/chat', methods = ['GET', 'POST'])
def chatbot_route():
        if request.method == 'POST':
                post_data = request.get_json()
                user_res = post_data["user"]
                bot_res = chatbot(user_res)
                return jsonify({"SHRDLU": bot_res})
        return jsonify({"get": "requested"})


if __name__ == '__main__':
#    app.run(debug = True)
    app.run(host = '0.0.0.0', port=os.getenv('PORT', 5555), debug=True)


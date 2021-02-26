from flask import Flask, jsonify, request
import os

app = Flask(__name__)

#dummy data
sentences = [{'sass' : 'sample_response_1'}, {'sass' : 'sample_response_2'}, {'sass' : 'sample_response_3'}]

#main route defaults
@app.route('/', methods = ['GET'])
def main_route():
        return jsonify({"about":"Default"})

#endpoint GET ALL (UNUSED)
@app.route('/sentences', methods = ['GET'])
def return_All():
    return jsonify({'sentences' : sentences})
            
#endpoint POST
@app.route('/sentences', methods = ['GET','POST'])
def test_route():
    sentence = {'sass' : request.json['sass']}

    #sentences.append(sentence)
    return jsonify({'sentences' : sentence})


if __name__ == '__main__':
#    app.run(debug = True)
    app.run(host = '0.0.0.0', port=os.getenv('PORT', 5555), debug=True)


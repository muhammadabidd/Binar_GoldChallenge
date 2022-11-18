from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "Menyapa DUNIAA",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run(debug = True)
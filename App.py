#Importing Libraries
import re
import sqlite3
import pandas as pd
import os


from datetime import datetime
from flask import Flask, jsonify, render_template, send_from_directory, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from fileinput import filename
from Script import process_word
from werkzeug.utils import secure_filename

#Difining app
app = Flask(__name__)


app.json_encoder= LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda : 'TWORST : API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda : '1.0.0'),
    'description' : LazyString(lambda : 'Dokumentasi API untuk Data Processing dan Modeling'), 
    },
    host = LazyString(lambda: request.host)
)

#Flask swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)


#Connecting to database
conn = sqlite3.connect('text_processing.db', check_same_thread=False)
c = conn.cursor()
#Defining and executing the query for table data if it not available
conn.execute('''CREATE TABLE IF NOT EXISTS data (text varchar(255), text_clean varchar(255));''')


#Homepage
@app.route('/', methods=['GET'])
def get():
    return render_template('index.html', files=os.listdir('output'))

#1 Basic API "Hello World"
@swag_from("docs/hello_world.yml", methods = ['GET'])
@app.route('/hello_world', methods=['GET'])
def hello_world():
    json_response = {
        'status_code' : 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

#2 plain API "text"
@swag_from("docs/hello_world.yml", methods = ['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : "Halo, selamat datang di API saya",
    }

    response_data = jsonify(json_response)
    return response_data

#3 API for cleaning provided text 
@swag_from("docs/hello_world.yml", methods = ['POST'])
@app.route('/text_clean', methods=['POST'])
def text_clean():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : process_word("Hallo,,,, nama*&@ saya adl Abid,,,, trims"),
    }
    
    response_data = jsonify(json_response)
    return response_data

#4 API for processing inputted text
@swag_from("docs/text_processing.yml", methods = ['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    text_clean = process_word(text)

    with conn:
        c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''', (text, text_clean))
        conn.commit()
    

    json_response = {
        'status_code' : 200,
        'description' : "Teks yang sudah diproses",
        'data' : text_clean,
    }

    response_data = jsonify(json_response)
    return response_data



#Defining allowed extensions
allowed_extensions = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


#5 API for processing inputted file
@swag_from("docs/file_Upload.yml", methods = ['POST'])
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files['file']

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        new_filename = f'{filename.split(".")[0]}.csv'
        
        
        save_location = os.path.join('input', new_filename)
        file.save(save_location)


        filepath = 'input/' + str(new_filename)

        data = pd.read_csv(filepath, encoding='latin-1')
        first_column_pre_process = data.iloc[:, 0]

        cleaned_word = []

        for text in first_column_pre_process:
            file_clean = process_word(text)

            with conn:
                c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''',(text, file_clean))
                conn.commit()

            cleaned_word.append(file_clean)
        
        new_data_frame = pd.DataFrame(cleaned_word, columns= ['Cleaned Text'])

        outputfilepath = f'output/{new_filename}'
        new_data_frame.to_csv(outputfilepath)
        print(new_data_frame)


    json_response = {
        'status_code' : 200,
        'description' : "File yang sudah diproses",
        'data' : "open this link to download : http://127.0.0.1:5000/download",
    }

    response_data = jsonify(json_response)
    return response_data

#Route for downloading processed file
@app.route('/download')
def download():
    return render_template('download.html', files=os.listdir('output'))

#Route for accesing directory to download
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('output', filename)


# Error Handling
@app.errorhandler(400)
def handle_400_error(_error):
    "Return a http 400 error to client"
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    "Return a http 401 error to client"
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    "Return a http 404 error to client"
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)

#App runner
if __name__ == '__main__' :
    app.run(debug=True)


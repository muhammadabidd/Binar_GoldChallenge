from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hellllllo World 2"

if __name__ == '__main__':
    app.run(debug = True)
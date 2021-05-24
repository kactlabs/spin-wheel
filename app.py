from flask import Flask, request, render_template
import json


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('front.html')


@app.route('/wheel', methods = ['GET', 'POST'])
def hello():
    json = get_json('data.json')
    data = json["user_data"]
    return render_template('index.html', values=data)

def get_json(USERS_JSONPATH):

    json_file = open(USERS_JSONPATH)
    json_data = json.load(json_file)
    #print(json_data)

    return json_data

if __name__== "__main__":
    app.run(debug=True)

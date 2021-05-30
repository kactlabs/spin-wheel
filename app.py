
'''
Created on 
    

Course work: 
    

@author: 
    Ana Jessica
    Ishita

Source:
    
'''

# Import necessary modules
from flask import Flask, request, render_template
import json

app = Flask(__name__)
USERS_JSONPATH = "data.json"

@app.route('/')
def home():
    return render_template('front.html')


# @app.route("/wheel", methods = ['GET', 'POST'])
# def wheel():

#     user_list = [
#         "Ana", 
#         "Vedha",
#         "Gokul",
#         "Prakash",
#         "Elakia",
#         "Divya",
#         "Aswin",
#         "Praabindh",
#         "Ishita",
#         "Mohit",
#         "Sanjana",
#         "praveena"

#     ]

#     user_string = ','.join(user_list)
    
#     return render_template("index.html", user_str = user_string)


@app.route('/wheel', methods = ['GET', 'POST'])
def hello():
    json = get_json('data.json')
    data = json["user_data"]
    return render_template('index.html', values=data)


@app.route("/admin", methods = ['GET'])
def admin():
    
    return render_template("admin.html")

@app.route('/admin/post',methods=['GET','POST'])
def get_json():

    json_file = open(USERS_JSONPATH)
    json_data = json.load(json_file)
    #print(json_data)

    return json_data

# return render_template('admin.html')

if __name__== "__main__":
    app.run(debug=True)

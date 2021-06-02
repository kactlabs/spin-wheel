
'''
Created on 
    

Course work: 
    

@author: 
    Talha
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

@app.route('/wheel', methods = ['GET', 'POST'])
def hello():
    json = get_json()
    data = json["user_data"]
    return render_template('index.html', values=data)


@app.route("/admin", methods = ['GET'])
def admin():
    
    return render_template("admin.html")

@app.route('/admin/view',methods=['GET','POST'])
def get_json():

    json_file = open(USERS_JSONPATH)
    json_data = json.load(json_file)
    #print(json_data)

    return json_data

@app.route('/admin/post',methods=['GET','POST'])
def add_json():

    new_value = request.values.get("wheel-names")

    data_dict = get_json()

    data_list = data_dict["user_data"]

    data_list.reverse()

    if len(data_list) == 0:
        num = 0
    else:
        num =  data_list[0]["value"]

    new_value_dict = {
        
            "label": new_value,
            "value": num + 1 , 
            "question": new_value
        
    }

    data_list.reverse()

    data_list.append(new_value_dict)

    updated_data_dict = {
        "user_data": data_list
    }

    with open(USERS_JSONPATH, 'w') as outfile:
        json.dump(updated_data_dict, outfile)

    return render_template("admin.html")

@app.route('/admin/flush',methods=['GET','POST'])
def flush_json():

    data_dict = get_json()

    data_list = data_dict["user_data"]

    data_list = []

    empty_data_dict = {
        "user_data": data_list
    }

    with open(USERS_JSONPATH, 'w') as outfile:
        json.dump(empty_data_dict, outfile)

    return render_template("admin.html")

if __name__== "__main__":
    app.run(debug=True)

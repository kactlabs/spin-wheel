
'''
Created on 
    

Course work: 
    

@author: 
    Talha
    Ana Jessica
    Ishita
    Talha

Source:
    
'''

from flask import Flask, request, render_template
import json

app = Flask(__name__)
USERS_JSONPATH = "data.json"

@app.route('/')
def home():
    return render_template('front.html')

@app.route('/wheel', methods = ['GET', 'POST'])
def show_wheel():
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

    return json_data

def check_for_tabs(name):

    name = name.replace('\t',' - ')
    return name

def check_for_newline(all_names):

    splitted_list = all_names.split('\r\n')

    return splitted_list

@app.route('/admin/post',methods=['GET','POST'])
def get_new_value():

    new_value = request.values.get("wheel-names")

    name_list = check_for_newline(new_value)

    for name in name_list:
        add_json(name)

    return render_template("admin.html")

def add_json(new_value):

    new_value = check_for_tabs(new_value)

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

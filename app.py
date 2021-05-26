
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

@app.route('/')
def home():
    return render_template('front.html')

@app.route("/wheel", methods = ['GET', 'POST'])
def wheel():

    user_list = [
        "Ana", 
        "Vedha",
        "Ishita",
        "Gokul",
        "Prakash",
        "Elakia",
        "Divya",
        "Sharon",
        "Talha",
        "Praabindh"
    ]

    user_string = ','.join(user_list)
    
    return render_template("index.html", user_str = user_string)


@app.route("/admin", methods = ['GET'])
def admin():
    
    return render_template("admin.html")

@app.route('/admin/post',methods=['POST'])
def wheelnames():
    
    profile_name=request.form.get("wheel-names")
    print (profile_name)

    arr = []
    arr = profile_name.splitlines()

    my_dict = dict() 
    for index,value in enumerate(arr):
        my_dict[index] = value

    print(json.dumps(my_dict))

    with open("users.json", "w") as outfile:
        outfile.write(json.dumps(my_dict))

    return render_template('admin.html')
    



if __name__== "__main__":
    app.run(debug=True)

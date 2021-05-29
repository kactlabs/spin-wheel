
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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front.html')

@app.route("/wheel", methods = ['GET', 'POST'])
def wheel():

    user_list = [
        "Ana", 
        "Vedha",
        "Gokul",
        "Prakash",
        "Elakia",
        "Divya",
        "Aswin",
        "Praabindh",
        "Ishita",
        "Mohit",
        "Sanjana",
        "praveena"

    ]

    user_string = ','.join(user_list)
    
    return render_template("index.html", user_str = user_string)

if __name__== "__main__":
    app.run(debug=True)

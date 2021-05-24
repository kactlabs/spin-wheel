from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('front.html')


@app.route("/wheel", methods = ['GET', 'POST'])
def wheel():
    
    return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('front.html')


# @app.route('/download',methods=['POST'])
# def download():
#     instance = instaloader.Instaloader()
    
#     instance.download_profile(profile_name= request.form.get("username"))
    

#     return render_template('index.html', prediction_text='Downloaded Successfully')


if __name__== "__main__":
    app.run(debug=True)

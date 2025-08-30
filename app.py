# Import necessary modules
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
USERS_JSONPATH = "data.json"

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('front.html', {"request": request})


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


@app.get('/wheel', response_class=HTMLResponse)
@app.post('/wheel', response_class=HTMLResponse)
def hello(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "values": []})


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get('/admin/post')
@app.post('/admin/post')
def get_json():
    with open(USERS_JSONPATH) as json_file:
        json_data = json.load(json_file)
    return json_data

# return render_template('admin.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5006)

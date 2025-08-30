
'''
Created on 
    

Course work: 
    

@author: 
    Ana Jessica
    Ishita

Source:
    
'''

# Import necessary modules
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
templates = Jinja2Templates(directory="spin-wheel-pooja-varsha-ui-improv/templates")
USERS_JSONPATH = "spin-wheel-pooja-varsha-ui-improv/data.json"

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


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get('/admin/post')
@app.post('/admin/post')
def get_json():
    with open(USERS_JSONPATH) as json_file:
        json_data = json.load(json_file)
    return json_data

@app.get('/wheel', response_class=HTMLResponse)
@app.post('/wheel', response_class=HTMLResponse)
def hello(request: Request):
    json_data = get_json()
    user_data = json_data["user_data"]
    # Assign colors based on the image: blue, red, yellow, green, repeating
    colors = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#9370DB", "#FFA07A", "#20B2AA", "#DA70D6", "#FF4500", "#1E90FF", "#ADFF2F", "#FF69B4"]
    data = []
    for i, name in enumerate(user_data):
        data.append({"label": name, "value": 1, "question": name, "color": colors[i % len(colors)]})
    return templates.TemplateResponse('index.html', {"request": request, "values": data})


@app.post('/add_names')
async def add_names(request: Request, names: str = Form(...)):
    try:
        with open(USERS_JSONPATH, 'r+') as json_file:
            json_data = json.load(json_file)
            new_names = [name.strip() for name in names.split(',')]
            # Filter out empty strings from new_names
            new_names = [name for name in new_names if name]
            if new_names: # Only extend if there are actual names to add
                json_data['user_data'].extend(new_names)
                json_file.seek(0)  # Go to the beginning of the file
                json.dump(json_data, json_file, indent=4)
                json_file.truncate()  # Remove any remaining part of the old data
    except Exception as e:
        print(f"Error updating data.json: {e}")
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""
        <html>
            <head>
                <meta http-equiv="refresh" content="0; url=/wheel">
            </head>
            <body>
                <p>Redirecting...</p>
            </body>
        </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

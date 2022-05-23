import random
import json

def read_json():

    f = open('data.json')
  

    users_dict = json.load(f)
  
    
    users_names = []
    users_probability = []

# prresult_dict={}
    users_dict = users_dict["user_data"]
    for users in users_dict:
        user = users["label"]
        weight = users["value"]

        users_names.append(user)
        users_probability.append(weight)

            
    return users_names , users_probability



# names = ["nagul", "Sudhir", "sivaram", "roughit", "elakiya"]
# probability = [10, 2, 4, 0 ,5]
names,probability = read_json()
wh = tuple(probability)
for i in range(10):
    item = random.choices(names,weights= wh, k=1)
    print("Iteration:", i, "Weighted Random choice is", item[0])

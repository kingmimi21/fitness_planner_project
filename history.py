# history.py
from datetime import date
import json
current_user = ""


def load_exercise_history():
    filename = f'{current_user}_data.json'
    print(f"DEBUG: Loading data from {filename}")
    try:
        with open(filename, 'r') as fp:
            data = json.load(fp)
        return data
    except IOError:
        return dict()


def save_exercise_history(data):
    with open('data.json', 'w') as fp:
        json.dump(data, fp)


def add_exercise_dictionary(dic, exercise, weight, reps):
    today = str(date.today())
    if dic.get(exercise):
        if dic[exercise].get(today):
            dic[exercise][today].append({'weight': weight, 'reps': reps})
        else:
            dic[exercise][today] = [{'weight': weight, 'reps': reps}]
    else:
        dic[exercise] = {today: [{'weight': weight, 'reps': reps}]}
    return dic

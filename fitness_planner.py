import history
import os
import sys
import yaml
import json
import time
from datetime import date, datetime
import calendar
import random

from utils import countdown_for_rest, round_nearest_five
from history import load_exercise_history, save_exercise_history, add_exercise_dictionary
from visuals import plot_progress
current_user = ""
history.current_user = current_user


def load_config(config):
    with open(config + '.yaml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    return conf


def view_exercise_history():
    data = load_exercise_history()
    if not data:
        print("No history found. Starting fresh.")
        return
    print("\n--- Progress Summary ---")
    for exercise, days in data.items():
        total_sets = sum(len(s) for s in days.values())
        print(f"{exercise}: {total_sets} sets recorded")

    print("\n=== Exercise History ===")
    for exercise, dates in data.items():
        print(f"\n{exercise}")
        for day, sets in dates.items():
            set_details = ', '.join(
                [f"{s['weight']}x{s['reps']}" for s in sets])
            print(f"{day}: {set_details}")


def load_exercise_history():
    try:
        with open(f'{current_user}_data.json', 'r') as fp:
            data = json.load(fp)
        return data
    except IOError:
        return dict()


def add_exercise_dictionary(dic, exercise, weight, reps):
    # {"bench press": {today: [{weight: 150, reps: 6}, {weight: 150, reps: 6}, {weight: 150, reps: 6}]}}
    today = str(date.today())
    if dic.get(exercise):
        if dic[exercise].get(today):
            dic[exercise][today] = dic[exercise][today] + \
                [{'weight': weight, 'reps': reps}]
        else:
            dic[exercise][today] = [{'weight': weight, 'reps': reps}]
    else:
        dic[exercise] = {today: [{'weight': weight, 'reps': reps}]}
    return dic


def save_exercise_history(data):
    with open(f'{current_user}_data.json', 'w') as fp:
        json.dump(data, fp)


def extract_int(s):
    return [int(x) for x in s.split() if x.isdigit()][0]


def convert_weight_string(s):
    """translates input to weight.
    "bar + 65" => 175 (lbs)
    not robust"""
    if "bar" in s:
        plate_weight = extract_int(s.split("bar")[1].split("+")[1])  # prettify
        return 45 + plate_weight * 2
    else:
        return extract_int(s)


def round_nearest_five(num):
    return int(num//5*5 + (5 if (num % 5) >= 2.5 else 0))


def interact_with_user(exercise, num_sets, warmup=False, rest_min=2):
    """Displays the current exercise and tracks number of reps performed"""
    exercise = random.choice([x.title().strip() for x in exercise.lstrip(
        '*').lstrip('^').lstrip('=').split('OR')])
    exercise_history = load_exercise_history()
    if exercise_history is None:
        exercise_history = {}

    prev_numbers = []
    if exercise_history.get(exercise):
        last_time = list(exercise_history[exercise].keys())[-1]
        # last_time_dow = calendar.day_name[datetime.strptime('2014-12-04', '%Y-%m-%d').date().weekday()]
        prev_numbers = exercise_history[exercise][last_time]

    print(f"===== {exercise} =====")

    if warmup:
        if not prev_numbers:
            inp = input(
                f"What's your best guess of your 4-6RM for {exercise}?")
            weight = convert_weight_string(inp)
        else:
            weight = convert_weight_string(prev_numbers[0]["weight"])
        print("       ( warm up ) ")

        def warmup_routine(reps, percent, rest_min):
            input(
                f"{reps} reps of {round_nearest_five(weight*percent)}. Press Enter to continue...")
            countdown_for_rest(rest_min)

        for (percent, reps, rest_min) in [(.5, 12, 1), (.5, 10, 1), (.7, 6, 1), (.9, 2, 2)]:
            warmup_routine(reps, percent, rest_min)

    if exercise_history.get(exercise):
        prev_num_str = [x['weight'] + 'x' + x['reps'] for x in prev_numbers]
        print(
            f" ----- {exercise} -----\r\n{last_time}: {', '.join(prev_num_str)}")

    for s in range(num_sets):  # TODO: handle warmups
        while True:
            inp = input(f"Set {s+1}! Enter weight, reps (e.g., 50, 10): ")
            try:
                weight, reps = inp.split(',', 1)
                weight = weight.strip()
                reps = reps.strip()
                if weight.replace('.', '', 1).isdigit() and reps.isdigit():
                    break
                else:
                    raise ValueError
            except ValueError:
                print(
                    "Invalid input format> Please enter weight and reps in the format 'weight, reps' (e.g., 50,10).")

        exercise_history = add_exercise_dictionary(
            exercise_history, exercise, weight, reps)
        save_exercise_history(exercise_history)
        countdown_for_rest(2)
    None


def countdown_for_rest(min):
    def display_time(s):
        def display_min(m): return str(m) + " min" if m > 0 else ""
        def display_sec(s): return str(s) + " sec" if s > 0 else ""
        sys.stdout.write(
            f"Rest for {display_min(s//60)} {display_sec(s%60)}         ")
    for remaining in range(int(min*60), 0, -1):
        sys.stdout.write("\r")
        display_time(remaining)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")


def shuffle(exercises, count):
    """Apply modifiers and then randomly shuffles list"""
    def build_weights(exercises):
        weights = list(map(lambda x: 0.0 if x.startswith(
            '*') else (1.0 if x.startswith('^') else 0.5), exercises))
        sum_weights = sum(weights)
        weights = list(map(lambda x: x/sum_weights, weights))
        return weights

    top_priority = [x for x in exercises if x.startswith('**')]
    weights = build_weights(exercises)
    # random.choices can result in duplicates
    the_rest = []
    for _ in range(count - len(top_priority)):
        chosen = random.choices(exercises, weights=weights, k=1)[0]
        while chosen in the_rest:
            chosen = random.choices(exercises, weights=weights, k=1)[0]
        the_rest.append(chosen)

    # ensuring = is last exercise performed
    return top_priority + [x for x in the_rest if not x.startswith('=')] + [x for x in the_rest if x.startswith('=')]


def main():
    exercises = load_config("exercises")
    routine = load_config("routine")

    current_day = calendar.day_name[date.today().weekday()]
    todays_routine = routine.get(current_day, None)

    if todays_routine:
        for muscle_group in todays_routine:
            exercise_set_count = todays_routine[muscle_group]
            muscle_group_exercises = shuffle(
                exercises[muscle_group], exercise_set_count)
            for i in range(exercise_set_count):
                # hardcoding num_sets for now
                interact_with_user(
                    muscle_group_exercises[i], 3, i == 0, rest_min=1.5)

    else:
        print("IT'S YOUR REST DAY!!!")
        # TODO check if value is actually a day of the week, or validate config?


def show_summary_stats():
    data = load_exercise_history()
    print("\n=== Summary Statistics ===")
    for exercise, dates in data.items():
        total_sets = sum(len(sets) for sets in dates.values())
        print(f"{exercise}: {total_sets} sets recorded")


if __name__ == '__main__':
    current_user = input("Enter your name: ").strip().lower().replace(" ", "_")
   import history
history.current_user = current_user
   while True:
        print("\n=== Exercise Planner Menu ===")
        print("1. Start today's workout")
        print("2. View exercise history")
        print("3. View summary statistics")
        print("4.Plot progress for an excercise")
        print("5. Exit")

        choice = input("Enter your Choice (1-5): ")

        if choice == '1':
            main()
        elif choice == '2':
            view_exercise_history()
        elif choice == '3':
            show_summary_stats()
        elif choice == '4':
            data = load_exercise_history()
            print("Available exercises with data:")
            print(list(data.keys()))  # <-- Add this line for debugging
            for ex in data.keys():
                print(f"- {repr(ex)}")
            exercise_name = input(
                "Enter the exercise name exactly as above: ").strip()
            plot_progress(exercise_name)
        elif choice == '5':
            print("Exiting the planner. Stay fit and healthy:)")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5")

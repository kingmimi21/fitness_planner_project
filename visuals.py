# visuals.py
import matplotlib.pyplot as plt
from history import load_exercise_history


def plot_progress(exercise_name):
    data = load_exercise_history()
    normalized_input = exercise_name.strip().lower()
    matched_key = None
    print("DEBUG: Comparing to these keys:")
    for ex in data.keys():
        print(f"  {repr(ex)} -> {ex.strip().lower()} (input: {normalized_input})")
        if ex.strip().lower() == normalized_input:
            matched_key = ex
            break
    if not matched_key:
        print("No data for that exercise.")
        return
    dates = sorted(data[matched_key].keys())
    avg_weights = []
    for day in dates:
        weights = [int(s['weight']) for s in data[matched_key][day]]
        avg_weights.append(sum(weights) / len(weights))
    import matplotlib.pyplot as plt
    plt.plot(dates, avg_weights, marker='o')
    plt.title(f"Average Weight Over Time for {matched_key}")
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

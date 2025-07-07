# utils.py
import sys
import time


def countdown_for_rest(mins):
    def display_min(m):
        return str(m) + " min" if m > 0 else ""

    def display_sec(s):
        return str(s) + " sec" if s > 0 else ""

    def display_time(s):
        sys.stdout.write(f"Rest for {display_min(s//60)} {display_sec(s%60)}")
    for remaining in range(int(mins * 60), 0, -1):
        sys.stdout.write("\r")
        display_time(remaining)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")


def round_nearest_five(num):
    return int(num//5*5 + (5 if (num % 5) >= 2.5 else 0))

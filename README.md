# Excercise_Diary_Planner


The Exercise Diary Planner is a Python-based command-line application that allows users to plan, log, and track their workouts over time. It supports multiple users, keeps a history of exercises, shows summary statistics, and allows users to monitor progress based on sets and weights.

The project is built on top of a forked GitHub repository and has been significantly extended and improved for a resubmission project to demonstrate practical use of Python features such as file I/O, modularization, data visualization, and user input handling.

  ~ Features ~


- Menu-based navigation


- User login support (per-user workout history)
 

- View workout history by date and exercise
 

- View total sets completed per exercise
 

- Input validation (for weights/reps)
 

- Rest timer between sets


- Exercise progress plotting (optional / bonus)
 

- Modularized code for maintainability

 
 
 ~ How to Run the App ~

 
 
 Prerequisites:


- Python 3.x installed


- Terminal or command prompt access


- matplotlib installed for plotting (optional)

Install requirements:


- pip install matplotlib
 
 
 Run the app:


- python fitness_planner.py

When prompted:
Enter your name. This will create a personalized workout history file named like alex_data.json.

~ Menu Options ~

=== Exercise Planner Menu ===
1. Start today's workout
2. View exercise history
3. View summary statistics
4. Plot progress for an exercise
5. Exit

~ Technologies Used ~


- Python 3


- json and yaml for data handling


- matplotlib for plotting progress


- Command-line interface (CLI)


- Modular file structure:


- fitness_planner.py – main program


- utils.py – countdown timer, helpers


- history.py – handles saving and loading data


- visuals.py – handles plotting

 ~ User Profiles ~

 Each user has their own file:

e.g. mimi_data.json, john_data.json
This allows multiple people to use the program without overwriting each other’s logs.

Bonus: Data Visualization
Users can view line graphs of average weight lifted over time for each exercise. This feature uses matplotlib and is optional if dependencies aren't installed.

~ Improvements Made (compared to original repo) ~



- Completely refactored into separate files (modularized)


- Added menu system and CLI interface


- Implemented user profiles and personalized history files


- Added input validation and error handling


- Created summary statistics and optional progress graphs


- Improved UX with clearer prompts and structure

 ~ Known Issues / Limitations ~



- Plotting may fail if the user has no recorded data or if matplotlib isn't installed


- Does not include GUI (command line only)


- Exercises and routines must still be defined in YAML manually
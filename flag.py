import tkinter as tk
from tkinter import messagebox, ttk
import time
import random

# Define flashcards categorized by difficulty
questions = {
    'easy': [
        {'question': "What is 2 + 2?", 'options': ["3", "4", "5", "6"], 'correctAnswer': "4"},
        {'question': "What is 5 + 3?", 'options': ["6", "7", "8", "9"], 'correctAnswer': "8"},
        {'question': "What is 10 - 4?", 'options': ["5", "6", "7", "8"], 'correctAnswer': "6"},
    ],
    'medium': [
        {'question': "What is the capital of France?", 'options': ["Berlin", "Madrid", "Paris", "Rome"], 'correctAnswer': "Paris"},
        {'question': "Which planet is known as the Red Planet?", 'options': ["Earth", "Mars", "Jupiter", "Saturn"], 'correctAnswer': "Mars"},
    ],
    'hard': [
        {'question': "What is the chemical symbol for gold?", 'options': ["Au", "Ag", "Pb", "Fe"], 'correctAnswer': "Au"},
        {'question': "What is the square root of 144?", 'options': ["10", "11", "12", "13"], 'correctAnswer': "12"},
    ]
}

# Theme colors
theme_colors = {
    'easy': "#D4EDDA",  # Light Green
    'medium': "#FFF3CD",  # Light Yellow
    'hard': "#F8D7DA"  # Light Red
}

current_question_index = 0
score = 0
time_left = 60  # Time limit in seconds
selected_difficulty = 'easy'  # Default difficulty

# Function to update the timer
def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)
    else:
        game_over()

# Function to load a new question
def load_question():
    global current_question_index
    question_data = questions[selected_difficulty][current_question_index]
    question_label.config(text=question_data['question'])
    
    for btn in option_buttons:
        btn.destroy()
    
    for option in question_data['options']:
        btn = tk.Button(game_frame, text=option, font=('Arial', 12), width=20, 
                        bg="white", fg="black", relief="raised",
                        command=lambda opt=option: check_answer(opt))
        btn.pack(pady=5)
        option_buttons.append(btn)
    
    # Update progress bar
    question_progress_bar["value"] = (current_question_index + 1) / len(questions[selected_difficulty]) * 100

# Function to check the answer
def check_answer(selected_option):
    global current_question_index, score
    correct_answer = questions[selected_difficulty][current_question_index]['correctAnswer']
    
    if selected_option == correct_answer:
        score += 1
    
    score_label.config(text=f"Score: {score}")
    
    # Move to the next question
    current_question_index += 1
    if current_question_index < len(questions[selected_difficulty]):
        load_question()
    else:
        game_over()

# Function to end the game
def game_over():
    messagebox.showinfo("Time's Up!", f"Game over! Your final score is {score}.")
    root.quit()

# Function to start the game
def start_game(difficulty):
    global selected_difficulty, current_question_index, score, time_left
    selected_difficulty = difficulty
    current_question_index = 0
    score = 0
    time_left = 60  # Reset timer
    score_label.config(text=f"Score: {score}")
    timer_label.config(text=f"Time Left: {time_left}s")
    question_progress_bar["value"] = 0
    
    root.configure(bg=theme_colors[difficulty])
    game_frame.configure(bg=theme_colors[difficulty])
    
    difficulty_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    update_timer()
    load_question()

# Setup the main window
root = tk.Tk()
root.title("Flashcard Quiz App")
root.geometry("400x400")
root.configure(bg="#F8F9FA")

# Difficulty selection screen
difficulty_frame = tk.Frame(root, bg="#F8F9FA")
tk.Label(difficulty_frame, text="Choose Difficulty:", font=('Arial', 14, 'bold'), bg="#F8F9FA").pack(pady=10)

for diff in ['easy', 'medium', 'hard']:
    tk.Button(difficulty_frame, text=diff.capitalize(), font=('Arial', 12), width=20, 
              bg=theme_colors[diff], fg="black", command=lambda d=diff: start_game(d)).pack(pady=5)

difficulty_frame.pack(fill="both", expand=True)

# Game screen
game_frame = tk.Frame(root)
question_label = tk.Label(game_frame, text="", font=('Arial', 16, "bold"), wraplength=300, bg="#F8F9FA")
question_label.pack(pady=20)

option_buttons = []

score_label = tk.Label(game_frame, text="Score: 0", font=('Arial', 12, "bold"), bg="#F8F9FA")
score_label.pack(pady=10)

timer_label = tk.Label(game_frame, text=f"Time Left: {time_left}s", font=('Arial', 12, "bold"), fg="red", bg="#F8F9FA")
timer_label.pack(pady=5)

question_progress_bar = ttk.Progressbar(game_frame, orient="horizontal", length=300, mode="determinate")
question_progress_bar.pack(pady=10)

# Start the application
root.mainloop()


import tkinter as tk
from tkinter import messagebox
import random
import os

# ---------------- SETTINGS ---------------- #

DIFFICULTIES = {
    "Easy": (1, 50, 60),
    "Medium": (1, 100, 45),
    "Hard": (1, 200, 30)
}

number = 0
attempts = 0
score = 0
time_left = 0
game_over = False

HIGH_SCORE_FILE = "highscore.txt"

# ---------------- HIGH SCORE ---------------- #

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_high_score(new_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_score))

high_score = load_high_score()

# ---------------- GAME FUNCTIONS ---------------- #

def start_game():
    global number, attempts, time_left, game_over

    difficulty = difficulty_var.get()
    low, high, timer = DIFFICULTIES[difficulty]

    number = random.randint(low, high)
    attempts = 0
    time_left = timer
    game_over = False

    instruction_label.config(
        text=f"Guess a number between {low} and {high}"
    )

    result_label.config(text="")
    attempts_label.config(text="Attempts: 0")
    timer_label.config(text=f"Time Left: {time_left}s")

    guess_button.config(state="normal")
    countdown()

def countdown():
    global time_left, game_over

    if game_over:
        return

    if time_left > 0:
        timer_label.config(text=f"Time Left: {time_left}s")
        time_left -= 1
        root.after(1000, countdown)
    else:
        game_over = True
        result_label.config(
            text=f"⏰ Time Up! Number was {number}",
            fg="red"
        )
        guess_button.config(state="disabled")

def check_guess(event=None):
    global attempts, score, high_score, game_over

    if game_over:
        return

    try:
        guess = int(entry.get())
        attempts += 1

        if guess < number:
            result_label.config(text="📉 Too Low!", fg="cyan")

        elif guess > number:
            result_label.config(text="📈 Too High!", fg="orange")

        else:
            game_over = True

            earned = max(100 - attempts * 5, 10)
            score += earned

            score_label.config(text=f"Score: {score}")

            if score > high_score:
                high_score = score
                save_high_score(high_score)

            high_score_label.config(
                text=f"High Score: {high_score}"
            )

            result_label.config(
                text=f"🎉 Correct! +{earned} Points",
                fg="lightgreen"
            )

            guess_button.config(state="disabled")

        attempts_label.config(
            text=f"Attempts: {attempts}"
        )

        entry.delete(0, tk.END)

    except ValueError:
        result_label.config(
            text="❌ Enter a valid number",
            fg="red"
        )

def reset_game():
    start_game()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("🎯 Ultimate Guess The Number")
root.geometry("500x500")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🎯 GUESS THE NUMBER",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)

difficulty_var = tk.StringVar(value="Medium")

difficulty_menu = tk.OptionMenu(
    root,
    difficulty_var,
    *DIFFICULTIES.keys()
)
difficulty_menu.pack(pady=5)

instruction_label = tk.Label(
    root,
    text="Choose Difficulty & Start",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 12)
)
instruction_label.pack()

entry = tk.Entry(
    root,
    font=("Arial", 16),
    justify="center",
    width=12
)
entry.pack(pady=15)

entry.bind("<Return>", check_guess)

guess_button = tk.Button(
    root,
    text="Guess",
    command=check_guess,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    width=15
)
guess_button.pack(pady=5)

result_label = tk.Label(
    root,
    text="",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 14)
)
result_label.pack(pady=10)

attempts_label = tk.Label(
    root,
    text="Attempts: 0",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 12)
)
attempts_label.pack()

timer_label = tk.Label(
    root,
    text="Time Left: 0",
    bg="#1e1e1e",
    fg="yellow",
    font=("Arial", 12)
)
timer_label.pack()

score_label = tk.Label(
    root,
    text="Score: 0",
    bg="#1e1e1e",
    fg="lightgreen",
    font=("Arial", 12)
)
score_label.pack()

high_score_label = tk.Label(
    root,
    text=f"High Score: {high_score}",
    bg="#1e1e1e",
    fg="gold",
    font=("Arial", 12)
)
high_score_label.pack()

start_button = tk.Button(
    root,
    text="Start Game",
    command=start_game,
    font=("Arial", 12, "bold"),
    bg="#2196F3",
    fg="white",
    width=15
)
start_button.pack(pady=10)

reset_button = tk.Button(
    root,
    text="Play Again",
    command=reset_game,
    font=("Arial", 12, "bold"),
    bg="#FF9800",
    fg="white",
    width=15
)
reset_button.pack()

root.mainloop()
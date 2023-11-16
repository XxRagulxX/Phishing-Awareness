import random
import sqlite3

# Create the SQLite database
conn = sqlite3.connect('phishing_challenge.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
''')
conn.commit()

# Phishing and legitimate messages
phishing_messages = [
    "Congratulations! You've won a free vacation. Click the link to claim your prize.",
    "Your bank account has been compromised. Please click the link to reset your password.",
    "Urgent message: Your email account will be suspended. Verify your account by clicking the link.",
]

legitimate_messages = [
    "Hello, this is your friend. Can you please send me the homework?",
    "Your monthly newsletter is ready. Click the link to read it.",
    "You have a new message on your social media account. Log in to check it.",
]

# Function to play the game
def play_game():
    print("Welcome to the Phishing Awareness Challenge!")
    name = input("Enter your name: ")
    score = 0

    while True:
        is_phishing = random.choice([True, False])
        message = random.choice(phishing_messages if is_phishing else legitimate_messages)

        print("\nMessage:")
        print(message)

        print("1. Phishing")
        print("2. Legitimate")
        user_input = input("Enter '1' or '2': ")

        if (is_phishing and user_input == '1') or (not is_phishing and user_input == '2'):
            print("Correct! This message is", "phishing" if is_phishing else "legitimate")
            score += 1
        else:
            print("Incorrect. This message is", "phishing" if is_phishing else "legitimate")

        play_again = input("Play again? (y/n): ").strip().lower()

        if play_again != 'y':
            break

    print(f"Your score is {score} out of messages checked.")

    # Insert the user and score into the database
    cursor.execute('INSERT INTO users (name, score) VALUES (?, ?)', (name, score))
    conn.commit()

# Function to display leaderboard
def display_leaderboard():
    print("\nLeaderboard:")
    cursor.execute('SELECT name, score FROM users ORDER BY score DESC LIMIT 3')
    leaderboard = cursor.fetchall()
    for position, (name, score) in enumerate(leaderboard, start=1):
        print(f"{position}. {name}: {score} points")

# Main loop
while True:
    play_game()
    display_leaderboard()

    play_again = input("Do you want to play again? (y/n): ").strip().lower()
    if play_again != 'y':
        break

# Close the database connection
conn.close()

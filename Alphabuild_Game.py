import random
import sqlite3
from flask import Flask, render_template, g, request, url_for, redirect

app = Flask(__name__)

DATABASE = 'phishing_challenge.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create the table if it doesn't exist
with app.app_context():
    cursor = get_db().cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    get_db().commit()

# Phishing and legitimate messages with images
phishing_messages = [
    {"label": "Phishing Image 1", "image": "phishing_image_1.jpg"},
    # Add more phishing messages as needed
]

legitimate_messages = [
    {"label": "Legitimate Image 1", "image": "legitimate_image_1.jpg"},
    # Add more legitimate messages as needed
]

# Function to process answers and display results
def process_answers():
    score = 0
    name = request.form.get('name')

    for i in range(len(phishing_messages)):
        user_input = request.form.get(f'answer_{i}')
        is_phishing = i % 2 == 0  # Every even index is a phishing question

        if (is_phishing and user_input == 'phishing') or (not is_phishing and user_input == 'legitimate'):
            score += 1

    # Insert the user and score into the database
    cursor = get_db().cursor()
    cursor.execute('INSERT INTO users (name, score) VALUES (?, ?)', (name, score))
    get_db().commit()

    question_index = int(request.form.get('question_index')) + 1

    if question_index < len(phishing_messages):
        # If there are more questions, redirect to the next question
        return redirect(url_for('show_question', question_index=question_index, name=name))
    else:
        # Display the leaderboard if all questions are answered
        leaderboard = display_leaderboard()
        return render_template('result.html', name=name, score=score, leaderboard=leaderboard)

# Function to display leaderboard
def display_leaderboard():
    cursor = get_db().cursor()
    cursor.execute('SELECT name, score FROM users ORDER BY score DESC LIMIT 3')
    leaderboard = cursor.fetchall()
    return leaderboard

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is submitted, redirect to the first question
        name = request.form.get('name')
        return render_template('questions.html', question_index=0, name=name, phishing_messages=phishing_messages)
    else:
        return render_template('enter_name.html', phishing_messages=phishing_messages)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    if request.method == 'POST':
        return process_answers()
    else:
        # Display the question based on the index
        name = request.args.get('name')
        return render_template('questions.html', question_index=question_index, name=name, phishing_messages=phishing_messages)

# ... (remaining code)

if __name__ == '__main__':
    app.run(debug=False)

# Close the database connection
conn = get_db()
if conn is not None:
    conn.close()

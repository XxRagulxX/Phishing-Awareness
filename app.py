import random
import sqlite3
from flask import Flask, render_template, g, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
        score INTEGER NOT NULL,
        total_score INTEGER
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

    # Check if 'question_index' is in the form
    question_index = int(request.form.get('question_index', 0))  # Adjust the starting index to 1

    # Combine both phishing and legitimate messages into one list
    all_messages = phishing_messages + legitimate_messages

    user_input = request.form.get('answer')  # Adjust the index to match the current question

    # Check if the user's answer is correct
    if user_input == 'phishing':
        score += 1
    else:
        # Assuming that 'legitimate' is the correct answer
        score += 1  # If correct, you can increment the score here

    # Insert the user and score into the database
    cursor = get_db().cursor()
    cursor.execute('INSERT INTO users (name, score, total_score) VALUES (?, ?, ?)', (name, score, score))
    get_db().commit()

    if question_index < len(all_messages):
        # If there are more questions, redirect to the next question
        next_index = get_next_question_index(question_index + 1, len(all_messages))
        return redirect(url_for('show_question', question_index=next_index))
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

# Function to get the next question index
def get_shuffled_questions():
    all_messages = phishing_messages + legitimate_messages
    random.shuffle(all_messages)
    return all_messages

# Function to get the next question index
def get_next_question_index(current_index, total_questions):
    # Increment the index, and if it exceeds the total number of questions, reset it to 1
    next_index = current_index + 1 if current_index < total_questions else 1
    return next_index

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is submitted, redirect to the first question
        name = request.form.get('name')
        questions = get_shuffled_questions()
        session['shown_questions'] = []  # Initialize an empty list to track shown questions
        return render_template('questions.html', question_index=1, name=name, questions=questions)
    else:
        return render_template('enter_name.html', phishing_messages=phishing_messages)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    if request.method == 'POST':
        return process_answers()
    else:
        # Get all questions without shuffling
        questions = phishing_messages + legitimate_messages

        # Check if there are more questions to show
        if 1 <= question_index <= len(questions):
            # Display the question based on the index
            message = questions[question_index - 1]

            # Keep track of shown questions in the session
            shown_questions = session.get('shown_questions', [])

            # Check if the same question was shown last time
            if shown_questions and shown_questions[-1] == message['label']:
                # If the same question was shown, get the next question index
                next_index = get_next_question_index(question_index, len(questions))
                return redirect(url_for('show_question', question_index=next_index))

            shown_questions.append(message['label'])
            session['shown_questions'] = shown_questions

            name = request.args.get('name')
            return render_template('questions.html', question_index=question_index + 1, name=name, message=message)
        else:
            # Redirect to the next page (e.g., result page) after showing all questions
            return redirect(url_for('result_page'))

if __name__ == '__main__':
    app.run(debug=False)

# Close the database connection
conn = get_db()
if conn is not None:
    conn.close()

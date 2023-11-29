from flask import Flask, render_template, g, request, url_for, redirect, session
from database import get_db, init_db, close_db
from quiz_functions import process_answers, display_leaderboard, get_next_question_index

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATABASE = 'phishing_challenge.db'

# Initialize the database
init_db(app)

# Phishing and legitimate messages with images
phishing_messages = [
    {"label": "Phishing Image 1", "image": "phishing_image_1.jpg"},
    {"label": "Phishing Image 2", "image": "phishing_image_2.jpg"},
    # Add more phishing messages as needed
]

legitimate_messages = [
    {"label": "Legitimate Image 1", "image": "legitimate_image_1.jpg"},
    {"label": "Legitimate Image 2", "image": "legitimate_image_2.jpg"},
    # Add more legitimate messages as needed
]

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is submitted, redirect to the first question
        name = request.form.get('name')
        questions = phishing_messages + legitimate_messages  # Combine all questions without shuffling
        session['shown_questions'] = []  # Initialize an empty list to track shown questions
        return render_template('questions.html', question_index=1, name=name, questions=questions)
    else:
        return render_template('enter_name.html', phishing_messages=phishing_messages)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    if request.method == 'POST':
        return process_answers(request, session, phishing_messages, legitimate_messages)
    else:
        # Get all questions without shuffling
        questions = phishing_messages + legitimate_messages

        # Check if there are more questions to show
        if 0 <= question_index <= len(questions):
            # Display the question based on the index
            message = questions[question_index - 1]

            # Keep track of shown questions in the session
            shown_questions = session.get('shown_questions', [])

            # Check if the same question was shown last time
            #if shown_questions and shown_questions[-1] == message['label']:
                # If the same question was shown, get the next question index
               # next_index = get_next_question_index(question_index, len(questions))
               # return redirect(url_for('show_question', question_index=next_index))

            shown_questions.append(message['label'])
            session['shown_questions'] = shown_questions

            name = request.args.get('name')
            return render_template('questions.html', question_index=question_index, name=name, message=message, questions=questions)
        else:
            # Redirect to the next page (e.g., result page) after showing all questions
            return redirect(url_for('result_page'))

if __name__ == '__main__':
    app.run(debug=False)

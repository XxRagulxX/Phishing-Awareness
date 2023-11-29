from database import get_db

from flask import Flask, render_template, g, request, url_for, redirect, session

def process_answers(request, session, phishing_messages, legitimate_messages):
    name = request.form.get('name')

    # Check if 'question_index' is in the form
    question_index = int(request.form.get('question_index', 0))  # Adjust the starting index to 1

    # Combine both phishing and legitimate messages into one list
    all_messages = phishing_messages + legitimate_messages

    user_input = request.form.get('answer')  # Adjust the index to match the current question

    # Check if the user's answer is correct
    if user_input == 'phishing':
        score = 1
    elif user_input == 'legitimate':
        score = 1
    else:
        score = 0

    # Get the current total score from the database
    cursor = get_db().cursor()
    cursor.execute('SELECT total_score FROM users WHERE name = ?', (name,))
    current_total_score = cursor.fetchone()

    if current_total_score is not None:
        # Update the total score by adding the score for the current question
        total_score = current_total_score[0] + score
    else:
        # If the user is not in the database, initialize the total score
        total_score = score

    # Try to insert a new record, ignore if the user already exists
    cursor.execute('INSERT OR IGNORE INTO users (name, score, total_score) VALUES (?, ?, ?)',
                   (name, score, total_score))

    # Update the user's score in the database
    cursor.execute('UPDATE users SET score = score + ?, total_score = total_score + ? WHERE name = ?',
                   (score, total_score, name))

    get_db().commit()

    if question_index < len(all_messages):
        # If there are more questions, redirect to the next question
        next_index = get_next_question_index(question_index, len(all_messages))
        return redirect(url_for('show_question', score=score, name=name, question_index=next_index))
    else:
        # Display the leaderboard if all questions are answered
        leaderboard = display_leaderboard()
        return render_template('result.html', name=name, score=score, leaderboard=leaderboard)



def display_leaderboard():
    cursor = get_db().cursor()
    cursor.execute('SELECT name, score FROM users ORDER BY score DESC LIMIT 3')
    leaderboard = cursor.fetchall()
    return leaderboard

def get_next_question_index(current_index, total_questions):
    # Increment the index, and if it exceeds the total number of questions, reset it to 1
    next_index = current_index + 1 if current_index < total_questions else 1
    return next_index
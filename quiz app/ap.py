

from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = 'your_secret_key'
valid_secret_codes = {"candidate1@example.com": "secretkey1", "candidate2@example.com": "secretkey2"}

questions = {
    "What is the output of '2+2' in Python?": ["a. 4", "b. 3", "c. 2", "d. 5"],
    "Which of the following is an immutable data type in Python?": ["a. List", "b. Dictionary", "c. Tuple", "d. Set"],
    "What is the keyword used to define a function in Python?": ["a. define", "b. function", "c. def", "d. func"],
}

answers = {
    "What is the output of '2+2' in Python?": "a",
    "Which of the following is an immutable data type in Python?": "c",
    "What is the keyword used to define a function in Python?": "c",
}
participants = []
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':  
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['secret_code'] = request.form['secret_code']      
        email = session['email']
        secret_code = session['secret_code']
        print(secret_code)
        if email not in valid_secret_codes or valid_secret_codes[email] != secret_code:
            print("invalid")
            return "Invalid secret key"
        # Prevent multiple submissions
        if email in participants:
            print("already submitted")
            return "You have already submitted your quiz."
        
        session['start_time'] = datetime.now(timezone.utc)
        session['score'] = 0
        session['answers'] = {}
        return redirect('/questions/1')  # Start with question 1
    return render_template('quiz.html')




#trying
@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def quiz_questions(question_number):
    if request.method == 'POST':
        session['answers'][str(question_number)] = request.form['answer']  # Convert question_number to string for consistency

        # Check if the answer is correct and update the score
        if answers.get(list(questions.keys())[question_number - 1]) == request.form['answer']:
            session['score'] += 1

        # Redirect to the next question or result page
        if question_number == len(questions):
            return redirect('/result')
        else:
            return redirect(f'/questions/{question_number + 1}')

    question = list(questions.keys())[question_number - 1]
    options = questions[question]
    return render_template('questions.html', question_number=question_number, question=question, options=options)






@app.route('/result')
def quiz_result():
   # score = request.args.get('score')  # Retrieve score from redirect
    try:
        score = int(session.get('score'))
        end_time = datetime.now(timezone.utc)
        elapsed_time = end_time - session['start_time']

        participant_info = {
            'name': session['name'],
            'email': session['email'],
            'score': score,
            'elapsed_time': elapsed_time,
        }
        participants.append(participant_info)
    except:
        print('error special in result')
    return render_template('result.html', name=session['name'], email=session['email'], score=score, elapsed_time=elapsed_time)

# @app.route('/quiz', methods=['GET', 'POST'])
# def quiz():
#     if request.method == 'POST':
#         session['name'] = request.form['name']
#         session['email'] = request.form['email']
#         session['start_time'] = datetime.now(timezone.utc)
#         session['answers'] = {}
#         return redirect('/questions/1')
#     return render_template('quiz.html')

# @app.route('/questions', methods=['GET', 'POST'])
# def quiz_questions2():
#     if request.method == 'POST':
#         session['answers'].update(request.form)
#         return redirect('/result')

#     question = list(questions.keys())[len(session['answers'])]
#     options = questions[question]
#     return render_template('questions.html', question=question, options=options)

# @app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
# def quiz_questions(question_number):
#     if request.method == 'POST':
#         session['answers'][question_number] = request.form['answer']
#         if question_number == len(questions): 
#             return redirect('/result')
#         else:
#             return redirect(f'/questions/{question_number + 1}')

#     question = list(questions.keys())[question_number - 1]
#     options = questions[question]
#     return render_template('questions.html', question=question, options=options)



# @app.route('/result')
# def quiz_result():
#     score = 0
#     for question, answer in session['answers'].items():
#         if answers.get(question) == answer:
#             score += 1

#     end_time = datetime.now(timezone.utc)
#     #elapsed_time = end_time - session['start_time']
#     elapsed_time = end_time
#     participant_info = {
#         'name': session['name'],
#         'email': session['email'],
#         'score': score,
#         'elapsed_time': elapsed_time,
#     }
#     participants.append(participant_info)
#     return render_template('result.html', name=session['name'], email=session['email'], score=score, elapsed_time=elapsed_time)
@app.route('/leaderboard')
def leaderboard():
    ranked_participants = sorted(participants, key=lambda x: (x['score'], x['elapsed_time'], x['name']))
    return render_template('leaderboard.html', participants=ranked_participants[::-1])


if __name__ == '__main__':
    app.run(debug=True,host='172.16.1.190')

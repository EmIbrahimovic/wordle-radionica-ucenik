import random
from flask import Flask, request, jsonify, session, render_template

# 1. THE APP: We initialize the Flask application here.
app = Flask(__name__)

# Secret key is required to store the target word in the user's browser session.
app.secret_key = 'high_school_wordle_secret'

# 2. THE DICTIONARY: A simple list of 20 4-letter words for our game.
DICTIONARY = [
    'GOLD', 'BLUE', 'FIRE', 'WIND', 'ROCK', 'STAR', 'MOON', 'TREE', 
    'BIRD', 'FISH', 'PARK', 'CAKE', 'BAKE', 'READ', 'CODE', 'GAME', 
    'SHIP', 'LOVE', 'HOPE', 'KIND'
]

def check_guess(target, guess):
    """
    TEACHING MOMENT: This function compares the guess to the secret word.
    It returns a list of results (correct, present, or absent) for each letter.
    """
    result = [{'letter': char, 'status': 'absent'} for char in guess]
    target_list = list(target)
    
    # First pass: Mark letters in the correct position (Green)
    for i in range(4):
        if guess[i] == target[i]:
            result[i]['status'] = 'correct'
            target_list[i] = None
            
    # Second pass: Mark letters that exist but are in the wrong spot (Yellow)
    for i in range(4):
        if result[i]['status'] == 'correct':
            continue
        if guess[i] in target_list:
            result[i]['status'] = 'present'
            target_list[target_list.index(guess[i])] = None
            
    return result

@app.route("/")
def hello_world():
    """
    TEACHING MOMENT: This is our main route. We name the function 'hello_world' 
    per your request and pass a 'title' variable to be used in the HTML.
    """
    if 'target' not in session:
        session['target'] = random.choice(DICTIONARY)
    return render_template("index.html", title="Wordle-4 Lite")

@app.route('/check', methods=['POST'])
def check():
    """Receives a guess and returns how many letters were right."""
    data = request.get_json()
    guess = data.get('guess', '').upper()
    
    # TEACHING MOMENT: Validation. 
    # Before checking the colors, we must ensure the word is actually in our allowed list.
    if guess not in DICTIONARY:
        return jsonify({'error': 'Not in word list'}), 400
        
    target = session.get('target', 'GOLD')
    results = check_guess(target, guess)
    
    return jsonify({
        'results': results,
        'won': guess == target,
        'target': target
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Starts a new game by clearing the old word."""
    session['target'] = random.choice(DICTIONARY)
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(debug=True)

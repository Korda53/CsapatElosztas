from flask import Flask, render_template, request, jsonify
from Scripts import database

app = Flask(__name__)

# Dummy data for checkboxes
checkbox_options = []

@app.route('/', methods=['GET','POST'])
def home():
    checkbox_options = database.get_players_from_database()
    return render_template('index.html', options=checkbox_options)

@app.route('/submit', methods=['POST'])
def submit():
    selected_options = request.form.getlist('options')

    database.availablePlayers = []

    if 'split' in request.form:
        for options in selected_options:
            player=database.get_player_attributes(options)
            database.createPlayer(player)

        teams = database.splitTeams(database.availablePlayers)
        print(database.countAverages(teams))

        return jsonify(database.availablePlayers, teams)

    elif 'remove' in request.form:
        for players in selected_options:
            database.remove_player(players)

    return(home())
    #checkbox_options = database.get_players_from_database()
    #return render_template('index.html', options=checkbox_options)

@app.route('/add', methods=['POST'])
def addPlayer():
    playerAttributes = []
    for key, value in request.form.items():
        if isinstance(value, str):
            playerAttributes.append(value)
        else:
            continue
    print(playerAttributes)
    database.addPlayerToDatabase(playerAttributes[:5])

    return(home())
    #checkbox_options = database.get_players_from_database()
    #return render_template('index.html', options=checkbox_options)

if __name__ == '__main__':
    app.run(debug=True)

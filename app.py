from flask import Flask, render_template, request, redirect, url_for, jsonify
import xml.etree.ElementTree as ET
import random

app = Flask(__name__)

# Load players from XML
def load_players():
    tree = ET.parse('players.xml')
    root = tree.getroot()
    players = []
    for player in root.findall('player'):
        name = player.find('name').text
        defence = int(player.find('defence').text)
        attack = int(player.find('attack').text)
        skill = int(player.find('skill').text)
        stamina = int(player.find('stamina').text)
        players.append({
            'name': name,
            'defence': defence,
            'attack': attack,
            'skill': skill,
            'stamina': stamina
        })
    return players

# Save players to XML
def save_players(players):
    root = ET.Element("players")
    for player in players:
        player_elem = ET.SubElement(root, "player")
        ET.SubElement(player_elem, "name").text = player['name']
        ET.SubElement(player_elem, "defence").text = str(player['defence'])
        ET.SubElement(player_elem, "attack").text = str(player['attack'])
        ET.SubElement(player_elem, "skill").text = str(player['skill'])
        ET.SubElement(player_elem, "stamina").text = str(player['stamina'])
    
    tree = ET.ElementTree(root)
    tree.write('players.xml')

@app.route('/', methods=['GET', 'POST'])
def index():
    players = load_players()
    if request.method == 'POST':
        selected_players = request.form.getlist('players')
        selected_players_data = [p for p in players if p['name'] in selected_players]
        teams = divide_teams(selected_players_data)
        return render_template('index.html', players=players, teams=teams)
    return render_template('index.html', players=players)

def divide_teams(selected_players):
    difference = 100
    teams = []
    
    for i in range(50):
        current_teams = divide_teams_iteration(selected_players)
        if(abs(current_teams[2]-current_teams[3])<difference):
             difference=abs(current_teams[2]-current_teams[3])
             teams=current_teams
        i+=1


    return teams

def divide_teams_iteration(selected_players):
    team_black = []
    team_white = []
    team_black_score=0
    team_white_score=0

    # Shuffle the list to ensure random distribution
    random.shuffle(selected_players)
    
    # Calculate the split point
    split_index = (len(selected_players) + 1) // 2  # Use +1 to favor the first team in case of odd count
    
    # Divide into two teams
    team_black = selected_players[:split_index]
    team_white = selected_players[split_index:]

    for player in team_black:
            player['score'] = sum([player['defence'], player['attack'], player['skill'], player['stamina']])
            team_black_score+=player['score']
  
    for player in team_white:
            player['score'] = sum([player['defence'], player['attack'], player['skill'], player['stamina']])
            team_white_score+=player['score']

    return team_black, team_white, team_black_score, team_white_score

def compare_teams(team_black_score, team_white_score):
     difference = abs(team_white_score-team_black_score)
     return difference     

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    defence = int(request.form['defence'])
    attack = int(request.form['attack'])
    skill = int(request.form['skill'])
    stamina = int(request.form['stamina'])
    
    players = load_players()
    
    # Check if the player already exists
    for player in players:
        if player['name'] == name:
            # Update existing player's values
            player['defence'] = defence
            player['attack'] = attack
            player['skill'] = skill
            player['stamina'] = stamina
            break
    else:
        # Add new player if not found
        players.append({'name': name, 'defence': defence, 'attack': attack, 'skill': skill, 'stamina': stamina})
    
    # Save the updated list of players back to XML
    save_players(players)
        
    return redirect(url_for('index'))

@app.route('/delete_player', methods=['POST'])
def delete_player():
    selected_players = request.form.getlist('delete_players')
    players = load_players()
    players = [p for p in players if p['name'] not in selected_players]
    save_players(players)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
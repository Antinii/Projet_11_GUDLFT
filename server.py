import json
from flask import Flask, render_template, request, redirect, flash, url_for

from datetime import datetime


def loadClubs():
    with open('clubs.json') as club:
        listOfClubs = json.load(club)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

current_date = datetime.now()
@app.template_filter("string_to_date")
def string_to_date(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        return render_template("welcome.html", club=club[0], competitions=competitions, current_date=current_date)
    else:
        return render_template("index.html", error="Email not found, please try again.")


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong, please try again")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    clubPoints = int(club["points"])
    placesRequired = int(request.form['places'])
    maxPlacesAllowed = 12
    maxPlacesAllowedMessage = f"Sorry! You can't book more then {maxPlacesAllowed} places."
    competitionPlaces = int(competition['numberOfPlaces'])

    if placesRequired > maxPlacesAllowed: # check if the number of places booked is not exceeding 12 per competition.
        return render_template('booking.html', club=club, competition=competition,
                               maxPlacesAllowedMessage=maxPlacesAllowedMessage)
    
    if clubPoints < placesRequired: # check if the number of placesRequired does not exceed point balance.
        flash("Your point balance is not enough.")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    if competitionPlaces < placesRequired: # check if the number of placesRequired does not exceed the competition places left.
        flash("Not enough places available for the quantity you requested.")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    if placesRequired <= 0: # check if placesRequired is higher then 0.
        flash('Incorrect value.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    
    club['points'] = int(club['points']) - placesRequired 
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great, booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


@app.route('/displayboard')
def display_board():
    points_table = [{'name': club['name'], 'points': club['points']} for club in clubs]
    return render_template('points_board.html', points_table=points_table)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

import json
from flask import Flask, render_template, request, redirect, flash, url_for

from datetime import datetime


def loadClubs():
    """
    Function to load clubs data from JSON file.

    Returns:
        List: List of clubs.
    """
    with open('clubs.json') as club:
        listOfClubs = json.load(club)['clubs']
        return listOfClubs


def loadCompetitions():
    """
    Function to load competitions data from JSON file.

    Returns:
        list: List of competitions.
    """
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
    """
    Flask template filter to convert string to date.

    Args:
        value (str): String representing a date.

    Returns:
        datetime: Datetime object.
    """
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    """
    Route for the index page.
    """
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Route to display summary.
    """
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        return render_template("welcome.html", club=club[0], competitions=competitions, current_date=current_date)
    else:
        return render_template("index.html", error="Email not found, please try again.")


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Route to book a competition.
    """
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])
    else:
        flash("Something went wrong, please try again")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Route to purchase places.
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    clubPoints = int(club["points"])
    placesRequired = int(request.form['places'])
    maxPlacesAllowed = 12
    maxPlacesAllowedMessage = f"Sorry! You can't book more then {maxPlacesAllowed} places."
    competitionPlaces = int(competition['numberOfPlaces'])

    if placesRequired > maxPlacesAllowed:  # check if the number of places booked is not exceeding 12 per competition.
        return render_template('booking.html', club=club, competition=competition,
                               maxPlacesAllowedMessage=maxPlacesAllowedMessage)

    if clubPoints < placesRequired:  # check if the number of placesRequired does not exceed point balance.
        flash("Your point balance is not enough.")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    if competitionPlaces < placesRequired:  # check if the number of placesRequired does not exceed the places left.
        flash("Not enough places available for the quantity you requested.")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    if placesRequired <= 0:  # check if placesRequired is higher then 0.
        flash('Incorrect value.')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great, booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


@app.route('/displayboard', methods=['GET'])
def display_board():
    """
    Route to display club points board.
    """
    points_table = [{'name': club['name'], 'points': club['points']} for club in clubs]
    return render_template('points_board.html', points_table=points_table)


@app.route('/logout')
def logout():
    """
    Route to log out.
    """
    return redirect(url_for('index'))

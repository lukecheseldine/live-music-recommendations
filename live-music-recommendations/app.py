from datetime import date
from flask import Flask, render_template, request, redirect, session
from requests import post, get
from base64 import urlsafe_b64encode
from flask_session import Session
import calendar

app = Flask(__name__)

# session for storing access_token
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# spotify api credentials
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SPOTIFY_SCOPES = 'user-read-private user-follow-read user-library-read playlist-read-private user-top-read'

# seatgeek api credentials
SEATGEEK_CLIENT_ID = ''
SEATGEEK_CLIENT_SECRET = ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorize', methods=['POST', 'GET'])
def authorize():
    url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={SPOTIFY_SCOPES}'
    return redirect(url)


@app.route('/callback', methods=['GET'])
def callback():
    if request.args.get('error'):
        return 'error'
    else:
        code = request.args.get('code')
        url = f'https://accounts.spotify.com/api/token'
        response = post(url, data={
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }, headers={
            'Authorization': 'Basic ' + (urlsafe_b64encode(str.encode(SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET)).decode()),
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        response_data = response.json()
        access_token = response_data['access_token']
        session['access_token'] = access_token
        return redirect('/recommendation')


@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')


@app.route('/artist', methods=['POST', 'GET'])
def artist():
    return render_template('artist.html')


@app.route('/genre', methods=['POST', 'GET'])
def genre():
    zipcode = request.form.get('zip-code')
    session['zip-code'] = zipcode
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = {
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = get(url, headers=headers)
    genres = response.json()['genres']
    genres = ['hip-hop', 'pop', 'country', 'latin', 'r-n-b', 'dance', 'blues', 'jazz', 'classical']
    return render_template('genre.html', genres=genres)


@app.route('/playlist', methods=['POST', 'GET'])
def playlist():
    return f"{request.form.get('selection')}"


@app.route('/results/genre/<genre>', methods=['POST', 'GET'])
def results(genre):
    url = 'https://api.spotify.com/v1/recommendations'
    params = {
        'seed_genres': str(genre),
        'limit': 5
    }
    headers = {
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = get(url, params=params, headers=headers)
    response_data = response.json()

    artists = set()
    for i in range(len(response_data['tracks'])):
        name = response_data['tracks'][i]['album']['artists'][0]['name']
        if name != 'Various Artists':
            artists.add(name)

    # remove duplicates
    artists = list(artists)

    performer_ids = set()
    # convert spotify artists to seatgeek performer ids
    url = 'https://api.seatgeek.com/2/performers'
    for artist in artists:
        params = {
            'q': artist,
            'client_id': SEATGEEK_CLIENT_ID
        }
        response = get(url, params=params).json()
        for perfomer in response['performers']:
            if perfomer['name'].lower() == artist.lower():
                performer_ids.add(str(perfomer['id']))

    # get recommendations for performers
    query = ''
    for performer_id in performer_ids:
        query += 'performers.id=' + performer_id + '&'
    zipcode = session.get('zip-code')
    url = f'https://api.seatgeek.com/2/recommendations?{query}postal_code={zipcode}&client_id={SEATGEEK_CLIENT_ID}'
    response = get(url).json()['recommendations']

    performances = []
    for event in response:
        event = event['event']
        if event['type'] != 'concert':
            continue
        
        performers = []
        for performer in event['performers']:
            if performer['name'] not in performers:
                performers.append(performer['name'])
        if event['performers'][0]['images']:
            image = event['performers'][0]['images']['huge']
        else:
            image = None
        year = event['datetime_local'][:4]
        month = event['datetime_local'][5:7]
        day = event['datetime_local'][8:10]
        month = calendar.month_name[int(month)]
        date = f'{month} {day}, {year}'

        performance = {
            'perfomers': performers,
            'date': date,
            'venue': event['venue']['name'],
            'image': image,
            'link': event['url']
        }
        performances.append(performance)

    return render_template('results.html', performances=performances)

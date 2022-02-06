from flask import Flask, render_template, request, redirect, session
from requests import post, get
from base64 import urlsafe_b64encode
from flask_session import Session


app = Flask(__name__)

# session for storing access_token
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# spotify api credentials
SPOTIFY_CLIENT_ID = '6151954dbc3842b98c6f8bbab8616310'
SPOTIFY_CLIENT_SECRET = '43e0561d85b944de8c6e9059d9a8a7f1'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SPOTIFY_SCOPES = 'user-read-private user-follow-read user-library-read playlist-read-private user-top-read'

# seatgeek api credentials
SEATGEEK_CLIENT_ID = 'MjU2MTgyNzV8MTY0NDExNzE3OS4yNjMwMjk'
SEATGEEK_CLIENT_SECRET = '8b866a86d6e0a65707b99864a3913c51b75431e62261c2f814611abce7c6f5b0'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorize', methods = ['POST', 'GET'])
def authorize():
    url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={SPOTIFY_SCOPES}'
    return redirect(url)
    

@app.route('/callback', methods=['GET'])
def callback():
    # TODO: Handle invalid login credentials/error, whenever this happens
    if request.args.get('error'):
        return 'error'
    else:
        code = request.args.get('code')
        url = f'https://accounts.spotify.com/api/token'
        response = post(url, data={
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }, headers={ \
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
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = {
        'Authorization': f'Bearer {session.get("access_token")}'
    }
    response = get(url, headers=headers)
    genres = response.json()['genres']
    return render_template('genre.html', genres=genres)


@app.route('/playlist', methods=['POST', 'GET'])
def playlist():
    return f"{request.form.get('selection')}"

@app.route('/results/genre/<genre>', methods=['POST', 'GET'])
def results(genre):
    url = 'https://api.spotify.com/v1/recommendations'
    params = {
        'seed_genres': str(genre),
        'limit': 50
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

    url = 
    


    return f"{artists} {len(artists)}"

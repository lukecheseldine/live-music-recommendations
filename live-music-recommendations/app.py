from flask import Flask, render_template, request, redirect
from requests import post
from base64 import urlsafe_b64encode


app = Flask(__name__)
# spotify api credentials
CLIENT_ID = '6151954dbc3842b98c6f8bbab8616310'
CLIENT_SECRET = '43e0561d85b944de8c6e9059d9a8a7f1'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPES = 'user-read-private user-follow-read user-library-read playlist-read-private user-top-read'



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorize', methods = ['POST'])
def authorize():
    url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}'
    print(url)
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
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }, headers={ \
            'Authorization': 'Basic ' + (urlsafe_b64encode(str.encode(CLIENT_ID + ':' + CLIENT_SECRET)).decode()),
            'Content-Type': 'application/x-www-form-urlencoded'
        }) 
        return redirect('/recommendation')

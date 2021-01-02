from flask import Flask, redirect, request
from urllib.parse import urlencode
from random import choice
from string import ascii_uppercase, digits
from flask_cors import CORS
from base64 import b64encode
import requests
import os

app = Flask(__name__)
CORS(app)
client_secret = os.environ.get('CLIENT_SECRET')
client_id = os.environ.get('CLIENT_ID')
redirect_uri = 'http://localhost:5000/callback/'
access_token = None

@app.route('/')
def hello_world():
    return 'Hello World!'

# from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

@app.route('/login/')
def login():
    authorize_dict = {
      'response_type': 'code',
      'client_id': client_id,
      'scope': 'user-read-private user-read-email user-modify-playback-state user-read-playback-state',
      'redirect_uri': redirect_uri,
      'state': id_generator(12)
    }
    params = urlencode(authorize_dict)
    url = 'https://accounts.spotify.com/authorize?%s' % params
    return redirect(url)

@app.route('/callback/<any:code>')
def getTokens(code):
    auth_data = {
      'code': request.args.to_dict()['code'],
      'redirect_uri': redirect_uri,
      'grant_type': 'authorization_code'
    }
    header = {
      'Authorization': 'Basic ' + b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    }
    res = requests.post('https://accounts.spotify.com/api/token',headers=header, data=auth_data)
    access_token = res.json()['access_token'] 
    print(f'access_token {access_token}')

    authenticated_header = {
       'Authorization': 'Bearer ' + access_token,
       'Accept': 'application/json',
       'Content-Type': 'application/json'
    }
    # get device
    devices = requests.get('https://api.spotify.com/v1/me/player/devices', headers=authenticated_header).json()
    # get first device -> but can select device later.
    device_id = devices['devices'][0]['id']
    print(f'device_id {device_id}')
    # search for playlist
    search_params = {
      'q': 'doja cat',
      'type': 'playlist'
    }
    playlist_url = 'https://api.spotify.com/v1/search?%s' % urlencode(search_params)
    print(f'playlist_url {playlist_url}')
    playlists = requests.get(playlist_url, headers=authenticated_header).json()
    
    playlist_id = playlists['playlists']['items'][0]['id']
    print(f'playlist_id {playlist_id}')
    # play playlist
    request_body = {
      "context_uri": f"spotify:playlist:{playlist_id}"
    }
    play_url = f'https://api.spotify.com/v1/me/player/play?device_id={device_id}'
    play_response = requests.put(play_url, json=request_body, headers=authenticated_header)
    return f'{play_response.status_code}'

#http://localhost:5000/login
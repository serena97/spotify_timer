from flask import (
    Response, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from urllib.parse import urlencode
from random import choice
from string import ascii_uppercase, digits
from flask_cors import CORS
from base64 import b64encode
import requests
import os
from flask import current_app

bp = Blueprint('auth', __name__, url_prefix='/auth')

access_token = ''

def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

@bp.route('/login')
def login():
    authorize_dict = {
      'response_type': 'code',
      'client_id': current_app.config['CLIENT_ID'],
      'scope': 'user-read-private user-read-email user-modify-playback-state user-read-playback-state',
      'redirect_uri': current_app.config['REDIRECT_URL'],
      'state': id_generator(12)
    }
    params = urlencode(authorize_dict)
    url = 'https://accounts.spotify.com/authorize?%s' % params
    return redirect(url)

@bp.route('/callback/<any:code>')
def getTokens(code):
    auth_data = {
      'code': request.args.to_dict()['code'],
      'redirect_uri': current_app.config['REDIRECT_URL'],
      'grant_type': 'authorization_code'
    }
    header = {
      'Authorization': 'Basic ' + b64encode(bytes(current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET'], 'utf-8')).decode('utf-8')
    }
    res = requests.post('https://accounts.spotify.com/api/token',headers=header, data=auth_data)
    global access_token
    access_token = res.json()['access_token'] 
    return render_template('auth/login.html', access_token=access_token)

@bp.route('/search/<query>')
def search(query):
    print(query)
    search_params = {
      'q': query,
      'type': 'playlist', 
      'limit': 10
    }
    authenticated_header = {
      'Authorization': 'Bearer ' + access_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    playlist_url = 'https://api.spotify.com/v1/search?%s' % urlencode(search_params)
    print(f'playlist_url {playlist_url}')
    playlists = requests.get(playlist_url, headers=authenticated_header).json()
    ret = []
    for item in playlists['playlists']['items']:
      name = item['name']
      ret.append(name)
    
    return jsonify(ret)

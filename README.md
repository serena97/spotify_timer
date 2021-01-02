Flask / Python webapp to play spotify playlists within timer

0. auth

1. get a playlist / album
GET https://api.spotify.com/v1/search -> id 
https://developer.spotify.com/console/get-search-item/

2. start playing tracks in spotify 
PUT https://api.spotify.com/v1/me/player/play
device_id: a7ee5ca90fb9020ed706a9d37df9905d3fc7fa5a 
https://developer.spotify.com/console/get-users-available-devices/

{
  "context_uri": "spotify:playlist:5aL9jeGMCA7uiH8MviKDSQ",
  "offset": {
    "position": 0
  },
  "position_ms": 0
}
https://developer.spotify.com/console/put-play/

3. After 25 mins pause, add alarm. start 5 min time, once time is up then start playing tracks again 
https://developer.spotify.com/console/put-pause/

4. Expand for this to play youtube tracks -> instead of embedding, can open youtube with new tab and then close tab after 25 mins 
https://developers.google.com/youtube/v3/docs/search/list#usage -> to get videoid ?v 
https://www.youtube.com/watch?v=bmVKaAV_7-A
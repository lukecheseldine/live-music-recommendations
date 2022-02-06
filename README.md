# SoundSearch
### Mission Statement
Due to the pandemic, many of us have not been able to go to concerts and live shows like we used to in the past. SoundSearch aims to restore our pre-pandemic concert-going ways by reconnecting its users to the live music scene!

![SoundSearch landing page](./live-music-recommendations/static/readme-index.png "SoundSearch landing page")

### Functionality
SoundSearch allows users to input a musical genre and location. It then returns a listing of concerts within that genre near the location specified. The website also links with a user's Spotify account, so additional functionality for providing recommendations based on a user's followed artists, liked songs, or playlists has strong foundations.

### Technology
SoundSearch is built with Flask, Bootstrap, and CSS/HTML/JS. On the backend, we perform OAuth authentication and API calls to the Spotify API, as well as API-key authentication and calls to the SeatGeek API in order to get all of our data in realtime. 

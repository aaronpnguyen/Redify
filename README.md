# Redify

A Reddit clone that utilizes Spotify's API, Python, Flask, SQL, HTML/CSS, and JavaScript.

# *NOTICE*

Because Redify is a small-scale project, users must contact either Aaron Nguyen or Corbin Crawford to have full access.

This is due to Spotify's strict API rules.

To contact, see below.

## Purpose

For most people, finding new music that they're able to enjoy is rough. Sometimes they may find themselves scavenging through an endless rabbit hole of different songs that they might not even find enjoyable to listen to. However, there are places such as Reddit that allows users the ability to find niche communities that share similar music tastes. This is where Redify comes in. Redify is a Reddit clone that utilizes Spotify's API and embeds to help users with this specific problem.

## Features

- Create account(s)
  - Able to change e-mail and password
  - Able to log-out of Spotify, removing Redify's access to the user's Spotify account
- Create topics
  - Able to favorite/unfavorite a topic
  - Able to browse and see a topic's active user count
- Create posts
  - Able to embed Spotify links
  - Able to create comments while also being able to embed Spotify links
- Retrieve Spotify stats (past month, past 3 months, and life-time)
- Store life-time stats on user profile for display
- Light/dark mode switch

## Credits

This project was done in collaboration by Aaron Nguyen and Corbin Crawford.
- Aaron was in charge of the backend, creating SQL queries, supplying data from Flask's back-end to the front-end, and utilizing/scraping Spotify's API.
  - https://www.linkedin.com/in/aaronpnguyen/
  - Discord: Aaronn#0002

- Corbin was in charge of the frontend, styling each page, giving the project a mordern feel/look, and adding quality of life features such as a light/dark mode switch for users.
  - https://www.linkedin.com/in/corbin-crawford/
  - Discord: CorbinC#6566
  
### Languages/Frameworks/Packages

Languages:
  - Python
  - HTML/CSS
  - JavaScript
  - SQL

Frameworks:
  - Flask

Packages:
  - Bcrypt
  - Spotipy
  - Jinja2
  - python-dotenv
  - PyMySQL

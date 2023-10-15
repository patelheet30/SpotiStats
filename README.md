# SPOTIFY STATS

## What is this?
This is a Python Webapp that uses the Spotify Data provided to you
to create a simple stats page for your Spotify account. It will show you
your top artists, top tracks, and top genres. It will also show you your
top tracks and artists for each year.

## How do I request my data from Spotify?
1. Go to [Spotify's Privacy Settings](https://www.spotify.com/us/account/privacy/)
2. Scroll down to "Download your data" and click "Request" for Account Data and Extended Streaming History
3. Wait for Spotify to send you an email with a download link
4. Download the data and upload it to the website

## How do I run this locally?
In order to utilise this repo, you also need to create a spotify developer account. Once you've done that
you should be able to go to the dashboard and then create a new app.

Open the new app and then click on `Settings`. In Settings get the `Client ID` and `Client Secret`.


1. Clone the repo
2. Install the requirements with `pip install -r requirements.txt`
3. Set the environment variable `APP_SECRET_KEY` located in `.env.example` to a random string/password,
alongside `CLIENT_ID` and `CLIENT_SECRET` to the values you got from the Spotify Developer Dashboard
4. Rename `.env.example` to `.env`
5. Run the script with `flask run` in your terminal.
6. Go to `127.0.0.1:5000` in your browser
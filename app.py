from utils.get_json import get_json
from utils.user_info import get_user_info
from utils.parsers import convert_minutes

from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import logging
import os
import zipfile
import json
import shutil
import tempfile

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SpotifyStats - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    session.pop('data_submitted', None)
    session.pop('user-info', None)
    return render_template('index.html')


@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        uploaded_file = request.files.getlist('json_files')
        json_data_list = {}

        for file in uploaded_file:
            logger.info(f"Processing file: {file.filename}")
            if '.json' in file.filename:
                file_content = json.loads(file.read().decode('utf-8'))
                json_data_list[file.filename] = file_content
                logger.info(f"Name of File: {file.filename}")
            elif '.zip' in file.filename:
                filename = secure_filename(file.filename)
                file.save(filename)
                with tempfile.TemporaryDirectory() as tempdir:
                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall(path=tempdir)
                        extracted_files = zip_ref.namelist()
                        for json_file in extracted_files:
                            if '.json' in json_file and not json_file.startswith('__MACOSX'):
                                with open(
                                        os.path.join(tempdir, json_file), 'r', encoding='utf-8'
                                        ) as jf:  # change is here
                                    try:
                                        file_content = json.loads(jf.read())
                                        json_data_list[json_file] = file_content
                                        logger.info(f"Processing File: {json_file}")
                                    except UnicodeDecodeError:
                                        logger.error(f"UnicodeDecodeError processing file: {json_file}")
                                    except json.JSONDecodeError:
                                        logger.error(f"JSONDecodeError processing file: {json_file}")
                            elif json_file.startswith('__MACOSX'):
                                logger.info(f"Skipping file: {json_file}")

                logger.info(f"Removing file: {filename}")
                os.remove(filename)

                for extracted_file in extracted_files:
                    if os.path.isfile(extracted_file):
                        logger.info(f"Removing file: {extracted_file}")
                        os.remove(extracted_file)
                    elif os.path.isdir(extracted_file):
                        logger.info(f"Removing directory: {extracted_file}")
                        shutil.rmtree(extracted_file)

        session['user-info'] = get_json(json_data_list)

        session['data_submitted'] = True

        return jsonify({'success': True})

    except BadRequest as e:
        logger.error(f"Bad request: {str(e)}")
        return jsonify({'message': 'Bad request'})
    except IOError as e:
        logger.error(f"IOError: {str(e)}")
        return jsonify({'message': 'Error processing file'})
    except Exception as e:
        logger.error(f"Generic exception: {str(e)}")
        return jsonify({'message': "Generic exception"})


@app.route('/success_page')
def success_page():
    try:
        if 'data_submitted' not in session:
            return redirect(url_for('hello_world'))
        return render_template('success.html', user=get_user_info(session['user-info'][0]))
    except Exception as e:
        print(e)
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'message': "Error processing file"})


@app.route('/get_content', methods=['POST'])
def get_content():
    content_type = request.json.get('content_type', '')
    if content_type not in ['artists', 'albums']:
        return jsonify({'Error': 'Invalid value for content_type'}), 400

    num_items = request.json.get('num_items', '')
    if not num_items.isnumeric() or int(num_items) <= 0:
        return jsonify({'Error': 'Invalid value for num_items'}), 400

    num_items = int(num_items)
    all_the_songs = session['user-info'][1]
    duration_dict = {}

    if content_type == 'artists':
        for song in all_the_songs:
            if song.artist in duration_dict:
                duration_dict[song.artist]['duration'] += int(song.duration) / 60000
                duration_dict[song.artist]['count'] += 1
            else:
                duration_dict[song.artist] = {'duration': int(song.duration) / 60000, 'count': 1}

        top_items_by_duration = sorted(duration_dict.items(), key=lambda item: item[1]['duration'], reverse=True)[
                                :num_items]
        top_items_by_duration_rounded = [(item, convert_minutes(data['duration']), data['count']) for item, data in
                                         top_items_by_duration]

        top_items_with_images = []
        for item in top_items_by_duration_rounded:
            results = sp.search(q=item[0], type='artist')
            if results['artists']['items']:
                item_id = results['artists']['items'][0]['id']
                item_info = sp.artist(item_id)
                if item_info['images']:
                    item_image = item_info['images'][0]['url']
                    item_url = item_info['external_urls']['spotify']
                    top_items_with_images.append((item[0], item[1], item[2], item_image, item_url))
                else:
                    top_items_with_images.append((item[0], item[1], item[2], '', ''))

    else:
        for song in all_the_songs:
            if song.album in duration_dict:
                duration_dict[song.album]['duration'] += int(song.duration) / 60000
                duration_dict[song.album]['count'] += 1
            else:
                duration_dict[song.album] = {'duration': int(song.duration) / 60000, 'count': 1}

        top_items_by_duration = sorted(duration_dict.items(), key=lambda item: item[1]['duration'], reverse=True)[
                                :num_items]
        top_items_by_duration_rounded = [(item, convert_minutes(data['duration']), data['count']) for item, data in
                                         top_items_by_duration]

        top_items_with_images = []
        for item in top_items_by_duration_rounded:
            results = sp.search(q=item[0], type='album')
            if results['albums']['items']:
                item_id = results['albums']['items'][0]['id']
                item_info = sp.album(item_id)
                if item_info['images']:
                    item_image = item_info['images'][0]['url']
                    item_url = item_info['external_urls']['spotify']
                    top_items_with_images.append((item[0], item[1], item[2], item_image, item_url))
                else:
                    top_items_with_images.append((item[0], item[1], item[2], '', ''))

    return render_template('items.html', items=top_items_with_images)


@app.route('/get_the_info', methods=['POST'])
def handle_click():
    click_info = request.json['click_info']

    return render_template('rightContainer.html', items=click_info)


@app.route('/songs')
def songs():
    songs_to_get = [song.to_dict() for song in session['user-info'][1]]
    return jsonify(songs_to_get)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()

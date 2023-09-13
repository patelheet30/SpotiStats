from utils.get_json import get_json

from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.exceptions import BadRequest

import logging

app = Flask(__name__)
app.secret_key = 'some_secret_key'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SpotifyStats - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    print(session)
    session.pop('data_submitted', None)
    print(session)
    return render_template('index.html')


@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        uploaded_file = request.files.getlist('json_files')
        json_data_list = []

        for file in uploaded_file:
            logger.info(f"Processing file: {file.filename}")

            json_data_list.append(uploaded_file)

        get_json(json_data_list)


        session['data_submitted'] = True
        print(session)

        return jsonify({'success': True})

    except BadRequest as e:
        logger.error(f"Bad request: {str(e)}")
        return jsonify({'message': 'Bad request'})
    except IOError as e:
        logger.error(f"IOError: {str(e)}")
        return jsonify({'message': 'Error processing file'})
    except Exception as e:
        logger.error(f"Generic exception: {str(e)}")
        return jsonify({'message': f"{e}"})


@app.route('/success_page')
def success_page():
    try:
        print(session)
        if 'data_submitted' not in session:
            return redirect(url_for('hello_world'))
        return render_template('success.html')
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'message': f"{e}"})


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run(debug=True)

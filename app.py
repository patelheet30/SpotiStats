from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SpotifyStats - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        uploaded_file = request.files.getlist('json_files')
        for file in uploaded_file:
            logger.info(f"Processing file: {file.filename}")

            json_data = file.read()

        return jsonify({'message': 'File successfully processed'})

    except BadRequest:
        return jsonify({'message': 'Bad request'})
    except IOError:
        return jsonify({'message': 'Error processing file'})
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'message': f"{e}"})


if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, request, jsonify
import requests
import os

create_bp = Blueprint('upload', __name__)

# Set headers for authentication
headers = {"Authorization": f"Bearer {os.environ.get('PINATA_JWT')}"}

@create_bp.route('/upload_file', methods=['POST'])
def upload_file():
    url = "https://uploads.pinata.cloud/v3/files"
    
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        print('FILES0',file.filename)
        # return 'apple'
        
        # Check if a file was actually uploaded
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Prepare additional form data
        name = request.form.get(f'{file.filename}', 'default_name')  # Use a default name if not provided
        data = {'name': file.filename}

        # Make the POST request to upload the file
        response = requests.post(url, files={'file': file}, data=data, headers=headers)

        # Return the response from Pinata
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Handle any errors during the request to Pinata
        return jsonify({'error': f'Request to Pinata failed: {str(e)}'}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

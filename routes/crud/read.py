from flask import Blueprint, request, jsonify
import requests
import os
import json
import time

read_bp = Blueprint('read', __name__)



headers = {"Authorization": f"Bearer {os.environ.get('PINATA_JWT')}"}

@read_bp.route('/retrieve_files', methods=['GET'])
def retrieve_files():
    url = "https://api.pinata.cloud/v3/files"

    response = requests.request("GET", url, headers=headers)

    files_data=json.loads(response.text)

    print(print(response.text))
    files_data=files_data['data']['files']

    return {'response': files_data}



@read_bp.route('/download_file', methods=['POST'])
def download_file():
    try:
        # Extract parameters from the request body
        data = request.json
        cid = data.get('cid')  # Get the 'cid' from the request body
        print("CIDCDCD",cid)
        
        expires = data.get('expires', 3600)  # Default to 1 hour (3600 seconds)
        
        # Set the current Unix timestamp as the date
        current_unix_timestamp = int(time.time())

        if not cid:
            return jsonify({'error': 'CID is required'}), 400

        # Construct the desired URL
        desired_url = f"https://peach-electrical-bat-818.mypinata.cloud/files/{cid}"

        # Prepare the payload
        payload = {
            "url": desired_url,
            "expires": expires,
            "date": current_unix_timestamp,
            "method": "GET"
        }

        # Pinata API endpoint
        url = "https://api.pinata.cloud/v3/files/sign"

        # Make the POST request to Pinata
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            signed_url = response.json().get("data")
            return jsonify({'signed_url': signed_url}), 200
        else:
            return jsonify({'error': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Handle request errors
        return jsonify({'error': f'Request to Pinata failed: {str(e)}'}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
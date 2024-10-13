from flask import Blueprint, request, jsonify
import requests
import os

# Create the Blueprint
delete_bp = Blueprint('delete', __name__)

# Set headers for authentication
headers = {"Authorization": f"Bearer {os.environ.get('PINATA_JWT')}"}

@delete_bp.route('/delete_file', methods=['DELETE'])
def delete_file():
    try:
        # Get the 'id' parameter from the request JSON body
        data = request.json
        file_id = data.get('id')

        if not file_id:
            return jsonify({'error': 'File ID is required'}), 400

        # Construct the URL for deleting the file
        url = f"https://api.pinata.cloud/v3/files/{file_id}"

        # Make the DELETE request to Pinata
        response = requests.request("DELETE", url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return jsonify({'message': 'File deleted successfully'}), 200
        else:
            return jsonify({'error': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Handle request errors
        return jsonify({'error': f'Request to Pinata failed: {str(e)}'}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

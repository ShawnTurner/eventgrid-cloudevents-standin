import sys
import json
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Log all command-line arguments
logging.info(f'Command-line arguments: {sys.argv}')

# Code all subscriptions here and push or do whatever

# Check if a payload was passed
if len(sys.argv) > 1:
    # The JSON payload is passed as the second command-line argument
    payload_json = sys.argv[1]

    # Parse the JSON payload
    payload = json.loads(payload_json)

    # Now you can access the data in the payload. For example, to log the entire payload, you can do:
    logging.info(payload)

    # Make a POST request to consumer:8000 with the payload
    response = requests.post('http://consumer:8000', json=payload)

    # Log the response from the server
    logging.info(f'Response status code: {response.status_code}')
    logging.info(f'Response body: {response.text}')

else:
    logging.warning("No payload was passed to the script.")
import sys
import json
import requests
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Log all command-line arguments
logging.info(f"Command-line arguments: {sys.argv}")

# This script models the 'test' topic and the processing of a single message that is pushed to the topic.
# All subscriptions to the topic must be given their message here.

# Check if a payload was passed
if len(sys.argv) > 1:
    # The JSON payload is passed as the second command-line argument
    payload_json = sys.argv[1]

    # Parse the JSON payload
    payload = json.loads(payload_json)
    logging.info(payload)

    # Webhook CloudEvents Subscription
    headers = {
        "ce-specversion": payload["root"][0]["specversion"],
        "ce-type": payload["root"][0]["type"],
        "ce-source": payload["root"][0]["source"],
        "ce-id": payload["root"][0]["id"],
        "ce-time": payload["root"][0]["time"],
        "Content-Type": "application/json",
    }
    response = requests.post(
        os.getenv("TEST_WEBHOOK_URL", "http://consumer:8000"),
        headers=headers,
        json=payload["root"][0]["data"],
    )
    # Log the response from the server
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response body: {response.text}")

    # Hypothetical second subscription, push to EventBus, etc

else:
    logging.warning("No payload was passed to the script.")

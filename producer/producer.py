import os
from azure.core.messaging import CloudEvent
from azure.eventgrid import EventGridPublisherClient
from azure.core.credentials import AzureKeyCredential

# Get Event Grid endpoint and key from environment variables
endpoint = os.environ.get("EVENT_GRID_ENDPOINT")
key = os.environ.get("EVENT_GRID_KEY")

# Create an EventGridPublisherClient
credential = AzureKeyCredential(key)
client = EventGridPublisherClient(endpoint, credential)

# Create a CloudEvent
event = CloudEvent(
    source="/myapp/messages",
    type="MyApp.MessagePublished",
    data={
        "message": "Hello, Azure EventGrid!"
    }
)

# Send the event
client.send([event])


print("Event published.")
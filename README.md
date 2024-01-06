
# EventGrid Webhook Stand-in

To locally test an EventGrid choregraphy, we can simulate webhook subscriptions by proxying POST requests to python scripts, which can simulate whatever behavior we need, such as relaying the payload as a POST request to a local event grid subscription endpoint.

This is _not_ any kind of EventGrid emulator or simulator. It is meant to be compatible with the EventGrid client libraries, which are ultimately straightforward HTTP clients.

## Get Started

1. Build and Start the python consumer app and the eventgrid standin

    `docker compose up --build`

2. Send a CloudEvents message in python using the CloudEvent SDK

    ```shell
    export EVENT_GRID_ENDPOINT=http://localhost:9000/hooks/test-topic
    export EVENT_GRID_KEY=dummy-key
    python producer/producer.py

    Event published.
    ```

3. Check consumer and webhook logs for processing

    ```shell
    2024-01-06 16:01:39 INFO:     Started server process [1]
    2024-01-06 16:01:39 INFO:     Waiting for application startup.
    2024-01-06 16:01:39 INFO:     Application startup complete.
    2024-01-06 16:01:39 INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    2024-01-06 16:01:41 receive_event
    2024-01-06 16:01:41 Received event: {'attributes': {'specversion': '1.0', 'id': '900adf69-e383-4d7d-9e42-1536cd46a966', 'source': '/myapp/messages', 'type': 'MyApp.MessagePublished', 'datacontenttype': 'application/json', 'time': '2024-01-06T21:01:41.072587Z'}, 'data': {'message': 'Hello, Azure EventGrid!'}}
    2024-01-06 16:01:41 INFO:     172.18.0.3:44908 - "POST / HTTP/1.1" 200 OK
    ```

# Azure Integration Scribbles

> To verify that the producer and consumer are compatible with real EventGrid subscriptions

0. 
  - Register with ngrok and configure your auth token
  - create an Azure EventGrid topic.

1. `docker run -it -p 4040:4040 -e NGROK_AUTHTOKEN=$NGROK_AUTHTOKEN ngrok/ngrok http 8000` or set env var and uncomment ngrok in [docker-compose.yaml](./docker-compose.yaml).

2. Assure that the consumer can process a cloud event

    ```shell
    curl -X POST -H "Content-Type: application/cloudevents+json" -d '{
    "specversion" : "1.0",
    "type" : "test",
    "source" : "test",
    "subject" : "test",
    "id" : "123",
    "time" : "2022-01-01T00:00:00Z",
    "datacontenttype" : "application/json",
    "data" : {}
    }' localhost:8000
    ```

3. Create an azure event grid subscription to your ngrok endpoint

    ```shell
    webhook_endpoint=${NGROK_ENDPOINT}
    az eventgrid event-subscription create --name consumer-subscription --source-resource-id /subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.EventGrid/topics/{topic} --endpoint $webhook_endpoint
    ```
    When everything is configured correctly, Azure will successfully activate the subscription.  Azure takes some time to complete this.

4. Send a message using producer.py

    ```shell
    export EVENT_GRID_ENDPOINT=https://test-a0d17325-topic.eastus-1.eventgrid.azure.net/api/events
    export EVENT_GRID_KEY=${event_grid_access_key}
    python producer/producer.py

    Event published.
    ```

    If the subscription to the ngrok endpoint and proxy to docker works correctly, the message should be logged by the consumer.

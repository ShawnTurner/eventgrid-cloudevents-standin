pip install -r requirements.txt

docker run -it -p 4040:4040 -e NGROK_AUTHTOKEN=$NGROK_AUTHTOKEN ngrok/ngrok http 8000

docker build -t event-consumer .
docker run -d -p 8000:8000 event-consumer

python3 producer.py

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

az eventgrid event-subscription create --name consumer-subscription --source-resource-id /subscriptions/{subscription_id}/resourceGroups/test/providers/Microsoft.EventGrid/topics/{topic} --endpoint {webhook_endpoint}
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from cloudevents.http import from_http
from pydantic import BaseModel
from starlette.responses import Response
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValidationEvent(BaseModel):
    id: str
    eventType: str
    subject: str
    eventTime: str
    data: dict


@app.post("/")
async def receive_event(request: Request):
    print(f"receive_event")

    body = await request.body()
    event = from_http(request.headers, body)

    # Check if the event is a validation event
    if event["type"] == "Microsoft.EventGrid.SubscriptionValidationEvent":
        # The event is a validation event, so return the validation code
        validation_code = event["data"]["validationCode"]
        print("Validation event received.")
        return {"validationResponse": validation_code}

    # Print the event
    print(f"Received event: {event}")

    # Return a response
    return Response(content=body, media_type="application/json")


@app.get("/")
async def get_empty_page():
    return Response(status_code=200, content="")


@app.options("/")
async def receive_options(request: Request):
    return Response(
        status_code=200,
        headers={
            "Allow": "POST",
            "WebHook-Allowed-Origin": request.headers.get("WebHook-Request-Origin"),
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

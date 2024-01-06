FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "consumer:app", "--host", "0.0.0.0", "--port", "8000"]
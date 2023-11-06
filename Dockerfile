FROM python:3.11

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

# Determines whether the process running is active, running and healthy.
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

EXPOSE 8000

CMD ["python3", "main.py"]

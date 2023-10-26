FROM python:3.11

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "main.py"]

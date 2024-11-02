FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
    
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG WEATHER_API_KEY
ARG GEMINI_API_KEY

ENV WEATHER_API_KEY=${WEATHER_API_KEY}
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

EXPOSE 5000

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

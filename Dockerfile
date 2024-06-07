FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

RUN adduser app --uid 10000 && chown -R 10000:10000 /app/
USER 10000

EXPOSE 80
CMD "gunicorn"

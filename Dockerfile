FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
EXPOSE 80
CMD "gunicorn"
FROM python:3.10-slim-buster

WORKDIR /app

COPY ./src ./src

COPY ./Data ./Data

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--chdir", "src", "-b", "0.0.0.0:8050", "app:server"]

FROM python:3.10-slim
RUN pip install poetry

# to reduce image size and increase performance
ENV PYTHONDONTWRITEBYTECODE 1
# to be able to see logs in container terminal
ENV PYTHONUNBUFFERED 1

ADD ./poetry.lock poetry.lock
ADD ./pyproject.toml pyproject.toml

# to reduce image size
RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN mkdir /static
RUN mkdir /app
WORKDIR /app
ADD ./ /app/

EXPOSE 8001
ENTRYPOINT ["sh","/app/docker/docker-entrypoint.sh"]

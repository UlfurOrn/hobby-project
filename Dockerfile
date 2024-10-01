FROM python:3.12

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY src/ src

WORKDIR /app/src

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "fastapi", "run", "pokemon_api/main.py"]

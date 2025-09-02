FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --locked 

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
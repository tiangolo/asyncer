FROM python:3.8

RUN pip install --no-cache-dir httpx "pydantic==1.5.1" pygithub

COPY ./app /app

CMD ["python", "/app/main.py"]

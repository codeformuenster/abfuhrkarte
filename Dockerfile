FROM python:3.8-slim

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY generate_sperrkarte.py generate_sperrkarte.py

CMD ["python", "generate_sperrkarte.py"]

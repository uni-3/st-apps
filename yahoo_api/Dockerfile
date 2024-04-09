FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

#RUN mkdir /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["streamlit", "run"]

CMD ["search.py"]
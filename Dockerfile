FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirments.txt .
RUN pip install -r requirments.txt

COPY . .

#COPY entrypoint.prod.sh .
#RUN sed -i 's/\r$//g'  entrypoint.prod.sh
#RUN chmod +x  entrypoint.prod.sh
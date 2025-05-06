#FROM ubuntu:latest
#LABEL authors="Alisher"
#
#ENTRYPOINT ["top", "-b"]
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]


EXPOSE 8000

CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]



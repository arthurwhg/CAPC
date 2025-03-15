FROM python:3.10-alpine
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN apk add --no-cache postgresql-dev g++ gcc musl-dev
RUN apk add --no-cache g++ gcc musl-dev postgresql-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY .. /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
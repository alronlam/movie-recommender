FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade && pip install -r requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput && python manage.py migrate
RUN npm run prod

EXPOSE 8000
CMD ["gunicorn", "config:wsgi"]

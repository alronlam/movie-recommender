FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install pip-tools==7.3.*
RUN pip install -r requirements.txt

# RUN apt-get update && apt-get -y install npm@9.5.1
# COPY package*.json .
# RUN npm install
# RUN npm run prod

COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

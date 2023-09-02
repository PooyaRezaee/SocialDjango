FROM python:3.11-slim-bullseye

# pip envirements
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# initlize project
WORKDIR /src

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# migrate database and static files
#RUN python manage.py migrate
RUN mkdir -p /var/www/social
RUN python manage.py collectstatic
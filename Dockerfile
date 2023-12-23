FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/runtext
WORKDIR /usr/src/runtext

RUN apt update

COPY ./requirements.txt /usr/src/runtext/requirements.txt
RUN apt install -y python3-opencv
RUN apt install -y espeak espeak-ng
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /usr/src/runtext/requirements.txt

COPY . /usr/src/runtext
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["gunicorn", "-b", "0.0.0.0:8000", "it_solution_proj.wsgi"]
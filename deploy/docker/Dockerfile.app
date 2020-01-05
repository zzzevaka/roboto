FROM python:3.6

WORKDIR /opt/project

COPY . /opt/project/

RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000

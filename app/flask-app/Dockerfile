FROM python:3.9
WORKDIR /app

RUN mkdir ./flask-app
COPY . ./flask-app
WORKDIR /app/flask-app
RUN pip install -r requirements.txt
ENV FLASK_ENV development

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
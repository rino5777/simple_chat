

FROM python:3.9-slim

WORKDIR /chatapp

COPY . /chatapp

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
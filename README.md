# Asynchronous Chat based on Django with WebSockets

This project is an asynchronous chat based on Django with the use of WebSockets. It allows users to send and receive messages in real-time. The application is launched in a Docker container for easy deployment and scalability.

 To start the project, simply run the following command:

( through Docker )
>Build the Docker Image and Run the Container
```
 >docker-compose up --build
```
>Execute Database Migrations
```
 >docker-compose exec web python manage.py migrate
 ```
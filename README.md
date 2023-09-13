# chatapp

## Introduction

Welcome to the Django ChatApp Backend project! This backend server serves as the foundation for a real-time chat application built using Django and WebSocket technology.

The primary goal of this project is to provide a scalable and efficient backend system to handle user authentication, chat message storage, and real-time message delivery. It allows users to communicate with each other seamlessly.

## Features

- User registration and authentication.
- Real-time chat messaging using WebSockets.
- Private chat support.
- Message history retrieval.
- Token-based authentication for secure communication.
- Customizable and extensible Django application.

## Requirements

Before getting started, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/) (3.10 recommended)
- [PostgreSQL](https://www.postgresql.org/) or other compatible database
- [Redis](https://redis.io/) (for Django Channels)


## Installation
* If you wish to run your own build, first ensure you have Python globally installed on your computer. If not, you can get python 3.10 [here](https://www.python.org").

* After doing this, clone this repo to your machine
    ```bash
        $ git clone git@github.com:AmmarAR97/chatapp.git
    ```

* Then move into the cloned repo as:
    ```bash
        $ cd chatapp
    ```

* Then, create virtual environment for python:
    ```bash
        $ python -m venv .
    ```

* #### Dependencies
    1. Activate the virtual env by running the following command:
        ```bash
            $ source bin/activate
        ```
    2. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt 
        ```
    3. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the file API service on your browser by using
    ```
        http://localhost:8000/
    ```
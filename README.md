# SmartChart-AI

## Description

This is a Capstone project partner with [Epic](https://www.epic.com/). This project aims to augment patient portals with an AI-driven plugin, it could process complex health information and simplify it for the patient right inside the browser.

## Style Guide
This project uses Python Django for the backend, React for the frontend, and MySQL for database operations.

## Getting Started

### Installing
* recommend node version 22.8.0
* install docker

### Executing program
For first time use, run `docker compose up --build` in root, then run `docker ps`, copy paste the CONTAINER ID of backend to `docker exec -it [CONTAINER ID] bash`, then run `python3 manage.py migrate`. Now you can sign up and log in with user authetation.

To only view the frontend, run ```npm install``` and ```npm start``` in ``frontend`` directory.

<!-- For using AI-plugin, generate your key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to ```.env``` in backend. -->
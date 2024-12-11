# SmartChart-AI

## Description

This is a Capstone project partner with [Epic](https://www.epic.com/). This project aims to augment patient portals with an AI-driven plugin, it could process complex health information and simplify it for the patient right inside the browser.

This project uses Python Django for the backend, React for the frontend, and MySQL for database operations.

## Setup Guide

### Installation
* recommend node version 22.8.0
* install docker desktop

### Executing program

#### First time setup
git clone our repo in your local. Run `docker compose up --build -d` in root, open the docker desktop to make sure all containers are activated. Open the frontend in a browser at `http://localhost:3000/`.

Run `docker ps`, copy paste the backend `CONTAINER ID` into `docker exec -it [CONTAINER ID] bash`, then run `python3 manage.py migrate`. Now you can sign up and log in with user authetation.

#### Returning User
Run `docker compose up --build -d` in root. Open the frontend in a browser at `http://localhost:3000/`.

#### Only Viewing frontend
Run ```npm install``` and ```npm start``` in ``frontend`` directory.

## Usage

### What works well

### What does not work well yet

## Next Step

## Acknowledgement

<!-- For using AI-plugin, generate your key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to ```.env``` in backend. -->
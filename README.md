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

- **User Authentication**: Sign-up & log-in feature that secure medical data to protect user privacy.  
- **Quick Sample View**: A preview page showcasing the dashboard and chatbot features.  
- **Medical Report Processing**: Users can upload medical reports and toggle to a friendly mode, where AI simplifies medical data into cards with easy-to-understand summaries.
- **Integrated Chatbot**: An chatbot helps users answer questions related to their medical reports.  
- **Better UI**: Drag-and-drop chatbot, floating card and adjustable font size for better user experience.

### What does not work well yet
- **Web Scraping**: While Selenium and BeautifulSoup worked locally, integrating them into the Docker application caused unresolved technical issues. The unfinished work is cuurent in `scraping-feature` branch.


## Next Step
1. **Enhance Dashboard**: Link dashboard elements to both original and simplified data, enable the AI to explain detailed part when clicking on a specific text in dashboard.
2. **Web Scraping**: Fix Docker integration for web scraping to scrape user's Epic MyChart report.
3. **Expand Database Features**: Fully implement chat history saving and question tracking in database to provide better chatbot context and continuity.

## Acknowledgement
Large thanks to our mentors from Epic - Brandon Lusk, Brock Humblet and Dan Wortmann for their invaluable guidance throughout the semester! Special thanks for instructor Amber Field for teaching Agile principles, as well as TA and peer mentor for for their constant support.

<!-- For using AI-plugin, generate your key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to ```.env``` in backend. -->
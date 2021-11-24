# stabine
## About
*stabine* kümmert sich um die Stabilität des [Klimacamp Augsburg](https://klimacamp-augsburg.de).

Damit das Camp von der Versammlungsfreiheit geschützt ist, müssen rund um die Uhr mindestens zwei Menschen anwesend sein. Sobald im Schichtplan (einem Online-Kalender) Lücken sind, schreibt *stabine* über Telegram ein paar Aktivisti an um diese zu füllen.

## Prerequisites
- Python
- pipenv

## Getting started
### Installation

    pipenv install

### Configuration
The application must be configured using environment variables or a `.env` file. See [settings.py](stabibot/settings.py) for all required and optional variables.

### Run

    python -m stabibot.tasks.daily

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

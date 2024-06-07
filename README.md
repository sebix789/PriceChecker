# PriceChecker

Web app created for comparing product price and offers.

## Project setup

### Mongo (Windows)

1. Install MongoDB Community Server from the [official site](https://www.mongodb.com/try/download/community)
2. Add Monogo to `PATH`:

- go to enviornment variables
- change environmanet variables
- in system variables look for PATH
- add new entry `your_path_to_mongo\MongoDB\Server\your_version`

3. Create folder `data/db` in main C folder (your path should look like that `C:\data\db`)
4. Run CMD in this directory `mongod` command

### Django and virtual env

1. Make sure you're in the topmost `kernel` directory
2. Create virtual environment `python3 -m venv .venv`
3. Install dependencies `pip install requirements.txt`
4. Run migrations `python manage.py migrate`
5. Start the server `invoke runserver`

### Optional stuff

- Install MongoDB Compass to see and manage your data with a GUI

## Packages

- beautifulsoup4==4.12.3
- Django==4.2.7
- django_environ==0.11.2
- invoke==2.2.0
- pymongo==4.7.2
- selenium==4.21.0

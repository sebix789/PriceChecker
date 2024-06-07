# PriceChecker

Web app created for comparing product price and offers.

# Installation
First you need to install MongoDB Community Server from official site https://www.mongodb.com/try/download/community
Make sure to install also MongoDB Compass to graphical see and manage your data, but it's not required
After successfull installation add Monogo to PATH variable by:
- go to enviornment variables
- change environmanet variables
- in system variables look for PATH
- add new entry your_path_to_mongo\MongoDB\Server\your_version

After that steps create folder data/db in main C folder (your path should look like that C:\data\db)
Run CMD in this directory `mongod` command

In project root install and run virtual environment (venv, but it's not required)
In project root run `pip install requirements.txt`

After that in project root `kernel` run `invoke runserver`

Now app is running

# Packages
Package used in project:
- beautifulsoup4==4.12.3
- Django==4.2.7
- django_environ==0.11.2
- invoke==2.2.0
- pymongo==4.7.2
- selenium==4.21.0

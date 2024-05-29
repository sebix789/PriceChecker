from invoke import task

@task
def runserver(c):
    c.run("python manage.py runserver")
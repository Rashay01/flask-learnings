# Setup

## Virtual ENV

```sh
python -m venv myenv
```

## Activate 
in cmd:
```sh
.\myenv\Scripts\Activate.ps1
```

### Git Ignore

- Add .gitignore file

### Create Repo in Github
1. Stage files --> `git add .`
2. Commit --> `git commit -m "message" .`
3. Push Github


## Installing flask

make sure your env is activated - [ref](https://flask.palletsprojects.com/en/3.0.x/installation/) 

```sh
pip install Flask
```
## Flask
- micro-framework --> tools to implement REST API
- freedom- as powerful as django 
- Light-weight 


DJANGO
- Competition --> a full fledge framework  with all the stuff 
- pre-made 
- heavy 

# Run flask 
```sh
flask --app main run
```

> if main file called `app.py`
```sh
flask run
```

For development 
```sh
flask run --debug
```
or
```sh
flask --app hello run --debug
```

runs on :
http://localhost:5000/

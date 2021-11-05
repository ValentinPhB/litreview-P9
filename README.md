# LitReview WebApp

## Table of contents

1. General info
2. Technologies
3. Setup
Setup for Unix
Setup for Windows
5. Run
6. Comptes
7. Author

## General info

Student project for OC. Web application : Reviews for articles and books.

With LiteReview you can follows/unfollow users, post/adjust your reviews of books and articles.
You can also require reviews and answer to other followed users.


## Technologies

Python 3.8.0

- asgiref==3.4.1
- autopep8==1.6.0
- Django==3.2.8
- Pillow==8.3.2
- pycodestyle==2.8.0
- pytz==2021.3
- sqlparse==0.4.2
- toml==0.10.2

## Setup
### A) *Setup for Unix*

Only first-time use :
After downloading litereview-P9-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, download it from https://github.com/ValentinPhB/litreview-P9

Create a virtual environment in "PATH" and install packages from requirements.txt.
```
$ cd ../path/to/litereview-P9
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements.txt
```
## Run
#### *Run local server for Unix* 
```
$ python3 manage.py runserver
```

### B) *Setup for Windows* 

Only first-time use :
After downloading litereview-P9-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, download it from https://github.com/ValentinPhB/litreview-P9

Then, using cmd, go to "PATH", create a virtual environment and install packages from requirements.txt.
```
$ CD ../path/to/litereview-P9
$ py -m venv env
$ env\Scripts\activate.bat
$ py -m pip install -U pip
$ pip install -r requirements.txt
```
## Run
#### *Run local server for Windows*
```
$ python manage.py runserver
```

## 5. Comptes

- SuperUser :   val
- mdp:          a
--------------------
- user :        david
- mdp :         azert12345
--------------------
- user :        louis
- mdp :         azert12345

## 6. Author

Valentin Pheulpin

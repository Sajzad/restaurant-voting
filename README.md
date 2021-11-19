# Restaurant Menu Voting APIs

REST APIs for voting restaurant menus and To find out Menu of the day.


## Getting Started


#### Running Tests in Development 

### How do I get set up? ###

* Clone the repo: ```git clone https://github.com/Sajzad/restaurant-voting.git```.

* Install virtualenv on your system. For linux: ```pip install virtualenv```.

* Go to restaurant-voting dir. And create virtual environment with virtualenv: ```virtualenv -p /usr/bin/python3 .env```.

* Activate the virtual environment: source ```.env/bin/activate```.

* Install required dependencies: ```pip install -r requirements.txt```.

* Set these environment variables which is forwarded via email with corresponding values.

* Go to website dir where the manage.py file.

* Create migrations files: ```./manage.py makemigrations```.

* Update the database with migrations: ```./manage.py migrate```.

* Start the local server: ```./manage.py runserver```.

**.Environent Variable **
```
    SECRET_KEY=foo
```
    
## API Features

```
1. Authentication
2. Creating restaurant
3. Uploading menu for restaurant (There should be a menu for each day)
4. Creating employee
5. Getting current day menu
6. Voting for restaurant menu
7. Getting results for the current day. The winner restaurant should not be the winner for 3 consecutive working days
8. Logout
```

### Dependencies Used

```
asgiref==3.4.1
Django==3.2.9
django-cors-headers==3.10.0
django-rest-framework==0.1.0
djangorestframework==3.12.4
djangorestframework-jwt==1.11.0
importlib-metadata==4.8.2
Markdown==3.3.6
PyJWT==1.7.1
pytz==2021.3
sqlparse==0.4.2
typing_extensions==4.0.0
zipp==3.6.0
```

## API Endpoints

Few endpoints require a token for authentication.

```
    `{'Authorization': 'Bearer': <token>}`
 ```

```
| EndPoint                                        |                       Functionality |
| ------------------------------------------------|-----------------------------------: |
| POST /api/register-user/                        |                Register a user      |
| POST /api/create-employee/                      |         Create a new employee       |
| POST /api/login/                                |                     User login      |
| GET /api/logout/                                |                    User Logout      |
| GET /api/restaurants/                           |            List of all restaurants  |
| GET /api/menu-list/                             |      List of all menus of today     |
| GET /api/vote/:id/                              |                       Vote menu     |
| GET /api/results/                               |         Show results of today       |

```
## Responses

The API responds with JSON data by default.


## Request examples

Request GET /api/results/

curl -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" https://localhost:8000/api/results/

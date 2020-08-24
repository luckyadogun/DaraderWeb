# Michael_UBA_Rental_WEB

### Project setup
1. Create a virtual environment
- Install Python 3.7.3
- `pip install pipenv`
- `pipenv --python 3.7.3`

2. Activate virtual environment
- `pipenv shell`
- Deploy app to your local environment:
  - If you use a Unix OS, from terminal run: `export ENVIRONMENT=local`
  - If you use a Windows OS, from Powershell run: `[Environment]::SetEnvironmentVariable('ENVIRONMENT',
    'local', 'User')` # 'User' is for the current user account. Replace with 'Machine' for machine-wide effect 
  - If in a production environment: `export ENVIRONMENT=prod`
  - If in a staging environment: `export ENVIRONMENT=staging`
 
3. Install dependencies
- `pipenv install -r requirements.txt`
- If in production or staging environment, run: `pipenv install -r requirements-prod.txt` 


### Database Setup

- Install Docker and Docker-compose
- `docker-compose up`

### Up and Running
- `python manage.py makemigrations`
- `python manage.py migrate`
- should you experience a PostgresDB bug do:
   https://github.com/Radu-Raicea/Dockerized-Flask/wiki/%5BDocker%5D-Remove-all-Docker-volumes-to-delete-the-database


# API Documentation Darader

This API documentation guides developers on the expected structure needed to **add new** functionalities and *consume* existing resources for this application.

#### Objects:
```
Property
Users
Country
State
LGA
Company
Gallery
FloorPlan
PropertyDetails
BookingRequest
BookmarkedProperty
Hotels
HotelPhotos
Room
FAQ
```

#### Response Codes

###### Response Codes

```markdown
200: Success
400: Bad request
401: Unauthorized
404: Cannot be found
405: Method not allowed
422: Unprocessable Entity 
50X: Server Error
```

##### Error Codes Details

```
100: Bad Request
110: Unauthorized
120: User Authenticaion Invalid
130: Parameter Error
140: Item Missing
150: Conflict
160: Server Error
```

##### Example Error Message

```
http code 402
{
    "code": 120,
    "message": "invalid crendetials",
    "resolve": "The username or password is not correct."
}
```



#### Functionalities

## Login

**You send:** Your login credentials. 

**You get:** An `API-Token` with which you can make further actions.

**Request:**

```
POST: /login 
{
    "username": "foo",
    "password": "1234567" 
}
```

**Successful Response:**

```
STATUS: 200 OK
{
   "apitoken": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "expirationDate": "2018-02-13T15:31:55.559Z"
}
```

**Failed Response:**

```
STATUS: 401 Unauthorized
{
    "code": 120,
    "message": "invalid crendetials",
    "resolve": "The username or password is not correct."
}
```

## Register

**You send:** Registration credentials. 

**You get:** A resolve message indicating success

**Request:**

```
POST: /register
{
    "username": "foo",
    "email": "jonhdoe@email.com",
    "password": "1234567" 
    "tos": true
}
```

**Successful Response:**

```
HTTP/1.1 200 OK
Server: My RESTful API
Content-Type: application/json
Content-Length: xy

{
   "code": 200
   "message": "Successful"
   "resolve": "Account Successfully created"
}
```

**Failed Response:**

```
STATUS: 401 Unauthorized

{
    "code": 120,
    "message": "invalid crendetials",
    "resolve": "The username or password is not correct."
}
```

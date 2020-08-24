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


##API

### Objects:
- Property
- Users
- Country
- State
- LGA
- Company
- Gallery
- FloorPlan
- PropertyDetails
- BookingRequest
- BookmarkedProperty

- Hotels
- HotelPhotos
- Room
- FAQ

### URIs:
#### Property:
- POST /property
- GET /property
- GET /property/{id}
- PUT /property/{id}
- DELETE /property/{id}
- PATCH /property/{id}
//TODO:
// Add custom actions if need be

#### Users:
- POST /user
- GET /user
- GET /user/{id}
- PUT /user/{id}
- DELETE /user/{id}
- PATCH /user/{id}
//TODO:
// Add custom actions if need be

#### Property:
- POST /property
- GET /property
- GET /property/{id}
- PUT /property/{id}
- DELETE /property/{id}
- PATCH /property/{id}
//TODO:
// Add custom actions if need be

#### Country:
- POST /country
- GET /country
- GET /country/{id}
- PUT /country/{id}
- DELETE /country/{id}
- PATCH /country/{id}
//TODO:
// Add custom actions if need be


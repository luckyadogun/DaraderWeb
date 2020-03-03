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
3. Install dependencies
- `pipenv install -r requirements.txt`


### Database Setup

- Install Docker and Docker-compose
- `docker-compose up`

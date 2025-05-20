# PWP SPRING 2025
# CookBook API

## Group Information
* Student 1. Shehan Hettiarachchige (nicholas.hettiarachchige@student.oulu.fi)
* Student 2. Amanda Randombage (Amanda.Randombage@student.oulu.fi)
* Student 3. Hans Madalagama (Hans.Madalagama@student.oulu.fi)

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

## Prerequisites
- Python 3.12.3
- SQLite 3.44.3
- Flask 3.1.0


### 1. Create and Activate Virtual Environment
For Windows PowerShell
```bash
python -m venv pwpenv
source pwpenv\Scripts\activate
```
For Linux
```bash
python -m venv pwpenv
source pwpenv\bin\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
#### Change directory to pwp-cookbook
```bash
cd "pwp-cookbook"
```

### 3. Set Environment Variables
For Windows PowerShell:
```bash
$env:FLASK_APP = "cookbookapp"
$env:PYTHONPATH = (Get-Location).Path
```
For Linux:
```bash
export FLASK_APP=cookbookapp
export PYTHONPATH=$(pwd)
```

## Database Setup

### 1. Initialize Database
```bash
flask init-db
```

### 2. Generate API Key
```bash
flask init-apikey
```

### 3. Populate Test Data
```bash
flask gen-test-data
```

### 4. Clear Database
```bash
flask drop-db
```

### 5. View Database
To view the database structure and data:
```bash
sqlite3 instance/pwp_cb.db
```

SQLite commands:
```bash
.tables          # List all tables
.schema         # Show table creation scripts
```

## Running the Application

### Start the Flask Server
```bash
flask run
```

The application will be available at:
- Main application: http://localhost:5000
- API Documentation (Swagger UI): http://localhost:5000/apidocs/
- API Specification (JSON): http://localhost:5000/apispec_1.json

## API Documentation

The API documentation is available through Swagger UI at `/apidocs/`. The documentation includes:
- Detailed endpoint descriptions
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Error codes and their meanings

### API Authentication
All API endpoints require an API key for authentication. Include the API key in the request header:
```
API-KEY: your_api_key_here
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/recipe_resource_test.py

# Run tests with coverage report
# Able to check coverage report on web browser using $(pwd)/htmlcov/index.html
pytest --cov=cookbookapp --cov-report=html

pytest --cov=cookbookapp --cov-report=term-missing
```

### Test Data Management
```bash
# Clear test data
flask clear-test-data

# Regenerate test data
flask gen-test-data
```

## Pylinting

### Run tests
```bash
# Run test
pylint --disable=no-member,import-outside-toplevel,no-self-use ./cookbookapp
```

## Deployment

The CookBookApp deployed on Oracle Cloud Infrastructure (OCI).

For successful deployment on OCI you should need:
- Oracle could account (only for the **testing** and **learing purpose** can use Oracle Cloud Free Tier account)
- OCI CLI install and configure (if needed follow https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- Docker
- kubectl

After creating cluster in oracle web console. follow "Quick Start" steps and steup "Local Access", with this method we can manage the cluster locally.

To check the current Kubernetes context (where your commands are being executed)

```bash
kubectl config current-context
```

Navigate to the project root and then run

```bash
kubectl apply -f deployment/cookbook-deployment-oci.yml
```

Check the status of the pods

```bash
kubectl get pods 
```

or for more specifically 

```bash
kubectl get pods -l app=cookbook-app
```

You can get pod names from above commands

Then, create APIKEY using below command
```bash
kubectl exec -it <pod-name> -c cookbook -- flask init-apikey
```

you can get APIKEY for the client app or API client (Postman)
 
To generate test data using
```bash
kubectl exec -it <pod-name> -c cookbook -- flask gen-test-data
``` 

To get service related details and external-IP/ public-IP
```bash
kubectl get svc cookbook-service
```

This public IP can be used in client app or API client (Postman)

To check the events associated with the pod and get more details about pod
```bash
kubectl describe pod <pod-name>
```

To check PersistentVolumeClaim (PVC) and the associated PersistentVolume (PV)
```bash
kubectl get pvc

kubectl describe pvc <PVC-name>
```

To check noded

```bash
kubectl get nodes -o wide
```

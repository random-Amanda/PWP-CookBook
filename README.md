# PWP SPRING 2025
# CookBook
# Group information
* Student 1. Shehan Hettiarachchige (nicholas.hettiarachchige@student.oulu.fi)
* Student 2. Amanda Randombage (Amanda.Randombage@student.oulu.fi)
* Student 3. Hans Madalagama (Hans.Madalagama@student.oulu.fi)


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

- Create and activate a python virtual environment
```bash
    python -m venv pwpenv
    source pwpenv/bin/activate
```

- Install dependencies using requirements.txt file

```bash
    pip install -r requirements.txt
```

- versions:
    SQLite version 3.44.3,
    Python 3.12.3,
    Flask 3.1.0

- Run the database initialization

```bash
    python3 app/app.py
```

#### Check the created database on sqlite

- open the db using sqlite on command prompt

```bash
    pwp_proj> sqlite3 pwp_cb.db
```
- sql dump is available in the instance folder


- Use below command to view the created tables

```bash
   sqlite> .tables
```

- Use schema command to view table screate scripts

```bash
   sqlite> .schema
```

#### Navigate to the cookbookapp directory

- commands for powershell
```bash
   $env:FLASK_APP = "cookbookapp"
   $env:FLASK_ENV = "development" 
```

#### Testing the API

- Set the python path environment variable to current directory
```bash
   $env:PYTHONPATH = (Get-Location).Path
```

- Run PyTest for each of the test case .py files
  ```bash
  pytest tests/recipe_resource_test.py
  pytest --cov=cookbookapp --cov-report=term-missing
  ```

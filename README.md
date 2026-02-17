# MOONBOT

Technical Assessment Backend Engineer

## Running tests

Tests can be run using docker compose by running
```
docker compose up test-runner
```

To run tests locally instead, first install the dependencies using
```
pip install -r requirements-dev.txt
```
or
```
poetry install --with dev
```

Non-e2e tests can then be run using pytest:
```
pytest tests
```

e2e tests can be included in the test run by providing the ```--e2e``` option and will require the API to be running:
```bash
# With API running on http://localhost:8080
API_URL=http://localhost:8080 pytest tests --e2e
```

## Running the API

To run the API using docker compose:
```
docker compose up
```

Then visit http://localhost:8080/docs for interactive Swagger documentation.

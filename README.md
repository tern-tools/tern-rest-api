# Tern REST API

---
**NOTE**

This project still not functional. Please wait for the first functional release
(0.0.1)

---

The Tern REST API is a RESTful API for Tern Project.

Currently, the API is not functional as it is still in the Specification development and project structure phase.

The specification is available at [Tern REST API Offline Swagger](https://tern-tools.github.io/tern-rest-api/), and contributions are welcome.

Mainly the API is implemented asynchronously on the server-side as the tern
reports can take a while to be generated.

```mermaid
  sequenceDiagram
    participant User
    participant API
    participant Tern
    User->>API: GET /api/v1/version
    API-->>User: 200 OK, JSON with version data
    User->>API: POST /api/v1/reports with JSON payload
    API-->>User: 200 OK, JSON with request id
    User->>API: POST /api/v1/reports/status with JSON payload
    API-->>User: 200 OK, JSON with status RUNNING
    API->>Tern: Process the request calling asynchronous
    Tern->>Tern: Processing
    loop
    User->>API: POST /api/v1/reports/status with JSON payload
    Tern->>Tern: Processing
    API-->>User: 200 OK, JSON with status RUNNING or UNKOWN
    end
    Tern->>API: Provides the answer for the id
    User->>API: POST /api/v1/reports/status with JSON payload
    API-->>User: 200 OK, JSON with status FAILED with error or DONE with report
```

## Development

This repository has the ``requirements.txt`` and the ``requirements-dev.txt``
files to help build your virtual environment.

We also recommend using [Pipenv](https://pipenv.pypa.io/en/latest/) to manage your virtual environment.

```shell
$ Pip install pipenv
$ pipenv shell
```

Install development requirements
```shell
$ pipenv install -d
```

### Running the development Tern REST API


Runing the API locally

```shell
$ flask run --reload
```

Open http://localhost:5000/ in your browser.

## Tests

We use [Tox](https://tox.wiki/en/latest/) to manage running the tests.

Running tests
```shell
$ tox
```

## Managing the requirements

Installing new requirements

```shell
$ pipenv install {package}
```

Development requirements
```shell
$ pipenv install -d {package}
```

Updating packages
```shell
$ pipenv update
```

Updating the ``requirements.txt`` and ``requirements-dev.txt``
```shell
$ pipenv lock -r > requirements.txt
$ pipenv lock -r -d > requirements-dev.txt
```
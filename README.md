# Tern REST API

---
**NOTE**

This project still not functional. Please wait for the first functional release (0.0.1)

---

The Tern REST API is a RESTful API for Tern Project.

At the moment the API is not functional as it is still in the Specification
development and project structure phase.

The specification is available at
[Tern REST API Offline Swagger](https://tern-tools.github.io/tern-rest-api/) and
contributions are welcome.

Mostly of the API is implemented in asynchronous way on the server side as the
tern reports can take a while to be generated.

```mermaid
  sequenceDiagram
    participant User
    participant API
    participant Tern
    User->>API: GET /api/v1/version
    API-->>User: 200 OK, JSON with version data
    User->>API: GET /api/v1/reports
    API-->>User: 200 OK, JSON with request id
    User->>API: GET /api/v1/reports/status
    API-->>User: 200 OK, JSON with status RUNNING
    API->>Tern: Process the request caling asynchronous
    Tern->>Tern: Processing
    loop
    User->>API: GET /api/v1/reports/status
    Tern->>Tern: Processing
    API-->>User: 200 OK, JSON with status RUNNING or UNKOWN
    end
    Tern->>API: Provides the answer for the id
    User->>API: GET /api/v1/reports/status
    API-->>User: 200 OK, JSON with status FAILED with error or DONE with report
```

## Development

This repository has the ``requirements.txt`` and the ``requirements-dev.txt`` files to help building your virtual environment. I also recomend use pipenv to manage your virtual environment.

```shell
pip install pipenv
pipenv shell
pipenv install -d
```

Runing the API locally:

```shell
flask run --reload
```

Open http://localhost:5000/ in your browser.
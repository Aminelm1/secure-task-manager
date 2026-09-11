# 🔐 Secure Task Manager

A secure containerized Task Management REST API built with **FastAPI**, **PostgreSQL**, **Keycloak**, **Docker**, **Kubernetes**, and **Jenkins**.

The project demonstrates authentication, role-based authorization, containerization, automated testing, and a complete CI/CD workflow.

## 🏗️ Architecture

```text
Developer
    |
    v
  GitHub
    |
    v
 Jenkins
    |
    +---- Pytest
    |
    +---- Docker Build
    |
    +---- Push Image
    |        |
    |        v
    |       GHCR
    |        |
    +--------+
             |
             v
        Kubernetes
       /     |      \
  FastAPI PostgreSQL Keycloak
                      |
                 PostgreSQL
```

## 🚀 Technologies

- **FastAPI** — REST API
- **PostgreSQL** — application database
- **Keycloak** — Identity and Access Management
- **OAuth2 / OpenID Connect** — authentication
- **JWT** — access tokens
- **RBAC** — role-based access control (`user`, `admin`)
- **Docker** — containerization
- **Kubernetes** — container orchestration
- **Jenkins** — CI/CD automation
- **GitHub Container Registry (GHCR)** — Docker image registry
- **Pytest** — automated testing

## 🔑 Authentication & Authorization

Authentication is handled by Keycloak using OAuth2/OpenID Connect.

The API validates JWT access tokens and implements role-based authorization.

Two application roles are available:

- `user` — access to task operations
- `admin` — access to administrative endpoints

Examples:

```text
GET /health       Public
GET /tasks        user
POST /tasks       user
PUT /tasks/{id}   user
DELETE /tasks/{id} user
GET /admin        admin
```

## 🔄 CI/CD Pipeline

Every Jenkins build executes the following workflow:

```text
GitHub Checkout
      ↓
Automated Tests
      ↓
Docker Image Build
      ↓
Push Image to GHCR
      ↓
Deploy to Kubernetes
      ↓
Kubernetes Rollout
```

Docker images are versioned using the Jenkins build number:

```text
ghcr.io/aminelm1/secure-task-api:<BUILD_NUMBER>
```

This allows each Kubernetes deployment to reference a specific application build.

## 🧪 Automated Tests

Tests are executed automatically by Jenkins using Pytest.

The test suite covers:

- API health check
- unauthenticated access
- user authorization
- admin authorization
- RBAC restrictions

Run locally with:

```bash
python -m pytest -v
```

## ☸️ Kubernetes

The Kubernetes environment contains:

```text
secure-task-api
postgres
keycloak
keycloak-postgres
```

PostgreSQL data is persisted using Kubernetes PersistentVolumeClaims.

Application credentials are provided to containers through Kubernetes Secrets rather than being stored directly in application source code.

## 🐳 Docker

Build the API image:

```bash
docker build -t secure-task-api .
```

The CI/CD pipeline publishes versioned images to GitHub Container Registry.

## ❤️ Health Check

The application exposes:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

## 📁 Project Structure

```text
secure-task-manager/
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── tests/
├── k8s/
├── Dockerfile
├── Dockerfile.jenkins
├── Jenkinsfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🔒 Security

Sensitive local configuration files are excluded from Git:

```text
.env
k8s/secrets.yaml
```

Example configuration files containing placeholders can be committed safely:

```text
.env.example
k8s/secrets.example.yaml
```

Keycloak handles identity management while the API validates signed JWTs and enforces RBAC.

> This project is intended as a local development/DevOps demonstration environment. Some development settings should be hardened before production use.

## 🎯 Project Goals

This project was created to demonstrate practical experience with:

- REST API development
- IAM and authentication
- OAuth2 / OpenID Connect
- JWT validation
- RBAC
- relational databases
- Docker
- Kubernetes
- CI/CD
- automated testing
- container registries
- DevOps and application security
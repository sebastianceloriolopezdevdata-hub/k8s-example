# Weather Microservices Demo

A project that demonstrates how to move from standalone services to containerized multi-service applications.

## Scenario

**SkyRoute Weather** is a fictional company that wants a simple platform where an operator can:

- choose one of 10 supported cities,
- view the current weather in Celsius,
- see friendly weather metadata,
- and validate a local admin user through a separate internal service.

The solution is small but structured like a real microservice system:

- **frontend**: React application for operators
- **weather-service**: FastAPI service that integrates with Open-Meteo
- **users-service**: FastAPI service with a simple local admin/user directory

This project is designed for:

- Dockerfile walkthroughs
- Docker Compose local orchestration
- later migration to Minikube / Kubernetes

## Architecture

```text
React Frontend (Nginx)
        |
        |  /api/weather/*
        v
  weather-service (FastAPI) ----> Open-Meteo Geocoding + Forecast API

        |
        |  /api/users/*
        v
   users-service (FastAPI)
```

## Supported Cities

The weather service allows only these cities:

- Bogota
- Cali
- Medellin
- Cartagena
- Barranquilla
- Quito
- Lima
- Mexico City
- Madrid
- New York

## Project Structure

```text
citycare-weather-demo/
├── docker-compose.yml
├── README.md
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── weather-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
└── users-service/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
```

## Run locally with Docker Compose

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:8080
- Weather API docs: http://localhost:8001/docs
- Users API docs: http://localhost:8002/docs

## Example Endpoints

### Weather service

- `GET /health`
- `GET /cities`
- `GET /weather/{city}`

### Users service

- `GET /health`
- `GET /users`
- `GET /users/admin`
- `POST /login`

# Vetty Crypto API

A production-oriented REST API built with FastAPI for retrieving cryptocurrency market data using CoinGecko API.

The project provides authenticated cryptocurrency endpoints, asynchronous external API communication, pagination, request validation, centralized error handling, configurable in-memory caching, webhook notifications, structured logging, Docker support, API documentation, and automated tests.

---

## Features

- REST API built with FastAPI
- Cryptocurrency data from CoinGecko
- Asynchronous HTTP requests using HTTPX
- API-key authentication for protected endpoints
- Public health-check endpoint
- Coins listing
- Cryptocurrency categories listing
- Market data in CAD
- Filtering by coin ID and/or category
- Pagination support
- Request validation
- Meaningful HTTP status codes
- Centralized application exception handling
- Configurable request timeout
- In-memory response caching
- Configurable cache TTL
- Webhook notification after fresh market-data retrieval
- Structured application logging
- Docker support
- Swagger/OpenAPI documentation
- Automated unit and API tests
- Environment-variable based configuration

---

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- HTTPX
- Pydantic
- Pydantic Settings
- Pytest
- pytest-cov
- Ruff
- Docker
- CoinGecko API

---

## Project Structure

```text
vetty-crypto-api/
│
├── app/
│   ├── api/
│   │   ├── categories.py
│   │   ├── coins.py
│   │   ├── health.py
│   │   └── market.py
│   │
│   ├── cache/
│   │   └── memory.py
│   │
│   ├── exceptions/
│   │   ├── errors.py
│   │   └── handlers.py
│   │
│   ├── schemas/
│   │   ├── category.py
│   │   ├── coin.py
│   │   └── market.py
│   │
│   ├── services/
│   │   ├── coingecko.py
│   │   └── webhook.py
│   │
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md

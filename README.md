# API Privacy Gateway

> Policy-driven outbound API gateway for traffic anonymization and control

A developer-facing control plane that proxies outbound API requests while enforcing privacy, rate limiting, and request-shaping policies to prevent third-party fingerprinting and traffic correlation.

---

## Features

**Privacy & Security**
- Header normalization and sanitization
- User-Agent rewriting and request jitter
- Policy-based anonymization (`standard`, `high_privacy`)
- API key authentication with multi-tenant support

**Performance & Control**
- Redis-backed sliding-window rate limiting (per-client)
- FastAPI control plane with request validation
- Centralized `/v1/relay` endpoint

**Developer Experience**
- Fully Dockerized with one-command startup
- Interactive API documentation at `/docs`
- Python SDK (scaffolded)

---

## Quick Start

```bash
cd infra
docker compose up --build
```

## Usage

```bash
POST /v1/relay
X-API-Key: sk_test_demo
Content-Type: application/json

{
  "method": "GET",
  "url": "https://httpbin.org/anything",
  "policy": "high_privacy"
}
```

---

## Architecture

```
Client App → API Gateway → External APIs
              │
              ├─ Auth (API Key)
              ├─ Rate Limiting (Redis)
              ├─ Policy Enforcement
              └─ Request Shaping
```

---

## Project Structure

```
gateway/
  app/
    api/         # FastAPI routes
    services/    # Auth, rate limiting, policies
    core/        # Configuration

infra/
  docker-compose.yml

sdk/
  api_privacy_gateway/
    client.py
```

---

## Roadmap

- [ ] PostgreSQL-backed policies and API keys
- [ ] Token rotation and key management
- [ ] OpenTelemetry tracing
- [ ] Complete SDK with retry logic
- [ ] Fine-grained per-route limits

---

## Why This Project

Demonstrates production-grade patterns for:
- Multi-tenant API gateway design
- Privacy-preserving network behavior
- Distributed rate limiting
- Clean separation of control and data planes

**Use Cases:** Third-party tracking prevention, organizational privacy policies, API quota management, traffic auditing

---

## License

MIT

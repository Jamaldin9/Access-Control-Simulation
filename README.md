# Access Control Simulation Engine (RBAC)

## Problem

How do enterprise systems enforce role-based access control (RBAC) while maintaining structured audit logs for compliance and monitoring?

This project simulates a real-world RBAC authorization engine with structured logging.

---

## Features

- Role-based permission enforcement
- ALLOW / DENY decision engine
- Disabled-user enforcement
- Structured JSONL audit logging
- Clean modular design

---

## Architecture

User → Authorization Engine → Policy Check → Decision  
Every decision is logged in structured JSONL format.

---

## Example Audit Log Output

```json
{
  "timestamp": "2026-02-20T14:22:11Z",
  "user": "admin_1",
  "action": "delete_record",
  "resource": "patient_db",
  "decision": "ALLOW"
}
# Access Control Simulation Engine (RBAC)

![Python](https://img.shields.io/badge/python-3.x-blue)
![Pytest](https://img.shields.io/badge/tests-pytest-green)

## Overview

This project simulates a production-style Role-Based Access Control (RBAC) authorization engine with structured audit logging.

It demonstrates secure decision-making, fail-closed authorization logic, structured logging for observability, and test-driven validation.

---

## Problem

How do enterprise systems enforce role-based access control (RBAC) while maintaining structured audit logs for compliance, monitoring, and security analysis?

Modern systems must:
- Enforce permissions consistently
- Default to secure behavior (fail-closed)
- Provide structured logs for auditing and incident response
- Remain modular and testable

This project models those patterns in a clean, extensible architecture.

---

## Features

- Role-based permission enforcement
- Fail-closed authorization (default DENY)
- Disabled-user enforcement
- Structured JSONL audit logging
- Modular separation of concerns
- Pytest unit test suite
- Signature-tolerant test harness

---

## Architecture

User → Authorization Engine → Policy Evaluation → Decision → Structured Log

### Design Principles

- **Fail-Closed Security Model**: Unknown roles or actions default to DENY
- **Stateless Authorization Logic**: Pure decision engine without hidden side effects
- **Structured Logging**: JSONL format for ingestion into observability tools
- **Separation of Concerns**: Policy logic decoupled from logging
- **Test-Driven Validation**: Behavior verified via pytest

---

## Example Audit Log Output

```json
{
  "timestamp": "2026-02-20T14:22:11Z",
  "user": "admin_1",
  "action": "delete_record",
  "resource": "patient_db",
  "decision": "ALLOW"
}
```

Logs are written in JSON Lines format, making them suitable for ingestion into:

- Splunk
- Datadog
- Elastic / ELK Stack
- SIEM pipelines

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/access-control-sim.git
cd access-control-sim
pip install -r requirements.txt
```

---

## Run Tests

```bash
pytest
```

---

## Example Usage

```bash
python app.py
```

---

## Real-World Relevance

This project mirrors patterns used in:

- Backend APIs
- Microservices
- Admin dashboards
- Healthcare systems
- Financial systems
- Compliance-sensitive infrastructure

Structured audit logging is critical for:
- Security investigations
- Regulatory compliance
- Behavioral analytics
- Monitoring and alerting

---

## Future Improvements

- JWT-based authentication simulation
- Policy definitions via config files
- Database-backed role storage
- REST API wrapper
- CI/CD integration with GitHub Actions

---

## Why This Project Matters

RBAC systems are foundational to modern distributed systems. This simulation demonstrates practical engineering patterns including secure defaults, modular design, structured logging, and automated testing — all core competencies for production software engineering roles.

---

Built for learning, security modeling, and systems design practice.
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


# Access Control Simulation Engine  
### Role-Based Access Control (RBAC) with Structured Audit Logging

## Overview

This project implements a simplified enterprise-grade Identity & Access Management (IAM) system using Role-Based Access Control (RBAC).

It models how modern infrastructure and security systems handle:

- Role → Permission inheritance  
- Multi-role aggregation  
- Effective permission calculation  
- Authorization decisions (ALLOW / DENY)  
- Disabled-user lifecycle enforcement  
- Structured audit logging  
- JSONL export for compliance and SIEM-style ingestion  

The system simulates core behaviors found in enterprise IAM platforms such as Azure AD, Okta, and AWS IAM.

---

## Architecture

```
access-control-sim/
│
├── src/
│   ├── models.py        # User and Role data models
│   ├── main.py          # RBAC engine, authorization logic, audit logging
│
├── audit_log.jsonl      # Exported structured audit log
└── README.md
```

Separation of concerns is maintained between:

- Data models (User, Role)
- Authorization logic
- Audit logging pipeline

---

## Features

### 1. Role-Based Access Control (RBAC)

- Roles contain permission sets
- Users can hold multiple roles
- Effective permissions are calculated using set union
- Duplicate permissions are automatically removed

Example:

Intern → {"read_docs"}  
IT_Support → {"reset_password"}  

User assigned both roles → {"read_docs", "reset_password"}

---

### 2. Authorization Engine

The `authorize()` function:

- Enforces disabled-user rule (hard deny)
- Computes effective permissions
- Returns True/False for access decisions
- Logs every decision

---

### 3. Structured Audit Logging

Each access request generates a structured audit event containing:

- Timestamp
- Username
- Permission requested
- Result (ALLOW / DENY)
- Reason (has_permission, user_disabled, missing_permission)

Example JSON event:

```json
{
  "ts": "2026-02-25T20:57:54",
  "user": "jamal",
  "permission": "read_docs",
  "result": "ALLOW",
  "reason": "has_permission"
}
```

---

### 4. JSONL Export

Audit events are exported to:

```
audit_log.jsonl
```

Format: **JSON Lines (one JSON object per line)**

This format is commonly used in:

- SIEM systems
- Log aggregation pipelines
- Security monitoring tools
- Compliance auditing workflows

---

## Example Runtime Output

```
Effective permissions for jamal: {'read_docs', 'reset_password'}

[ALLOW] ts=... user=jamal perm=read_docs reason=has_permission
[ALLOW] ts=... user=jamal perm=reset_password reason=has_permission

After disabling user...

[DENY] ts=... user=jamal perm=read_docs reason=user_disabled
[DENY] ts=... user=jamal perm=reset_password reason=user_disabled

Audit summary:
Total events: 4
Denied events: 2
Denied reasons: {'user_disabled': 2}
Top denied permissions: {'read_docs': 1, 'reset_password': 1}
```

---

## Security Concepts Demonstrated

- Least privilege enforcement  
- Identity lifecycle management  
- Role abstraction modeling  
- Permission inheritance  
- Authorization decision logging  
- Structured log design  
- Basic compliance analytics  

---

## Why This Project Matters

This project demonstrates foundational knowledge relevant to:

- Identity & Access Management (IAM)
- Cloud infrastructure engineering
- Security engineering
- Governance, Risk & Compliance (GRC)
- Enterprise IT operations
- Regulated environments (finance, biotech, healthcare)

It reflects how access control and audit logging are implemented in real enterprise systems.

---

## Future Improvements

- Persistent role/user storage (JSON database)
- CLI interface for role management
- Policy-based access control (PBAC)
- Unit tests for authorization engine
- REST API wrapper
- Log rotation simulation
- Multi-user environment simulation

---

## Author

Jamal Din  
Computer Science — Infrastructure & Security Focus

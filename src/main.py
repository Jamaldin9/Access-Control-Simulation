from datetime import datetime
import json
from typing import Dict, Set
from models import Role, User

# Simple in-memory audit log (one dict per event)
AUDIT_LOG: list[dict] = []

def audit_log(user: User, permission: str, result: str, reason: str) -> None:
    """Append an audit event and print a readable line."""
    event = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "user": user.username,
        "permission": permission,
        "result": result,
        "reason": reason,
    }
    AUDIT_LOG.append(event)
    print(f"[{result}] ts={event['ts']} user={event['user']} perm={event['permission']} reason={event['reason']}")

    # In a real system, we would write this to a file or external logging system instead of keeping it in memory.
def export_audit_log_jsonl(filepath: str) -> None:
    """
    Export AUDIT_LOG to a JSON Lines file (one JSON object per line).
    """
    with open(filepath, "w", encoding="utf-8") as f:
        for event in AUDIT_LOG:
            f.write(json.dumps(event) + "\n")

def get_effective_permissions(user: User, roles: Dict[str, Role]) -> Set[str]:
    effective = set()
    for role_name in user.roles:
        role = roles.get(role_name)
        if role is None:
            continue
        effective |= role.permissions
    return effective

def authorize(user: User, roles: Dict[str, Role], permission: str) -> bool:
    if not user.enabled:
        audit_log(user, permission, "DENY", "user_disabled")
        return False
    
    effective = get_effective_permissions(user, roles)
    if permission in effective:
        audit_log(user, permission, "ALLOW", "has_permission")
        return True
    
    audit_log(user, permission, "DENY", "missing_permission")
    return False

def main():
    #Create Roles and Users
    intern = Role("Intern")
    intern.permissions.add("read_docs")

    it_support = Role("IT_Support")
    it_support.permissions.add("reset_password")

    # Create a roles dictionary for lookup
    roles = {
        intern.name: intern,
        it_support.name: it_support
    }

    # Create a user and assign the role
    jamal = User("jamal")
    jamal.roles = ["Intern", "IT_Support"]

    # Check effective permissions and authorization
    effective_permissions = get_effective_permissions(jamal, roles)
    print(f"Effective permissions for {jamal.username}: {effective_permissions}")

    #Check authorization for specific permissions
    print("Can read_docs?", authorize(jamal, roles, "read_docs"))
    print("Can reset_password?", authorize(jamal, roles, "reset_password"))

    # Now let's disable the user and check permissions again
    jamal.enabled = False
    print("After disabling user...")
    print("Can read_docs?", authorize(jamal, roles, "read_docs"))
    print("Can reset_password?", authorize(jamal, roles, "reset_password"))
    print("\nAudit summary:")
    print(f"Total events: {len(AUDIT_LOG)}")

    denied = [e for e in AUDIT_LOG if e["result"] == "DENY"]
    print(f"Denied events: {len(denied)}")

    # Breakdown of denied reasons
    reasons: dict[str, int] = {}
    for e in denied:
        reasons[e["reason"]] = reasons.get(e["reason"], 0) + 1
    print(f"Denied reasons: {reasons}")

    # Top denied permissions
    denied_perms: dict[str, int] = {}
    for e in denied:
        denied_perms[e["permission"]] = denied_perms.get(e["permission"], 0) + 1
    print(f"Top denied permissions: {denied_perms}")

    # Export audit log to JSONL file
    export_audit_log_jsonl("audit_log.jsonl")
    print("Audit log exported to audit_log.jsonl")


if __name__ == "__main__":
    main()
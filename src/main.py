from typing import Dict, Set
from models import Role, User

def get_effective_permissions(user: User, roles: Dict[str, Role]) -> Set[str]:
    effective = set()
    for role_name in user.roles:
        role = roles.get(role_name)
        if role is None:
            continue
        effective|= role.permissions
    return effective

def authorize(user: User, roles: Dict[str, Role], permission: str) -> bool:
    if not user.enabled:
        return False
    effective = get_effective_permissions(user, roles)
    return permission in effective

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
    jamal.roles.append(intern.name)

    # Create a roles dictionary for lookup
    roles = {intern.name: intern}

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

if __name__ == "__main__":
    main()
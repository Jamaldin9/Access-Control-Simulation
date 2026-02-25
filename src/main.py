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
    
def main():
    intern = Role("Intern")
    intern.permissions.add("read.docs")
    jamal = User("jamal")
    jamal.roles.append(intern.name)
    roles = {intern.name: intern}
    effective_permissions = get_effective_permissions(jamal, roles)
    print(f"Effective permissions for {jamal.username}: {effective_permissions}")

if __name__ == "__main__":
    main()
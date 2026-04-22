from flask import session

ROLE_PERMISSIONS = {
    "admin": {"*": ["read", "write", "delete"]},

    "it": {"*": ["read", "write"]},

    "hr": {
        "dashboard": ["read"],
        "staff": ["read", "write"],
        "schedule": ["read", "write"],
        "reports": ["read", "write"]
    },

    "finance": {
        "dashboard": ["read"],
        "income": ["read", "write"],
        "payroll": ["read", "write"],
        "reports": ["read"]
    },

    "driver": {
        "dashboard": ["read"],
        "payments": ["read", "write"],
        "reports": ["read"]
    },

    "conductor": {
        "dashboard": ["read"],
        "payments": ["read", "write"],
        "reports": ["read"]
    },

    "manager": {
        "dashboard": ["read"],
        "schedule": ["read", "write"],
        "reports": ["read", "write"]
    }
}

def can_access(module, action="read"):
    role = session.get("post", "").strip().lower()

    permissions = ROLE_PERMISSIONS.get(role, {})

    if "*" in permissions:
        return True

    return module in permissions and action in permissions[module]
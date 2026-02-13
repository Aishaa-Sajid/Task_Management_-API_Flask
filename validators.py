import re

# -------- EMAIL VALIDATION --------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# -------- PASSWORD VALIDATION --------
def is_valid_password(password):
    return len(password) >= 6


# -------- REQUIRED FIELDS CHECK --------
def require_fields(data, fields):
    for field in fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"
    return True, None


# -------- TASK STATUS VALIDATION --------
def is_valid_status(status):
    return status in ["pending", "in-progress", "completed"]


# -------- PRIORITY VALIDATION --------
def is_valid_priority(priority):
    return priority in ["low", "medium", "high"]

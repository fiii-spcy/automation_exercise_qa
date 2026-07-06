import uuid


def generate_email():
    return f"hashfi_{uuid.uuid4().hex[:8]}@mailtest.com"
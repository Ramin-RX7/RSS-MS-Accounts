import hashlib


def hash_password(raw_password):
    return hashlib.sha256(bytes(raw_password, "utf-8")).hexdigest()

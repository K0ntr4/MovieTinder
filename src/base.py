import hashlib
import json


def get_db_config():
    """
    Load and return the database configuration from a JSON file.

    The function reads the database configuration from '../config/dbconfig.json'
    and returns it as a dictionary.

    Returns:
        dict: Database configuration parameters.
    """
    with open('../config/dbconfig.json', 'r') as file:
        data = json.load(file)
    return data


def hash_password(password):
    """
    Hash a password using SHA-256.

    This function takes a plaintext password as input, hashes it using the
    SHA-256 algorithm, and returns the hexadecimal representation of the hash.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The SHA-256 hash of the password in hexadecimal format.
    """
    return hashlib.sha256(password.encode()).hexdigest()

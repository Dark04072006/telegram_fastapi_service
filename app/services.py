import os

from dotenv import load_dotenv

load_dotenv()


def check_admin(username, password):
    if username == os.getenv('ADMIN_NAME') and password == os.getenv('ADMIN_PASS'):
        return True
    return False
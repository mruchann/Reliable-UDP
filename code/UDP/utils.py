import datetime
import hashlib


def get_current_timestamp():
    return datetime.datetime.now().timestamp()


def calculate_checksum(data):
    return hashlib.md5(data).digest()
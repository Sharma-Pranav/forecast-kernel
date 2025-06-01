import hashlib
import json

def compute_file_hash(path, algo='sha256') -> str:
    hash_func = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

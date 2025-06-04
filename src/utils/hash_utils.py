"""File hashing helpers used for CI verification."""

import hashlib
import json

def compute_file_hash(path: str, algo: str = 'sha256') -> str:
    """Return the digest of ``path`` using the given algorithm.

    Parameters
    ----------
    path : str
        File path to hash.
    algo : str, optional
        Hash algorithm name recognised by :mod:`hashlib`.

    Returns
    -------
    str
        Hexadecimal digest of the file contents.
    """

    hash_func = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


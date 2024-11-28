from typing import Union

# This file can be empty or contain Python-side implementations if needed
from ._c_uutils_hash_compute import _c_hash_compute, _c_hash_compute_str, _c_hash_compute3


def hash_compute(data: Union[bytes, bytearray, str]):
    if isinstance(data, (bytes, bytearray)):
        return _c_hash_compute(data)
    elif isinstance(data, str):
        return _c_hash_compute_str(data)
    else:
        raise TypeError(f'Unknown type for hash_compute - {data!r}')


def hash_compute3(a: int, b: int, c: int):
    return _c_hash_compute3(a, b, c)

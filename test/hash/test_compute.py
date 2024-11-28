import pytest

from pyuutils.hash import hash_compute, hash_compute3


@pytest.fixture
def sample_data():
    return b"Hello, World!"


@pytest.fixture
def sample_bytearray():
    return bytearray(b"Hello, World!")


@pytest.fixture
def sample_str():
    return "Hello, World!"


@pytest.mark.unittest
class TestUUtilsHash:
    def test_hash_compute(self, sample_data):
        result = hash_compute(sample_data)
        assert isinstance(result, int)
        assert result == 19357685

    def test_hash_compute_bytearray(self, sample_bytearray):
        result = hash_compute(sample_bytearray)
        assert isinstance(result, int)
        assert result == 19357685

    def test_hash_compute_str(self, sample_str):
        result = hash_compute(sample_str)
        assert isinstance(result, int)
        assert result == 19357685

    def test_hash_compute3(self):
        result = hash_compute3(1, 2, 3)
        assert isinstance(result, int)
        assert result == 3082062082

import pytest

from pyuutils.hash import (
    hash_murmur2_u8, hash_compute_u32, hash_compute_u16,
    hash_compute_i32, hash_compute_i16, hash_compute_i8,
    hash_compute_str, hash_compute3
)


@pytest.fixture
def sample_data():
    return {
        "bytes": b"example data",
        "uint32": [1, 2, 3, 4],
        "uint16": [1, 2, 3, 4],
        "int32": [1, 2, 3, 4],
        "int16": [1, 2, 3, 4],
        "string": "example"
    }


@pytest.mark.unittest
class TestHashFunctions:
    @pytest.mark.parametrize(['dname', 'init', 'expected'], [
        ("bytes", 0, 1576048315)
    ])
    def test_hash_murmur2_u8(self, sample_data, dname, init, expected):
        result = hash_murmur2_u8(sample_data[dname], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 2601976293)
    ])
    def test_hash_compute_u32(self, sample_data, init, expected):
        result = hash_compute_u32(sample_data["uint32"], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 2831519633)
    ])
    def test_hash_compute_u16(self, sample_data, init, expected):
        result = hash_compute_u16(sample_data["uint16"], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 2601976293)
    ])
    def test_hash_compute_i32(self, sample_data, init, expected):
        result = hash_compute_i32(sample_data["int32"], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 2831519633)
    ])
    def test_hash_compute_i16(self, sample_data, init, expected):
        result = hash_compute_i16(sample_data["int16"], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 1031300535)
    ])
    def test_hash_compute_i8(self, sample_data, init, expected):
        result = hash_compute_i8(sample_data["bytes"], init)
        assert isinstance(result, int)
        assert result == expected

    @pytest.mark.parametrize(['init', 'expected'], [
        (0, 3160595133)
    ])
    def test_hash_compute_str(self, sample_data, init, expected):
        result = hash_compute_str(sample_data["string"], init)
        assert isinstance(result, int)
        assert result == expected

    def test_hash_compute3(self):
        result = hash_compute3(123, 456, 789)
        assert isinstance(result, int)
        assert result == 4029415479

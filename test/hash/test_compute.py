import random
import string

import pytest

from pyuutils.hash import (
    hash_murmur2_u8, hash_compute_u32, hash_compute_u16,
    hash_compute_i32, hash_compute_i16, hash_compute_i8,
    hash_compute_str, hash_compute3
)


@pytest.fixture(scope="module", autouse=True)
def set_random_seed():
    random.seed(42)


@pytest.fixture
def sample_data():
    """
    Provide sample data for hash function testing.
    Contains various types of input data.
    """
    return {
        "bytes": b"example data",
        "uint32": [1, 2, 3, 4],
        "uint16": [1, 2, 3, 4],
        "int32": [1, 2, 3, 4],
        "int16": [1, 2, 3, 4],
        "string": "example"
    }


@pytest.mark.unittest
class TestHashCompute:
    def test_hash_murmur2_u8_consistency(self, sample_data):
        """
        Test hash consistency by repeating hash computation 100 times.
        Ensures same input always produces same hash value.
        """
        first_hash = hash_murmur2_u8(sample_data["bytes"], 0)
        for _ in range(100):
            assert hash_murmur2_u8(sample_data["bytes"], 0) == first_hash

    def test_hash_murmur2_u8_distribution(self, sample_data):
        """
        Test hash distribution by generating many random inputs.
        Check collision rate is low.
        """
        hash_values = set()
        for _ in range(5000):
            random_bytes = bytes(random.getrandbits(8) for _ in range(10))
            hash_values.add(hash_murmur2_u8(random_bytes, 0))

        # Ensure low collision rate
        assert len(hash_values) > 4900

    def test_hash_murmur2_u8_avalanche(self, sample_data):
        """
        Test avalanche effect by making small input changes.
        Verify significant hash value differences.
        """
        base_input = sample_data["bytes"]
        base_hash = hash_murmur2_u8(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            modified_input = bytearray(base_input)
            modified_input[i] ^= 1  # Flip a bit
            changed_hash = hash_murmur2_u8(bytes(modified_input), 0)
            changed_hashes.append(changed_hash)

        # Calculate bit differences
        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]

        # Ensure significant bit changes
        assert all(diff > 10 for diff in bit_differences)

    def test_hash_murmur2_u8_type(self, sample_data):
        """
        Verify correct return type for hash function.
        """
        result = hash_murmur2_u8(sample_data["bytes"], 0)
        assert isinstance(result, int)

    # Similar test structure for other hash functions...
    def test_hash_compute_u32_consistency(self, sample_data):
        first_hash = hash_compute_u32(sample_data["uint32"], 0)
        for _ in range(100):
            assert hash_compute_u32(sample_data["uint32"], 0) == first_hash

    def test_hash_compute_u32_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_list = [random.randint(0, 2 ** 32 - 1) for _ in range(4)]
            hash_values.add(hash_compute_u32(random_list, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_u32_avalanche(self, sample_data):
        base_input = sample_data["uint32"]
        base_hash = hash_compute_u32(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            modified_input = list(base_input)
            modified_input[i] += 1
            changed_hash = hash_compute_u32(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]

        assert all(diff > 10 for diff in bit_differences)

    def test_hash_compute_u32_type(self, sample_data):
        result = hash_compute_u32(sample_data["uint32"], 0)
        assert isinstance(result, int)

    def test_hash_compute_i32_consistency(self, sample_data):
        first_hash = hash_compute_i32(sample_data["int32"], 0)
        for _ in range(100):
            assert hash_compute_i32(sample_data["int32"], 0) == first_hash

    def test_hash_compute_i32_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_list = [random.randint(-2 ** 31, 2 ** 31 - 1) for _ in range(4)]
            hash_values.add(hash_compute_i32(random_list, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_i32_avalanche(self, sample_data):
        base_input = sample_data["int32"]
        base_hash = hash_compute_i32(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            modified_input = list(base_input)
            modified_input[i] += 1
            changed_hash = hash_compute_i32(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]

        assert all(diff > 10 for diff in bit_differences)

    def test_hash_compute_i32_type(self, sample_data):
        result = hash_compute_i32(sample_data["int32"], 0)
        assert isinstance(result, int)

    # Repeat similar comprehensive tests for other hash functions:
    # - hash_compute_u16
    # - hash_compute_i32
    # - hash_compute_i16
    # - hash_compute_i8
    # - hash_compute_str
    # - hash_compute3

    def test_hash_compute_u16_consistency(self, sample_data):
        first_hash = hash_compute_u16(sample_data["uint16"], 0)
        for _ in range(100):
            assert hash_compute_u16(sample_data["uint16"], 0) == first_hash

    def test_hash_compute_u16_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_list = [random.randint(0, 2 ** 16 - 1) for _ in range(4)]
            hash_values.add(hash_compute_u16(random_list, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_u16_avalanche(self, sample_data):
        base_input = sample_data["uint16"]
        base_hash = hash_compute_u16(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            modified_input = list(base_input)
            modified_input[i] += 1
            changed_hash = hash_compute_u16(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]
        assert all(diff > 7 for diff in bit_differences)

    def test_hash_compute_u16_type(self, sample_data):
        result = hash_compute_u16(sample_data["uint16"], 0)
        assert isinstance(result, int)

    def test_hash_compute_i16_consistency(self, sample_data):
        first_hash = hash_compute_i16(sample_data["int16"], 0)
        for _ in range(100):
            assert hash_compute_i16(sample_data["int16"], 0) == first_hash

    def test_hash_compute_i16_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_list = [random.randint(-2 ** 15, 2 ** 15 - 1) for _ in range(4)]
            hash_values.add(hash_compute_i16(random_list, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_i16_avalanche(self, sample_data):
        base_input = sample_data["int16"]
        base_hash = hash_compute_i16(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            modified_input = list(base_input)
            modified_input[i] += 1
            changed_hash = hash_compute_i16(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]
        assert all(diff > 7 for diff in bit_differences)

    def test_hash_compute_i16_type(self, sample_data):
        result = hash_compute_i16(sample_data["int16"], 0)
        assert isinstance(result, int)

    def test_hash_compute_i8_consistency(self, sample_data):
        first_hash = hash_compute_i8(sample_data["bytes"], 0)
        for _ in range(100):
            assert hash_compute_i8(sample_data["bytes"], 0) == first_hash

    def test_hash_compute_i8_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_bytes = bytes(random.randint(0, 255) for _ in range(random.randint(1, 100)))
            hash_values.add(hash_compute_i8(random_bytes, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_i8_avalanche(self, sample_data):
        base_input = sample_data["bytes"]
        base_hash = hash_compute_i8(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            bts = list(map(lambda x: chr(x).encode(), list(base_input)))
            for _ in range(random.randint(1, min(len(base_input) // 5, 2))):
                bts[random.randint(0, len(bts) - 1)] = \
                    bytes(random.randint(0, 255) for _ in range(random.randint(0, 2)))
            modified_input = b''.join(bts)
            changed_hash = hash_compute_i8(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]
        assert all(diff > 7 for diff in bit_differences)

    def test_hash_compute_i8_type(self, sample_data):
        result = hash_compute_i8(sample_data["bytes"], 0)
        assert isinstance(result, int)

    def test_hash_compute_str_consistency(self, sample_data):
        first_hash = hash_compute_str(sample_data["string"], 0)
        for _ in range(100):
            assert hash_compute_str(sample_data["string"], 0) == first_hash

    def test_hash_compute_str_distribution(self, sample_data):
        hash_values = set()
        for _ in range(5000):
            random_string = ''.join([random.choice(string.printable) for _ in range(random.randint(1, 100))])
            hash_values.add(hash_compute_str(random_string, 0))

        assert len(hash_values) > 4900

    def test_hash_compute_str_avalanche(self, sample_data):
        base_input = sample_data["string"]
        base_hash = hash_compute_str(base_input, 0)

        changed_hashes = []
        for i in range(len(base_input)):
            bts = list(base_input)
            for _ in range(random.randint(1, 2)):
                bts[random.randint(0, len(bts) - 1)] = \
                    ''.join([random.choice(string.printable) for _ in range(random.randint(0, 2))])
            modified_input = ''.join(bts)
            changed_hash = hash_compute_str(modified_input, 0)
            changed_hashes.append(changed_hash)

        bit_differences = [bin(base_hash ^ changed_hash).count('1') for changed_hash in changed_hashes]
        assert all(diff > 10 for diff in bit_differences)

    def test_hash_compute_str_type(self, sample_data):
        result = hash_compute_str(sample_data["string"], 0)
        assert isinstance(result, int)

    def test_hash_compute3_comprehensive(self):
        """
        Comprehensive test for hash_compute3 covering multiple properties.
        """
        # Consistency test
        first_hash = hash_compute3(123, 456, 789)
        for _ in range(100):
            assert hash_compute3(123, 456, 789) == first_hash

        # Type test
        result = hash_compute3(123, 456, 789)
        assert isinstance(result, int)

    def test_hash_compute3_consistency(self):
        first_hash = hash_compute3(123, 456, 789)
        for _ in range(100):
            assert hash_compute3(123, 456, 789) == first_hash

        for _ in range(10):
            a, b, c = random.randint(0, 2 ** 32 - 1), random.randint(0, 2 ** 32 - 1), random.randint(0, 2 ** 32 - 1)
            first_hash = hash_compute3(a, b, c)
            for _ in range(10):
                assert hash_compute3(a, b, c) == first_hash

    def test_hash_compute3_distribution(self):
        hash_values = set()

        for _ in range(5000):
            a = random.randint(0, 2 ** 32 - 1)
            b = random.randint(0, 2 ** 32 - 1)
            c = random.randint(0, 2 ** 32 - 1)
            hash_values.add(hash_compute3(a, b, c))

        collision_rate = 1 - (len(hash_values) / 5000)
        assert collision_rate < 0.05, f"Collision rate too high: {collision_rate}"

    def test_hash_compute3_avalanche_effect(self):
        base_a, base_b, base_c = 123, 456, 789
        base_hash = hash_compute3(base_a, base_b, base_c)

        test_cases = [
            (base_a + 1, base_b, base_c),
            (base_a, base_b + 1, base_c),
            (base_a, base_b, base_c + 1),
        ]

        bit_differences = []
        for test_case in test_cases:
            test_hash = hash_compute3(*test_case)
            diff_bits = bin(base_hash ^ test_hash).count('1')
            bit_differences.append(diff_bits)

        assert all(diff > 10 for diff in bit_differences), \
            f"Insufficient bit changes: {bit_differences}"

    def test_hash_compute3_return_type(self):
        result = hash_compute3(123, 456, 789)
        assert isinstance(result, int), "Return type must be integer"
        assert 0 <= result < 2 ** 32, "Return value out of expected range"

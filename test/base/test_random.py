import math
from collections import Counter

import pytest

from pyuutils.base.random import RandomGenerator


@pytest.fixture
def random_gen():
    """Fixture to provide a RandomGenerator instance."""
    return RandomGenerator()


@pytest.mark.unittest
class TestBaseRandom:
    def test_set_seed(self, random_gen):
        """Test setting the global seed."""
        random_gen.set_seed(42)

    def test_seed(self, random_gen):
        """Test setting the instance seed."""
        random_gen.seed(42)

    @pytest.mark.parametrize("max_value", [10, 100, 1000])
    def test_uni(self, random_gen, max_value):
        """Test uniform distribution for unsigned integer [0, max]."""
        for _ in range(1000):
            result = random_gen.uni(max_value)
            assert 0 <= result <= max_value

    @pytest.mark.parametrize("max_value", [10, 100, 1000])
    def test_uni_with_seed(self, random_gen, max_value):
        """Test uniform distribution for unsigned integer [0, max]."""
        expected = []
        for rid in range(100):
            random_gen.seed(0)
            actual = []
            for _ in range(10):
                result = random_gen.uni(max_value)
                assert 0 <= result <= max_value
                actual.append(result)
                if rid == 0:
                    expected.append(result)

            assert actual == pytest.approx(expected)

        # different seeds
        for sid in range(1, 100):
            random_gen.seed(sid)
            actual = []
            for _ in range(10):
                result = random_gen.uni(max_value)
                assert 0 <= result <= max_value
                actual.append(result)
            assert actual != pytest.approx(expected)

    def test_uni_1(self, random_gen):
        """Test uniform distribution for double [0, 1)."""
        for _ in range(1000):
            result = random_gen.uni_1()
            assert 0 <= result < 1

    @pytest.mark.parametrize("max_value", [10.0, 100.0, 1000.0])
    def test_uni_r(self, random_gen, max_value):
        """Test uniform distribution for double [0, max)."""
        for _ in range(1000):
            result = random_gen.uni_r(max_value)
            assert 0 <= result < max_value

    @pytest.mark.parametrize("rate", [0.1, 1.0, 10.0])
    def test_exp(self, random_gen, rate):
        """Test exponential distribution."""
        for _ in range(1000):
            result = random_gen.exp(rate)
            assert result >= 0

    @pytest.mark.parametrize("minv, maxv", [(0.0, 1.0), (1.0, 2.0)])
    def test_arcsine(self, random_gen, minv, maxv):
        """Test arcsine distribution."""
        for _ in range(1000):
            result = random_gen.arcsine(minv, maxv)
            assert minv <= result <= maxv

    @pytest.mark.parametrize("alpha, beta", [(0.5, 0.5), (2.0, 5.0)])
    def test_beta(self, random_gen, alpha, beta):
        """Test beta distribution."""
        for _ in range(1000):
            result = random_gen.beta(alpha, beta)
            assert 0 <= result <= 1

    @pytest.mark.parametrize("shape, scale", [(2.0, 1.0), (5.0, 2.0)])
    def test_gamma(self, random_gen, shape, scale):
        """Test gamma distribution."""
        for _ in range(1000):
            result = random_gen.gamma(shape, scale)
            assert result >= 0

    @pytest.mark.parametrize("mean, stddev", [(0.0, 1.0), (5.0, 2.0)])
    def test_normal(self, random_gen, mean, stddev):
        """Test normal distribution."""
        result = random_gen.normal(mean, stddev)
        assert isinstance(result, float)
        # Normal distribution can have any value, no direct assert

    @pytest.mark.parametrize("mean", [1.0, 5.0, 10.0])
    def test_poisson(self, random_gen, mean):
        """Test Poisson distribution."""
        for _ in range(1000):
            result = random_gen.poisson(mean)
            assert result >= 0

    @pytest.mark.parametrize("shape, scale", [(2.0, 1.0), (5.0, 2.0)])
    def test_weibull(self, random_gen, shape, scale):
        """Test Weibull distribution."""
        for _ in range(1000):
            result = random_gen.weibull(shape, scale)
            assert result >= 0

    @pytest.mark.parametrize("lower, mode, upper", [(0.0, 0.5, 1.0), (1.0, 1.5, 2.0)])
    def test_tri(self, random_gen, lower, mode, upper):
        """Test triangular distribution."""
        for _ in range(1000):
            result = random_gen.tri(lower, mode, upper)
            assert lower <= result <= upper

    def _calc_mean(self, samples):
        """Calculate sample mean"""
        return sum(samples) / len(samples)

    def _calc_variance(self, samples):
        """Calculate sample variance"""
        mean = self._calc_mean(samples)
        return sum((x - mean) ** 2 for x in samples) / len(samples)

    def _calc_percentile(self, samples, p):
        """Calculate percentile

        Args:
            samples: List of numerical values
            p: Percentile value between 0 and 1
        """
        sorted_samples = sorted(samples)
        k = (len(sorted_samples) - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_samples[int(k)]
        d0 = sorted_samples[int(f)] * (c - k)
        d1 = sorted_samples[int(c)] * (k - f)
        return d0 + d1

    def _is_approximately_equal(self, a, b, tolerance=0.1):
        """Check if two floating point numbers are approximately equal

        Args:
            a, b: Numbers to compare
            tolerance: Maximum allowed difference
        """
        return abs(a - b) <= tolerance

    def test_uni_distribution(self, random_gen):
        """Test properties of uniform distribution

        Checks:
        1. Range validation
        2. Mean approximation
        3. Uniformity across intervals
        """
        max_value = 100
        n_samples = 10000
        samples = [random_gen.uni(max_value) for _ in range(n_samples)]

        # Check value range
        assert all(0 <= x <= max_value for x in samples)

        # Check if mean is close to theoretical value
        theoretical_mean = max_value / 2
        sample_mean = self._calc_mean(samples)
        assert self._is_approximately_equal(sample_mean, theoretical_mean, max_value * 0.05)

        # Check uniformity: divide range into 10 intervals and verify sample count in each
        interval_size = max_value / 10
        intervals = [0] * 10
        for x in samples:
            interval_idx = min(9, int(x / interval_size))
            intervals[interval_idx] += 1

        expected_count = n_samples / 10
        assert all(abs(count - expected_count) < expected_count * 0.2 for count in intervals)

    def test_normal_distribution(self, random_gen):
        """Test properties of normal distribution

        Checks:
        1. Mean and standard deviation
        2. Symmetry
        3. 68-95-99.7 rule
        """
        mean, stddev = 0.0, 1.0
        n_samples = 10000
        samples = [random_gen.normal(mean, stddev) for _ in range(n_samples)]

        # Check mean and standard deviation
        sample_mean = self._calc_mean(samples)
        sample_variance = self._calc_variance(samples)
        sample_stddev = math.sqrt(sample_variance)

        assert self._is_approximately_equal(sample_mean, mean, 0.1)
        assert self._is_approximately_equal(sample_stddev, stddev, 0.1)

        # Check symmetry
        median = self._calc_percentile(samples, 0.5)
        assert self._is_approximately_equal(median, mean, 0.1)

        # Check 68-95-99.7 rule
        sorted_samples = sorted(samples)
        count_1sigma = sum(1 for x in samples if abs(x - mean) <= stddev)
        count_2sigma = sum(1 for x in samples if abs(x - mean) <= 2 * stddev)
        count_3sigma = sum(1 for x in samples if abs(x - mean) <= 3 * stddev)

        assert abs(count_1sigma / n_samples - 0.68) < 0.05
        assert abs(count_2sigma / n_samples - 0.95) < 0.05
        assert abs(count_3sigma / n_samples - 0.997) < 0.05

    def test_exponential_distribution(self, random_gen):
        """Test properties of exponential distribution

        Checks:
        1. Range validation
        2. Mean and variance
        3. Memoryless property
        """
        rate = 1.0
        n_samples = 10000
        samples = [random_gen.exp(rate) for _ in range(n_samples)]

        # Check value range
        assert all(x >= 0 for x in samples)

        # Check if mean is close to theoretical value 1/rate
        theoretical_mean = 1 / rate
        sample_mean = self._calc_mean(samples)
        assert self._is_approximately_equal(sample_mean, theoretical_mean, 0.1)

        # Check if variance is close to theoretical value 1/rate^2
        theoretical_variance = 1 / (rate * rate)
        sample_variance = self._calc_variance(samples)
        assert self._is_approximately_equal(sample_variance, theoretical_variance, 0.2)

        # Check memoryless property: P(X > s + t | X > s) = P(X > t)
        s, t = 1.0, 1.0
        count_greater_s = sum(1 for x in samples if x > s)
        count_greater_s_plus_t = sum(1 for x in samples if x > s + t)
        count_greater_t = sum(1 for x in samples if x > t)

        if count_greater_s > 0:
            conditional_prob = count_greater_s_plus_t / count_greater_s
            direct_prob = count_greater_t / n_samples
            assert self._is_approximately_equal(conditional_prob, direct_prob, 0.1)

    def test_poisson_distribution(self, random_gen):
        """Test properties of Poisson distribution

        Checks:
        1. Integer and non-negative values
        2. Mean equals variance
        3. Mode approximation
        """
        mean = 5.0
        n_samples = 10000
        samples = [random_gen.poisson(mean) for _ in range(n_samples)]

        # Check value range (integer and non-negative)
        # actually they are not int, but floats
        assert all(int(x) == pytest.approx(x) and x >= 0 for x in samples)

        # Check if mean and variance are close to theoretical values
        sample_mean = self._calc_mean(samples)
        sample_variance = self._calc_variance(samples)

        assert self._is_approximately_equal(sample_mean, mean, 0.2)
        assert self._is_approximately_equal(sample_variance, mean, 0.2)

        # Check discrete properties
        counter = Counter(samples)
        total = sum(counter.values())

        # Check if mode is close to mean
        mode = max(counter.items(), key=lambda x: x[1])[0]
        assert abs(mode - mean) <= 1

    def test_beta_distribution(self, random_gen):
        """Test properties of Beta distribution

        Checks:
        1. Range validation
        2. Mean and variance
        """
        alpha, beta = 2.0, 5.0
        n_samples = 10000
        samples = [random_gen.beta(alpha, beta) for _ in range(n_samples)]

        # Check value range
        assert all(0 <= x <= 1 for x in samples)

        # Check if mean is close to theoretical value
        theoretical_mean = alpha / (alpha + beta)
        sample_mean = self._calc_mean(samples)
        assert self._is_approximately_equal(sample_mean, theoretical_mean, 0.05)

        # Check if variance is close to theoretical value
        theoretical_variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
        sample_variance = self._calc_variance(samples)
        assert self._is_approximately_equal(sample_variance, theoretical_variance, 0.1)

    def test_triangular_distribution(self, random_gen):
        """Test properties of triangular distribution

        Checks:
        1. Range validation
        2. Mean approximation
        3. Mode verification
        """
        lower, mode, upper = 0.0, 0.5, 1.0
        n_samples = 10000
        samples = [random_gen.tri(lower, mode, upper) for _ in range(n_samples)]

        # Check value range
        assert all(lower <= x <= upper for x in samples)

        # Check if mean is close to theoretical value
        theoretical_mean = (lower + mode + upper) / 3
        sample_mean = self._calc_mean(samples)
        assert self._is_approximately_equal(sample_mean, theoretical_mean, 0.05)

        # Check if mode is close to theoretical mode
        sorted_samples = sorted(samples)
        mid_point = sorted_samples[len(sorted_samples) // 2]
        assert self._is_approximately_equal(mid_point, mode, 0.1)

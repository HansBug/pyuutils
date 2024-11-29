import pytest

from pyuutils.base.random import RandomGenerator


@pytest.fixture
def random_gen():
    """Fixture to provide a RandomGenerator instance."""
    return RandomGenerator()


@pytest.mark.unittest
class TestRandomGeneratorWrapper:
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

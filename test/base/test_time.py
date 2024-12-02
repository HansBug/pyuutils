import time

import pytest
from hbutils.testing import OS

from pyuutils.base import TimeMonitor


# Optional: Performance profiling decorator
def profile_time_monitor(func):
    def wrapper(*args, **kwargs):
        import cProfile
        import pstats

        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)

        stats = pstats.Stats(profiler).sort_stats('cumulative')
        stats.print_stats()

        return result

    return wrapper


@pytest.mark.unittest
class TestBaseTime:
    def test_time_monitor_initialization(self):
        """Test TimeMonitor initialization with default and custom periods."""
        monitor1 = TimeMonitor()
        monitor2 = TimeMonitor(0.5)

        assert monitor1.get_events() == 0
        assert monitor2.get_events() == 0

    def test_time_monitor_events(self):
        monitor = TimeMonitor()
        start_time = time.time()

        assert monitor.get_events() == 0
        # assert monitor.event_rate() >= 1 << 24  # should be a huge number, represents inf

        monitor.has_passed()
        assert monitor.get_events() == 1
        if not OS.windows:
            assert monitor.event_rate() == pytest.approx(1 / (time.time() - start_time), rel=0.8)

    def test_time_monitor_reset_and_next(self):
        """Test reset and next methods."""
        monitor = TimeMonitor(0.1)

        # Simulate events
        for _ in range(10):
            time.sleep(0.01)
            monitor.has_passed()

        assert monitor.get_events() > 0

        # Test next method
        monitor.next()
        assert monitor.get_events() == 0

        # Test reset method
        monitor.reset()
        assert monitor.get_events() == 0

    def test_time_monitor_performance(self):
        """
        Test time monitor's performance and overhead.

        This test ensures that the time monitor doesn't introduce
        significant performance overhead.
        """
        import time

        start_time = time.time()
        monitor = TimeMonitor(1.0)

        # Simulate high-frequency events
        for _ in range(10000):
            monitor.has_passed()

        total_time = time.time() - start_time
        assert total_time < 0.5, f"Performance test took too long: {total_time}s"

    def test_time_monitor_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very short period
        monitor1 = TimeMonitor(0.0001)  # 0.1ms

        # Very long period
        monitor2 = TimeMonitor(10.0)

        # Ensure no exceptions are raised
        for _ in range(100):
            monitor1.has_passed()
            monitor2.has_passed()

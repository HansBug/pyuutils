from unittest import skipUnless
from unittest.mock import patch

import pytest
from hbutils.testing import OS

from pyuutils.base.platform import (
    MemInfo, ProcInfo, get_os_error, get_memory_info,
    init_process_info, get_process_info, get_process_info_max
)


@pytest.fixture
def sample_meminfo():
    return MemInfo(
        phys_total=16777216,  # 16GB
        phys_avail=8388608,  # 8GB
        phys_cache=2097152,  # 2GB
        swap_total=4194304,  # 4GB
        swap_avail=4194304,  # 4GB
        virt_total=20971520,  # 20GB
        virt_avail=12582912,  # 12GB
    )


@pytest.fixture
def sample_procinfo():
    return ProcInfo(
        mem_virt=1048576,  # 1GB
        mem_work=524288,  # 512MB
        mem_swap=0,  # 0MB
        time_user=1000,  # 1 second
        time_sys=500,  # 0.5 second
        time_real=2000,  # 2 seconds
    )


@pytest.mark.unittest
class TestPlatform:
    def test_meminfo_dataclass(self):
        info = MemInfo()
        assert info.phys_total == 0
        assert info.phys_avail == 0
        assert info.phys_cache == 0
        assert info.swap_total == 0
        assert info.swap_avail == 0
        assert info.virt_total == 0
        assert info.virt_avail == 0

    def test_procinfo_dataclass(self):
        info = ProcInfo()
        assert info.mem_virt == 0
        assert info.mem_work == 0
        assert info.mem_swap == 0
        assert info.time_user == 0
        assert info.time_sys == 0
        assert info.time_real == 0

    @skipUnless(not OS.windows, 'Non-windows required')
    @pytest.mark.parametrize(['code', 'message'], [
        # (-2, 'Unknown error -2'),
        # (-1, 'Unknown error -1'),
        # (0, 'Success'),
        (1, 'Operation not permitted'),
        (2, 'No such file or directory'),
        (3, 'No such process'),
        (4, 'Interrupted system call'),
        # (5, 'Input/output error'),
        # (6, 'No such device or address'),
        (7, 'Argument list too long'),
        (8, 'Exec format error'),
        (9, 'Bad file descriptor'),
        # (10, 'No child processes'),
        # (11, 'Resource temporarily unavailable'),
        # (12, 'Cannot allocate memory'),
        (13, 'Permission denied'),
        (14, 'Bad address'),
        (15, 'Block device required')
    ])
    def test_get_os_error_non_windows(self, code, message):
        error_msg = get_os_error(code)
        assert isinstance(error_msg, str)
        assert error_msg == message

    @skipUnless(OS.windows, 'Windows required')
    @pytest.mark.parametrize(['code', 'message'], [
        (1, 'Incorrect function.'),
        (2, 'The system cannot find the file specified.'),
        (3, 'The system cannot find the path specified.'),
        (4, 'The system cannot open the file.'),
        (7, 'The storage control blocks were destroyed.'),
        (8, 'Not enough memory resources are available to process this command.'),
        (9, 'The storage control block address is invalid.'),
        (13, 'The data is invalid.'),
        (14, 'Not enough memory resources are available to complete this operation.'),
        (15, 'The system cannot find the drive specified.'),
    ])
    def test_get_os_error_windows(self, code, message):
        error_msg = get_os_error(code)
        assert isinstance(error_msg, str)
        assert error_msg == message
        # assert error_msg.rstrip() == message  # TODO: optimize the C code, we need to process \r\n linewrap

    def test_get_memory_info_run(self):
        info = get_memory_info()
        assert isinstance(info, MemInfo)

    @patch('pyuutils.base.platform._c_base_getMemInfo')
    def test_get_memory_info(self, mock_get_meminfo, sample_meminfo):
        def mock_impl(info):
            info.phys_total = sample_meminfo.phys_total
            info.phys_avail = sample_meminfo.phys_avail
            info.phys_cache = sample_meminfo.phys_cache
            info.swap_total = sample_meminfo.swap_total
            info.swap_avail = sample_meminfo.swap_avail
            info.virt_total = sample_meminfo.virt_total
            info.virt_avail = sample_meminfo.virt_avail

        mock_get_meminfo.side_effect = mock_impl
        info = get_memory_info()
        assert isinstance(info, MemInfo)
        assert info.phys_total == sample_meminfo.phys_total
        assert info.phys_avail == sample_meminfo.phys_avail
        assert info.phys_cache == sample_meminfo.phys_cache
        assert info.swap_total == sample_meminfo.swap_total
        assert info.swap_avail == sample_meminfo.swap_avail
        assert info.virt_total == sample_meminfo.virt_total
        assert info.virt_avail == sample_meminfo.virt_avail

    def test_init_process_info_run(self):
        init_process_info()

    @patch('pyuutils.base.platform._c_base_initProcInfo')
    def test_init_process_info(self, mock_init):
        init_process_info()
        mock_init.assert_called_once()

    def test_get_process_info_run(self):
        info = get_process_info()
        assert isinstance(info, ProcInfo)

    @patch('pyuutils.base.platform._c_base_getProcInfo')
    def test_get_process_info(self, mock_get_procinfo, sample_procinfo):
        def mock_impl(info):
            info.mem_virt = sample_procinfo.mem_virt
            info.mem_work = sample_procinfo.mem_work
            info.mem_swap = sample_procinfo.mem_swap
            info.time_user = sample_procinfo.time_user
            info.time_sys = sample_procinfo.time_sys
            info.time_real = sample_procinfo.time_real

        mock_get_procinfo.side_effect = mock_impl
        info = get_process_info()
        assert isinstance(info, ProcInfo)
        assert info.mem_virt == sample_procinfo.mem_virt
        assert info.mem_work == sample_procinfo.mem_work
        assert info.mem_swap == sample_procinfo.mem_swap
        assert info.time_user == sample_procinfo.time_user
        assert info.time_sys == sample_procinfo.time_sys
        assert info.time_real == sample_procinfo.time_real

    def test_get_process_info_max_run(self):
        info = get_process_info_max()
        assert isinstance(info, ProcInfo)

    @patch('pyuutils.base.platform._c_base_getProcInfoMax')
    def test_get_process_info_max(self, mock_get_procinfo_max, sample_procinfo):
        def mock_impl(info):
            info.mem_virt = sample_procinfo.mem_virt * 2
            info.mem_work = sample_procinfo.mem_work * 2
            info.mem_swap = sample_procinfo.mem_swap
            info.time_user = sample_procinfo.time_user * 2
            info.time_sys = sample_procinfo.time_sys * 2
            info.time_real = sample_procinfo.time_real * 2

        mock_get_procinfo_max.side_effect = mock_impl
        info = get_process_info_max()
        assert isinstance(info, ProcInfo)
        assert info.mem_virt == sample_procinfo.mem_virt * 2
        assert info.mem_work == sample_procinfo.mem_work * 2
        assert info.mem_swap == sample_procinfo.mem_swap
        assert info.time_user == sample_procinfo.time_user * 2
        assert info.time_sys == sample_procinfo.time_sys * 2
        assert info.time_real == sample_procinfo.time_real * 2

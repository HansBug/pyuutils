#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <base/platform.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_base_platform, m) {
    m.doc() = "Python bindings for UUtils/include/base/platform.h functions";

    // Bind meminfo_t struct
    py::class_<meminfo_t>(m, "_c_meminfo_t")
        .def(py::init<>())
        .def_readwrite("phys_total", &meminfo_t::phys_total,
            "Total physical RAM in kB")
        .def_readwrite("phys_avail", &meminfo_t::phys_avail,
            "Available physical RAM in kB")
        .def_readwrite("phys_cache", &meminfo_t::phys_cache,
            "Physical RAM cache in kB")
        .def_readwrite("swap_total", &meminfo_t::swap_total,
            "Total swap space in kB")
        .def_readwrite("swap_avail", &meminfo_t::swap_avail,
            "Available swap space in kB")
        .def_readwrite("virt_total", &meminfo_t::virt_total,
            "Total virtual memory in kB")
        .def_readwrite("virt_avail", &meminfo_t::virt_avail,
            "Available virtual memory in kB");

    // Bind procinfo_t struct
    py::class_<procinfo_t>(m, "_c_procinfo_t")
        .def(py::init<>())
        .def_readwrite("mem_virt", &procinfo_t::mem_virt,
            "Virtual memory configuration in kB")
        .def_readwrite("mem_work", &procinfo_t::mem_work,
            "Working memory configuration in kB")
        .def_readwrite("mem_swap", &procinfo_t::mem_swap,
            "Swap memory configuration in kB")
        .def_readwrite("time_user", &procinfo_t::time_user,
            "User CPU time usage in milliseconds")
        .def_readwrite("time_sys", &procinfo_t::time_sys,
            "System CPU time usage in milliseconds")
        .def_readwrite("time_real", &procinfo_t::time_real,
            "Real time usage in milliseconds");

    m.def("_c_oserror", &oserror, py::arg("error_code"),
        "Get OS-specific error description for given error code\n\n"
        ":param error_code: The error code to get description for\n"
        ":type error_code: int\n"
        ":return: Error description string\n"
        ":rtype: str");

    m.def("_c_base_getMemInfo", [](py::object info) {
        meminfo_t native_info;
        base_getMemInfo(&native_info);
        info.attr("phys_total") = native_info.phys_total;
        info.attr("phys_avail") = native_info.phys_avail;
        info.attr("phys_cache") = native_info.phys_cache;
        info.attr("swap_total") = native_info.swap_total;
        info.attr("swap_avail") = native_info.swap_avail;
        info.attr("virt_total") = native_info.virt_total;
        info.attr("virt_avail") = native_info.virt_avail;
    }, py::arg("info"),
       "Get hosting machine memory information\n\n"
       ":param info: MemInfo object to store the information\n"
       ":type info: MemInfo");

    m.def("_c_base_initProcInfo", &base_initProcInfo,
        "Initialize the process information gathering");

    m.def("_c_base_getProcInfo", [](py::object info) {
        procinfo_t native_info;
        base_getProcInfo(&native_info);
        info.attr("mem_virt") = native_info.mem_virt;
        info.attr("mem_work") = native_info.mem_work;
        info.attr("mem_swap") = native_info.mem_swap;
        info.attr("time_user") = native_info.time_user;
        info.attr("time_sys") = native_info.time_sys;
        info.attr("time_real") = native_info.time_real;
    }, py::arg("info"),
       "Get current process memory and time consumption sample\n\n"
       ":param info: ProcInfo object to store the information\n"
       ":type info: ProcInfo");

    m.def("_c_base_getProcInfoMax", [](py::object info) {
        procinfo_t native_info;
        base_getProcInfoMax(&native_info);
        info.attr("mem_virt") = native_info.mem_virt;
        info.attr("mem_work") = native_info.mem_work;
        info.attr("mem_swap") = native_info.mem_swap;
        info.attr("time_user") = native_info.time_user;
        info.attr("time_sys") = native_info.time_sys;
        info.attr("time_real") = native_info.time_real;
    }, py::arg("info"),
       "Get current process memory and time consumption sample and store maximum values\n\n"
       ":param info: ProcInfo object to store the information\n"
       ":type info: ProcInfo");
}

#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>
#include <base/time.hpp>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_base_time, m) {
    m.doc() = "Python bindings for base/time.hpp";

    py::class_<base::time_monitor>(m, "_CTimeMonitor")
        .def(py::init<double>(), py::arg("period_in_seconds") = 1.0,
             "Initialize the time monitor\n\n"
             ":param period_in_seconds: The period to monitor in seconds\n"
             ":type period_in_seconds: float")
        .def("get_events", &base::time_monitor::get_events,
             "Get the number of events registered for the current period\n\n"
             ":return: Number of events\n"
             ":rtype: int")
        .def("event_rate", &base::time_monitor::event_rate,
             "Compute the number of events per second\n\n"
             ":return: Event rate\n"
             ":rtype: int")
        .def("has_passed", &base::time_monitor::has_passed,
             "Account for an event and check if the specified time period has passed\n\n"
             ":return: True if the period has passed, False otherwise\n"
             ":rtype: bool")
        .def("next", &base::time_monitor::next,
             "Prepare for the next period")
        .def("reset", &base::time_monitor::reset,
             "Reset the monitor for another/unrelated performance measure");

#ifdef TEST_TIME_MONITOR
    py::class_<base::time_monitor>(m, "_CTimeMonitor")
        .def("get_delay_rate", &base::time_monitor::get_delay_rate,
             "Get the delay rate (only available in TEST_TIME_MONITOR mode)\n\n"
             ":return: Delay rate\n"
             ":rtype: int");
#endif
}

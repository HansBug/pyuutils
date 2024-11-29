#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <base/random.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_base_random, m) {
    m.doc() = "Python bindings for RandomGenerator class";

    py::class_<RandomGenerator>(m, "_CRandomGenerator")
        .def(py::init<>(), "Initialize a new RandomGenerator instance.")
        .def_static("set_seed", &RandomGenerator::set_seed, py::arg("seed"),
                    "Set globally shared random seed.\n\n"
                    ":param seed: Seed value\n"
                    ":type seed: int")
        .def("seed", &RandomGenerator::seed, py::arg("seed"),
             "Set random seed for this generator instance.\n\n"
             ":param seed: Seed value\n"
             ":type seed: int")
        .def("uni", py::overload_cast<uint32_t>(&RandomGenerator::uni), py::arg("max"),
             "Generate a random unsigned integer in the range [0, max].\n\n"
             ":param max: Maximum value\n"
             ":type max: int\n"
             ":return: Random unsigned integer\n"
             ":rtype: int")
        .def("uni", py::overload_cast<uint32_t, uint32_t>(&RandomGenerator::uni), py::arg("from"), py::arg("till"),
             "Generate a random unsigned integer in the range [from, till].\n\n"
             ":param from: Inclusive lower bound\n"
             ":type from: int\n"
             ":param till: Inclusive upper bound\n"
             ":type till: int\n"
             ":return: Random unsigned integer\n"
             ":rtype: int")
        .def("uni", py::overload_cast<int32_t, int32_t>(&RandomGenerator::uni), py::arg("from"), py::arg("till"),
             "Generate a random signed integer in the range [from, till].\n\n"
             ":param from: Inclusive lower bound\n"
             ":type from: int\n"
             ":param till: Inclusive upper bound\n"
             ":type till: int\n"
             ":return: Random signed integer\n"
             ":rtype: int")
        .def("uni_1", &RandomGenerator::uni_1,
             "Generate a random double in the range [0, 1).\n\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("uni_r", py::overload_cast<double>(&RandomGenerator::uni_r), py::arg("max"),
             "Generate a random double in the range [0, max).\n\n"
             ":param max: Exclusive upper bound\n"
             ":type max: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("uni_r", py::overload_cast<double, double>(&RandomGenerator::uni_r), py::arg("from"), py::arg("till"),
             "Generate a random double in the range [from, till).\n\n"
             ":param from: Inclusive lower bound\n"
             ":type from: float\n"
             ":param till: Exclusive upper bound\n"
             ":type till: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("exp", &RandomGenerator::exp, py::arg("rate"),
             "Generate a random double following an exponential distribution.\n\n"
             ":param rate: Rate parameter\n"
             ":type rate: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("arcsine", &RandomGenerator::arcsine, py::arg("minv"), py::arg("maxv"),
             "Generate a random double following an arcsine distribution.\n\n"
             ":param minv: Minimum value\n"
             ":type minv: float\n"
             ":param maxv: Maximum value\n"
             ":type maxv: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("beta", &RandomGenerator::beta, py::arg("alpha"), py::arg("beta"),
             "Generate a random double following a beta distribution.\n\n"
             ":param alpha: Alpha parameter\n"
             ":type alpha: float\n"
             ":param beta: Beta parameter\n"
             ":type beta: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("gamma", &RandomGenerator::gamma, py::arg("shape"), py::arg("scale"),
             "Generate a random double following a gamma distribution.\n\n"
             ":param shape: Shape parameter\n"
             ":type shape: float\n"
             ":param scale: Scale parameter\n"
             ":type scale: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("normal", &RandomGenerator::normal, py::arg("mean"), py::arg("stddev"),
             "Generate a random double following a normal distribution.\n\n"
             ":param mean: Mean value\n"
             ":type mean: float\n"
             ":param stddev: Standard deviation\n"
             ":type stddev: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("poisson", &RandomGenerator::poisson, py::arg("mean"),
             "Generate a random double following a Poisson distribution.\n\n"
             ":param mean: Mean value\n"
             ":type mean: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("weibull", &RandomGenerator::weibull, py::arg("shape"), py::arg("scale"),
             "Generate a random double following a Weibull distribution.\n\n"
             ":param shape: Shape parameter\n"
             ":type shape: float\n"
             ":param scale: Scale parameter\n"
             ":type scale: float\n"
             ":return: Random double\n"
             ":rtype: float")
        .def("tri", &RandomGenerator::tri, py::arg("lower"), py::arg("mode"), py::arg("upper"),
             "Generate a random double following a triangular distribution.\n\n"
             ":param lower: Lower bound\n"
             ":type lower: float\n"
             ":param mode: Mode value\n"
             ":type mode: float\n"
             ":param upper: Upper bound\n"
             ":type upper: float\n"
             ":return: Random double\n"
             ":rtype: float");
}

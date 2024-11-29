#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <hash/compute.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_hash, m) {
    m.doc() = "Python bindings for UUtils/include/hash/compute.h functions";

    m.def("_c_hash_compute", [](py::buffer data, uint32_t initval) {
        py::buffer_info info = data.request();
        return hash_compute(info.ptr, info.size * info.itemsize, initval);
    }, "Compute hash for arbitrary data",
       py::arg("data"), py::arg("initval") = 0);

    m.def("_c_hash_compute_str", [](const std::string& str, uint32_t initval) {
        return hash_computeStr(str.c_str(), initval);
    }, "Compute hash for a string",
       py::arg("str"), py::arg("initval") = 0);

    m.def("_c_hash_compute3", &hash_compute3, "Compute hash from 3 previous hash values",
          py::arg("a"), py::arg("b"), py::arg("c"));
}

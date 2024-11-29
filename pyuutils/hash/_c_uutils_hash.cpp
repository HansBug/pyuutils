#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <hash/compute.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_hash, m) {
    m.doc() = "Python bindings for UUtils/include/hash/compute.h functions";

    m.def("_c_hash_compute", [](py::buffer data, hashint_t initval) {
        py::buffer_info info = data.request();
        return hash_compute(info.ptr, info.size * info.itemsize, initval);
    }, "Compute 32-bit hash for arbitrary data\n\n"
       ":param data: Input data\n"
       ":type data: buffer\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: 32-bit hash value\n"
       ":rtype: int",
       py::arg("data"), py::arg("initval") = 0);

    m.def("_c_hash_compute_str", [](const std::string& str, uint32_t initval) {
        return hash_computeStr(str.c_str(), initval);
    }, "Compute hash for a string\n\n"
       ":param str: Input string\n"
       ":type str: str\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int",
       py::arg("str"), py::arg("initval") = 0);

    m.def("_c_hash_compute3", &hash_compute3,
        "Compute a new hash from 3 previous hash values\n\n"
        ":param a: First hash value\n"
        ":type a: int\n"
        ":param b: Second hash value\n"
        ":type b: int\n"
        ":param c: Third hash value\n"
        ":type c: int\n"
        ":return: Combined hash value\n"
        ":rtype: int",
        py::arg("a"), py::arg("b"), py::arg("c"));
}

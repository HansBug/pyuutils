#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <hash/compute.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_hash, m) {
    m.doc() = "Python bindings for UUtils/include/hash/compute.h functions";

    m.def("_c_hash_murmur2_U8", [](py::bytes data, size_t length, hashint_t initval) {
        std::string data_str = data;
        return hash_murmur2_U8(reinterpret_cast<const uint8_t*>(data_str.data()), length, initval);
    }, py::arg("data"), py::arg("length"), py::arg("initval"),
       "Compute hash value using Murmur2 for uint8_t data\n\n"
       ":param data: Input data\n"
       ":type data: bytes\n"
       ":param length: Number of bytes to read\n"
       ":type length: int\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeU32", [](const std::vector<uint32_t>& data, hashint_t initval) {
        return hash_computeU32(data.data(), data.size(), initval);
    }, py::arg("data"), py::arg("initval"),
       "Compute hash value for uint32_t data\n\n"
       ":param data: Input data\n"
       ":type data: List[int]\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeU16", [](const std::vector<uint16_t>& data, hashint_t initval) {
        return hash_computeU16(data.data(), data.size(), initval);
    }, py::arg("data"), py::arg("initval"),
       "Compute hash value for uint16_t data\n\n"
       ":param data: Input data\n"
       ":type data: List[int]\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeI32", [](const std::vector<int32_t>& data, hashint_t initval) {
        return hash_computeI32(data.data(), data.size(), initval);
    }, py::arg("data"), py::arg("initval"),
       "Compute hash value for int32_t data\n\n"
       ":param data: Input data\n"
       ":type data: List[int]\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeI16", [](const std::vector<int16_t>& data, hashint_t initval) {
        return hash_computeI16(data.data(), data.size(), initval);
    }, py::arg("data"), py::arg("initval"),
       "Compute hash value for int16_t data\n\n"
       ":param data: Input data\n"
       ":type data: List[int]\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeI8", [](py::bytes data, hashint_t initval) {
        std::string data_str = data;
        return hash_computeI8(reinterpret_cast<const int8_t*>(data_str.data()), data_str.size(), initval);
    }, py::arg("data"), py::arg("initval"),
       "Compute hash value for int8_t data\n\n"
       ":param data: Input data\n"
       ":type data: bytes\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_computeStr", [](const std::string& str, hashint_t initval) {
        return hash_computeStr(str.c_str(), initval);
    }, py::arg("str"), py::arg("initval"),
       "Compute hash value for a string\n\n"
       ":param str: Input string\n"
       ":type str: str\n"
       ":param initval: Initial value for hash computation\n"
       ":type initval: int\n"
       ":return: Computed hash value\n"
       ":rtype: int");

    m.def("_c_hash_compute3", &hash_compute3, py::arg("a"), py::arg("b"), py::arg("c"),
       "Compute a new hash from 3 previous hash values\n\n"
       ":param a: First hash value\n"
       ":type a: int\n"
       ":param b: Second hash value\n"
       ":type b: int\n"
       ":param c: Third hash value\n"
       ":type c: int\n"
       ":return: Combined hash value\n"
       ":rtype: int");
}

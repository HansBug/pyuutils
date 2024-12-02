#include <pybind11/pybind11.h>
#include <base/relation.h>

namespace py = pybind11;

PYBIND11_MODULE(_c_uutils_base_relation, m) {
    m.doc() = "Python bindings for partial order relations between sets";

    py::enum_<relation_t>(m, "_CRelation", "Enum for base relations between sets")
        .value("_c_DIFFERENT", base_DIFFERENT, "Incomparable or not (set1 <= set2) depending on exactness")
        .value("_c_SUPERSET", base_SUPERSET, "Set1 is a superset of set2 or not used")
        .value("_c_GREATER", base_GREATER, "Same as superset")
        .value("_c_SUBSET", base_SUBSET, "Set1 is a subset of set2 or set1 <= set2 depending on exactness")
        .value("_c_LESS", base_LESS, "Same as subset")
        .value("_c_EQUAL", base_EQUAL, "Set1 is equal to set2 or not used")
        .export_values();

    m.def("_c_sym_relation", &base_symRelation, py::arg("rel"),
         "Return the symmetric of a relation (invert subset and superset bits)");

    m.def("_c_sub2super", &base_sub2super, py::arg("rel"),
         "Convert a subset relation to a superset relation");

    m.def("_c_super2sub", &base_super2sub, py::arg("rel"),
         "Convert a superset relation to a subset relation");
}

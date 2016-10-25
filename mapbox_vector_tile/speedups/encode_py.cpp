/**
 * (Python -> C++) binding
 *
 */


#include <Python.h>


static PyObject *
geo_encode(PyObject *self, PyObject *args)
{
    const char *command;

    return Py_BuildValue("s", "foo");
}


static PyMethodDef speedupsMethods[] = {
    {"geo_encode",  geo_encode, METH_VARARGS, "Encodes a list of coordinates"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initspeedups(void)
{
    (void) Py_InitModule("speedups", speedupsMethods);
}

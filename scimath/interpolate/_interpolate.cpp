/*
    (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
    All rights reserved.

    This software is provided without warranty under the terms of the BSD
    license included in LICENSE.txt and may be redistributed only under
    the conditions described in the aforementioned license. The license
    is also available online at http://www.enthought.com/licenses/BSD.txt

    Thanks for using Enthought open source!
*/

#include "Python.h"
#include <stdlib.h>

#include "interpolate.h"
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/arrayobject.h"


using namespace std;

extern "C" {

static PyObject* linear_method(PyObject*self, PyObject* args, PyObject* kywds)
{
    const char *kwlist[] = {"x","y","new_x","new_y", NULL};
    PyObject *py_x, *py_y, *py_new_x, *py_new_y;
    py_x = py_y = py_new_x = py_new_y = NULL;
    PyObject *arr_x, *arr_y, *arr_new_x, *arr_new_y;
    arr_x = arr_y = arr_new_x = arr_new_y = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kywds, "OOOO:linear_dddd",
                                     const_cast<char**>(kwlist), &py_x, &py_y,
                                     &py_new_x, &py_new_y))
       return NULL;
    arr_x = PyArray_FROMANY(py_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_x) {
        PyErr_SetString(PyExc_ValueError, "x must be a 1-D array of floats");
        goto fail;
    }
    arr_y = PyArray_FROMANY(py_y, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_y) {
        PyErr_SetString(PyExc_ValueError, "y must be a 1-D array of floats");
        goto fail;
    }
    arr_new_x = PyArray_FROMANY(py_new_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_new_x) {
        PyErr_SetString(PyExc_ValueError,
                        "new_x must be a 1-D array of floats");
        goto fail;
    }
    arr_new_y = PyArray_FROMANY(py_new_y, NPY_DOUBLE, 1, 1,
                                NPY_ARRAY_INOUT_ARRAY);
    if (!arr_new_y) {
        PyErr_SetString(PyExc_ValueError,
                        "new_y must be a 1-D array of floats");
        goto fail;
    }

    linear((double*)PyArray_DATA((PyArrayObject*)arr_x),
           (double*)PyArray_DATA((PyArrayObject*)arr_y),
           PyArray_DIM((PyArrayObject*)arr_x, 0),
           (double*)PyArray_DATA((PyArrayObject*)arr_new_x),
           (double*)PyArray_DATA((PyArrayObject*)arr_new_y),
           PyArray_DIM((PyArrayObject*)arr_new_x, 0));

    Py_DECREF(arr_x);
    Py_DECREF(arr_y);
    Py_DECREF(arr_new_x);
    Py_DECREF(arr_new_y);

    Py_RETURN_NONE;

fail:
    Py_XDECREF(arr_x);
    Py_XDECREF(arr_y);
    Py_XDECREF(arr_new_x);
    Py_XDECREF(arr_new_y);
    return NULL;
}

static PyObject* loginterp_method(PyObject*self, PyObject* args,
                                  PyObject* kywds)
{
    const char *kwlist[] = {"x","y","new_x","new_y", NULL};
    PyObject *py_x, *py_y, *py_new_x, *py_new_y;
    py_x = py_y = py_new_x = py_new_y = NULL;
    PyObject *arr_x, *arr_y, *arr_new_x, *arr_new_y;
    arr_x = arr_y = arr_new_x = arr_new_y = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kywds, "OOOO:loginterp_dddd",
                                     const_cast<char **>(kwlist), &py_x, &py_y,
                                     &py_new_x, &py_new_y))
       return NULL;
    arr_x = PyArray_FROMANY(py_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_x) {
        PyErr_SetString(PyExc_ValueError, "x must be a 1-D array of floats");
        goto fail;
    }
    arr_y = PyArray_FROMANY(py_y, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_y) {
        PyErr_SetString(PyExc_ValueError, "y must be a 1-D array of floats");
        goto fail;
    }
    arr_new_x = PyArray_FROMANY(py_new_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_new_x) {
        PyErr_SetString(PyExc_ValueError,
                        "new_x must be a 1-D array of floats");
        goto fail;
    }
    arr_new_y = PyArray_FROMANY(py_new_y, NPY_DOUBLE, 1, 1,
                                NPY_ARRAY_INOUT_ARRAY);
    if (!arr_new_y) {
        PyErr_SetString(PyExc_ValueError,
                        "new_y must be a 1-D array of floats");
        goto fail;
    }

    loginterp((double*)PyArray_DATA((PyArrayObject*)arr_x),
              (double*)PyArray_DATA((PyArrayObject*)arr_y),
              PyArray_DIM((PyArrayObject*)arr_x,0),
              (double*)PyArray_DATA((PyArrayObject*)arr_new_x),
              (double*)PyArray_DATA((PyArrayObject*)arr_new_y),
              PyArray_DIM((PyArrayObject*)arr_new_x,0));

    Py_DECREF(arr_x);
    Py_DECREF(arr_y);
    Py_DECREF(arr_new_x);
    Py_DECREF(arr_new_y);

    Py_RETURN_NONE;

fail:
    Py_XDECREF(arr_x);
    Py_XDECREF(arr_y);
    Py_XDECREF(arr_new_x);
    Py_XDECREF(arr_new_y);
    return NULL;
}

static PyObject* window_average_method(PyObject*self, PyObject* args,
                                       PyObject* kywds)
{
    const char *kwlist[] = {"x","y","new_x","new_y", NULL};
    PyObject *py_x, *py_y, *py_new_x, *py_new_y;
    py_x = py_y = py_new_x = py_new_y = NULL;
    PyObject *arr_x, *arr_y, *arr_new_x, *arr_new_y;
    arr_x = arr_y = arr_new_x = arr_new_y = NULL;
    double width;

    if (!PyArg_ParseTupleAndKeywords(args, kywds, "OOOOd:loginterp_dddd",
                                     const_cast<char **>(kwlist), &py_x, &py_y,
                                     &py_new_x, &py_new_y, &width))
       return NULL;
    arr_x = PyArray_FROMANY(py_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_x) {
        PyErr_SetString(PyExc_ValueError, "x must be a 1-D array of floats");
        goto fail;
    }
    arr_y = PyArray_FROMANY(py_y, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_y) {
        PyErr_SetString(PyExc_ValueError, "y must be a 1-D array of floats");
        goto fail;
    }
    arr_new_x = PyArray_FROMANY(py_new_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_new_x) {
        PyErr_SetString(PyExc_ValueError,
                        "new_x must be a 1-D array of floats");
        goto fail;
    }
    arr_new_y = PyArray_FROMANY(py_new_y, NPY_DOUBLE, 1, 1,
                                NPY_ARRAY_INOUT_ARRAY);
    if (!arr_new_y) {
        PyErr_SetString(PyExc_ValueError,
                        "new_y must be a 1-D array of floats");
        goto fail;
    }

    window_average((double*)PyArray_DATA((PyArrayObject*)arr_x),
                   (double*)PyArray_DATA((PyArrayObject*)arr_y),
                   PyArray_DIM((PyArrayObject*)arr_x,0),
                   (double*)PyArray_DATA((PyArrayObject*)arr_new_x),
                   (double*)PyArray_DATA((PyArrayObject*)arr_new_y),
                   PyArray_DIM((PyArrayObject*)arr_new_x,0), width);

    Py_DECREF(arr_x);
    Py_DECREF(arr_y);
    Py_DECREF(arr_new_x);
    Py_DECREF(arr_new_y);

    Py_RETURN_NONE;

fail:
    Py_XDECREF(arr_x);
    Py_XDECREF(arr_y);
    Py_XDECREF(arr_new_x);
    Py_XDECREF(arr_new_y);
    return NULL;
}

static PyObject* block_average_above_method(PyObject*self, PyObject* args,
                                            PyObject* kywds)
{
    const char *kwlist[] = {"x","y","new_x","new_y", NULL};
    PyObject *py_x, *py_y, *py_new_x, *py_new_y;
    py_x = py_y = py_new_x = py_new_y = NULL;
    PyObject *arr_x, *arr_y, *arr_new_x, *arr_new_y;
    arr_x = arr_y = arr_new_x = arr_new_y = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kywds, "OOOO:loginterp_dddd",
                                     const_cast<char **>(kwlist), &py_x, &py_y,
                                     &py_new_x, &py_new_y))
       return NULL;
    arr_x = PyArray_FROMANY(py_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_x) {
        PyErr_SetString(PyExc_ValueError, "x must be a 1-D array of floats");
        goto fail;
    }
    arr_y = PyArray_FROMANY(py_y, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_y) {
        PyErr_SetString(PyExc_ValueError, "y must be a 1-D array of floats");
        goto fail;
    }
    arr_new_x = PyArray_FROMANY(py_new_x, NPY_DOUBLE, 1, 1, NPY_ARRAY_IN_ARRAY);
    if (!arr_new_x) {
        PyErr_SetString(PyExc_ValueError,
                        "new_x must be a 1-D array of floats");
        goto fail;
    }
    arr_new_y = PyArray_FROMANY(py_new_y, NPY_DOUBLE, 1, 1,
                                NPY_ARRAY_INOUT_ARRAY);
    if (!arr_new_y) {
        PyErr_SetString(PyExc_ValueError,
                        "new_y must be a 1-D array of floats");
        goto fail;
    }

    block_average_above((double*)PyArray_DATA((PyArrayObject*)arr_x),
                        (double*)PyArray_DATA((PyArrayObject*)arr_y),
                        PyArray_DIM((PyArrayObject*)arr_x,0),
                        (double*)PyArray_DATA((PyArrayObject*)arr_new_x),
                        (double*)PyArray_DATA((PyArrayObject*)arr_new_y),
                        PyArray_DIM((PyArrayObject*)arr_new_x,0));

    Py_DECREF(arr_x);
    Py_DECREF(arr_y);
    Py_DECREF(arr_new_x);
    Py_DECREF(arr_new_y);

    Py_RETURN_NONE;

fail:
    Py_XDECREF(arr_x);
    Py_XDECREF(arr_y);
    Py_XDECREF(arr_new_x);
    Py_XDECREF(arr_new_y);
    return NULL;
}

static PyMethodDef interpolate_methods[] = {
    {"linear_dddd", (PyCFunction)linear_method,
     METH_VARARGS|METH_KEYWORDS, ""},
    {"loginterp_dddd", (PyCFunction)loginterp_method,
     METH_VARARGS|METH_KEYWORDS, ""},
    {"window_average_ddddd", (PyCFunction)window_average_method,
     METH_VARARGS|METH_KEYWORDS, ""},
    {"block_average_above_dddd", (PyCFunction)block_average_above_method,
     METH_VARARGS|METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC PyInit__interpolate(void)
{
    PyObject* m;
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_interpolate",
        "A few interpolation routines.\n",
        -1,
        interpolate_methods,
    };
    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;

    import_array();

    return m;
}

} // extern "C"

# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Provides functions that manipulate quaternions.

    Quaternions are frequently used to avoid 'gimbal lock' and/or 'twisting'
    when rotating polygons in 3D space.
"""

# Major library imports.
import numpy as np


def normq(quat):
    """
    Normalize a quaternion.

    """

    quat = np.asarray(quat)
    return quat / np.sqrt(np.dot(quat, quat))


def qmult(q1, q2):
    """
    Multiply two quaternions.

    """

    s1, v1 = q1[0], q1[1:]
    s2, v2 = q2[0], q2[1:]
    scalar = s1 * s2 - np.dot(v1, v2)
    vector = s2 * v1 + s1 * v2 + _crossv(v1, v2)[0]
    return np.hstack((scalar, vector))


def rotmat(q):
    """
    Transform a unit quaternion into its corresponding rotation matrix (to
    be applied on the right side).

    """

    w, x, y, z = q
    xx2 = 2 * x * x
    yy2 = 2 * y * y
    zz2 = 2 * z * z
    xy2 = 2 * x * y
    wz2 = 2 * w * z
    zx2 = 2 * z * x
    wy2 = 2 * w * y
    yz2 = 2 * y * z
    wx2 = 2 * w * x

    rmat = np.empty((3, 3), float)
    rmat[0, 0] = 1. - yy2 - zz2
    rmat[0, 1] = xy2 - wz2
    rmat[0, 2] = zx2 + wy2
    rmat[1, 0] = xy2 + wz2
    rmat[1, 1] = 1. - xx2 - zz2
    rmat[1, 2] = yz2 - wx2
    rmat[2, 0] = zx2 - wy2
    rmat[2, 1] = yz2 + wx2
    rmat[2, 2] = 1. - xx2 - yy2

    return rmat


def rotquat(vhat1, vhat2):
    """
    Compute the quaternion that rotates the normalized vector *vhat1* to *vhat2*.

    The quaternion is represented as a tuple (scalar part, vector part).

    """

    # Compute the bisector.
    bisector = vhat1 + vhat2

    # Handle the case where the bisector is an array of zeros.
    null_indices = np.nonzero(
        (bisector == np.array([0., 0., 0.])).all(axis=-1))
    index = 0

    while len(null_indices) > 0 and index < 3:
        unit_vector = np.zeros((1, 3))
        unit_vector[:, index] = 1.0
        bisector = _crossv(vhat1[null_indices],
                           np.repeat(unit_vector, len(null_indices)))
        null_indices = np.nonzero((bisector == np.array([0., 0., 0.])).all(
            axis=-1))
        index += 1

    # Normalize the bisector
    bisector = _normv(bisector)

    # Compute the scalar part
    cost2 = _dotv(vhat1, bisector)

    # Compute the vector part
    sint2v = _crossv(vhat1, bisector)

    # NOTE: This is an expanded version of the old version of numpy's
    # 'column_stack' function.
    tup = (cost2, np.transpose(sint2v))
    arrays = list(map(np.transpose, list(map(np.atleast_2d, tup))))
    return np.concatenate(arrays, 1)


def _crossv(vertices1, vertices2):
    """
    Perform the cross product on arrays of 3-vectors.

    """

    v10, v11, v12 = np.transpose(vertices1)
    v20, v21, v22 = np.transpose(vertices2)

    # NOTE: This is an expanded version of the old version of numpy's
    # 'column_stack' function.
    tup = (
        v11 * v22 - v12 * v21,
        v12 * v20 - v10 * v22,
        v10 * v21 - v11 * v20)
    arrays = list(map(np.transpose, list(map(np.atleast_2d, tup))))
    return np.concatenate(arrays, 1)


def _dotv(vertices1, vertices2):
    """
    Perform the dot product on arrays of 3-vectors.

    """

    return np.sum(vertices1 * vertices2, axis=-1)


def _normv(vertices):
    """
    Normalize an array of 3-vectors.

    """

    vertices = np.asarray(vertices)
    return vertices / np.sqrt(_dotv(vertices, vertices))[:, np.newaxis]

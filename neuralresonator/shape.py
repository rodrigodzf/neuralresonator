# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_shape.ipynb.

# %% auto 0
__all__ = ['generate_convex_shape', 'generate_convex_mesh']

# %% ../nbs/02_shape.ipynb 2
import random

import numpy as np
from .modal import MATERIALS, System
from skfem import MeshTri
from skimage.draw import polygon2mask

# %% ../nbs/02_shape.ipynb 4
def generate_convex_shape(n: int) -> np.ndarray:
    """
    This function was taken and adapted from https://stackoverflow.com/a/68602707

    Generate convex shappes according to Pavel Valtr's 1995 alogrithm. Ported from
    Sander Verdonschot's Java version, found here:
    https://cglab.ca/~sander/misc/ConvexGeneration/ValtrAlgorithm.java

    returns a numpy array of shape (n, 2)
    """

    # initialise random coordinates
    X_rand, Y_rand = np.sort(np.random.random(n)), np.sort(np.random.random(n))
    X_new, Y_new = np.zeros(n), np.zeros(n)

    # divide the interior points into two chains
    last_true = last_false = 0
    for i in range(1, n):
        if i != n - 1:
            if random.getrandbits(1):
                X_new[i] = X_rand[i] - X_rand[last_true]
                Y_new[i] = Y_rand[i] - Y_rand[last_true]
                last_true = i
            else:
                X_new[i] = X_rand[last_false] - X_rand[i]
                Y_new[i] = Y_rand[last_false] - Y_rand[i]
                last_false = i
        else:
            X_new[0] = X_rand[i] - X_rand[last_true]
            Y_new[0] = Y_rand[i] - Y_rand[last_true]
            X_new[i] = X_rand[last_false] - X_rand[i]
            Y_new[i] = Y_rand[last_false] - Y_rand[i]

    # randomly combine x and y and sort by polar angle
    np.random.shuffle(Y_new)
    vertices = np.stack((X_new, Y_new), axis=-1)
    vertices = vertices[np.argsort(np.arctan2(vertices[:, 1], vertices[:, 0]))]

    # arrange points end to end to form a polygon
    vertices = np.cumsum(vertices, axis=0)

    # center around the origin
    x_max, y_max = np.max(vertices[:, 0]), np.max(vertices[:, 1])
    vertices[:, 0] += ((x_max - np.min(vertices[:, 0])) / 2) - x_max
    vertices[:, 1] += ((y_max - np.min(vertices[:, 1])) / 2) - y_max

    return vertices


def generate_convex_mesh(
    n_points: int = 10,  # number of points in the convex shape
    n_refinement_steps: int = 3,  # number of refinement steps
) -> tuple[MeshTri, np.ndarray]:  # mesh and points in the normalized range [-1.0, 1.0]
    """
    Generate a 2D convex mesh
    """
    import triangle

    # convex mesh generates a mesh normalized to [-0.5, 0.5]
    points = generate_convex_shape(n_points) * 2
    tri = triangle.triangulate({"vertices": points}, "q")
    return (
        MeshTri(tri["vertices"].T, tri["triangles"].T).refined(n_refinement_steps),
        points,
    )
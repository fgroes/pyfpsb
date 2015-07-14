import numpy as np


def load_data():
    data_dtype = [("position", np.float32, 3), ("color", np.float32, 3)]
    data = np.zeros(9, dtype=data_dtype)
    depth1 = -0.5
    depth2 = +0.5
    data["position"] = [
       (0, -1, depth1),
       (1, 1, depth1),
       (-1, 1, depth1),
       (-1, -1, depth2),
       (1, -1, depth2),
       (0, 1, -1.0),
       (1, 0.5, -0.6),
       (0.5, 0, -0.6),
       (1, -0.5, -0.6)]
    data["color"] = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1)]
    indices = np.array([0, 1, 2, 5, 3, 4, 6, 7, 8], dtype=np.ushort)
    return data, indices


def load_cube():
    data_dtype = [("position", np.float32, 3), ("color", np.float32, 3)]
    data = np.zeros(8, dtype=data_dtype)
    data["position"] = [
       (-0.5, -0.5, -0.5),
       ( 0.5, -0.5, -0.5),
       (-0.5,  0.5, -0.5),
       ( 0.5,  0.5, -0.5),
       (-0.5, -0.5,  0.5),
       ( 0.5, -0.5,  0.5),
       (-0.5,  0.5,  0.5),
       ( 0.5,  0.5,  0.5)]
    data["color"] = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
        (0, 1, 1),
        (1, 0, 1),
        (0.1, 0.1, 0.1)]
    indices = np.array([
        0, 1, 2,
        1, 3, 2,
        4, 6, 5,
        5, 6, 7,
        0, 2, 4,
        2, 6, 4,
        1, 5, 3,
        3, 5, 7,
        2, 3, 6,
        3, 6, 7,
        0, 4, 1,
        1, 4, 5
    ], dtype=np.ushort)
    return data, indices

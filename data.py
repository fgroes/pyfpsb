import numpy as np


def load_data():
	#data = np.zeros(4, dtype=[("position", np.float32, 2), ("color", np.float32, 4)])
	depth1 = -0.5
	depth2 = +0.5
	data = np.array([
		+0, -1, depth1,
		+1, +0, +0,
		+1, +1, depth1,
		+0, +1, +0,
		-1, +1, depth1,
		+0, +0, +1,
		-1, -1, depth2,
		+0, +1, +0,
		+1, -1, depth2,
		+0, +0, +1,
		+0, +1, -1.0,
		+1, +0, +1,
		], dtype=np.float32)
	indices = np.array([0, 1, 2, 5, 3, 4], dtype=np.ushort)
	return data, indices

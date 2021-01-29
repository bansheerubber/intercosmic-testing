import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_sphere(ax, radius):
	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)

	x = radius * np.outer(np.cos(u), np.sin(v))
	y = radius * np.outer(np.sin(u), np.sin(v))
	z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

	elev = 0
	rot = 0
	ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.2)
	#calculate vectors for "vertical" circle
	a = np.array([-np.sin(elev / 180 * np.pi), 0, np.cos(elev / 180 * np.pi)])
	b = np.array([0, 1, 0])
	b = b * np.cos(rot) + np.cross(a, b) * np.sin(rot) + a * np.dot(a, b) * (1 - np.cos(rot))

	ax.plot(
		np.sin(u) * radius,
		np.cos(u) * radius,
		0,
		color='k',
		linestyle = 'dashed'
	)
	horiz_front = np.linspace(0, np.pi, 100)
	ax.plot(
		np.sin(horiz_front) * radius,
		np.cos(horiz_front) * radius,
		0,
		color='k'
	)

	vert_front = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
	ax.plot(
		(a[0] * np.sin(u) + b[0] * np.cos(u)) * radius,
		b[1] * np.cos(u) * radius,
		(a[2] * np.sin(u) + b[2] * np.cos(u)) * radius,
		color='k',
		linestyle = 'dashed'
	)

	ax.plot(
		(a[0] * np.sin(vert_front) + b[0] * np.cos(vert_front)) * radius,
		b[1] * np.cos(vert_front) * radius,
		(a[2] * np.sin(vert_front) + b[2] * np.cos(vert_front)) * radius,
		color='k'
	)

	ax.view_init(elev = elev, azim = 0)
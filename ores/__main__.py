from mpl_toolkits import mplot3d
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from .draw_sphere import draw_sphere

# (r, theta, phi) to (x, y, z), z is vertical
def spherical_to_cartesian(point):
	radius, theta, phi = point
	return (
		math.cos(theta) * math.sin(phi) * radius, # x
		math.sin(theta) * math.sin(phi) * radius, # y
		math.cos(phi) * radius, # z
	)

# (x, y, z) to (r, theta, phi)
def cartesian_to_spherical(point):
	x, y, z = point
	return (
		math.sqrt(x ** 2 + y ** 2 + z ** 2), # radius
		math.atan2(y, x), # theta
		math.atan2(math.sqrt(x ** 2 + y ** 2), z) # phi
	)

# pick a random point on a sphere uniformily
def pick_point():
	z = 2 * random.random() - 1
	theta = 2 * math.pi * random.random() - math.pi
	x = np.cos(theta) * math.sqrt(1 - z ** 2)
	y = np.sin(theta) * math.sqrt(1 - z ** 2)
	return ((x, y, z), cartesian_to_spherical((x, y, z)))

# covert to radians
def rad(degrees):
	return math.pi / 180 * degrees

def generate_ore_vein(spherical):
	points = [spherical] # list of ores in the cluster
	radius, theta, phi = spherical

	# start at the specified point
	total_theta = theta
	total_phi = phi

	eccentric_chance = random.random() ** 0.5 # higher percentages are rarer
	maximum = 35 # maximum amount of ores
	minimum = 10 # minimum amount of ores
	count = int((random.random() ** 2) * (maximum - minimum) + minimum) # amount of ores we have in this cluster
	for i in range(1, count):
		# vary the theta axis a little if we meet the threshold
		amount_theta = 1
		if random.random() > eccentric_chance:
			amount_theta = 5
		
		# vary the phi axis a little if we meet the threshold
		amount_phi = 1
		if random.random() > eccentric_chance:
			amount_phi = 5
		
		# walk the points around the central point we picked
		total_theta = total_theta + rad(random.random() * amount_theta * 2 - amount_theta)
		total_phi = total_phi + rad(random.random() * amount_phi * 2 - amount_phi)

		points.append((
			radius,
			total_theta,
			total_phi
		))
	return points

def plot_ore_vein():
	points = [spherical_to_cartesian(point) for point in generate_ore_vein(pick_point()[1])]
	x = [point[0] for point in points]
	y = [point[1] for point in points]
	z = [point[2] for point in points]
	ax.scatter3D(x, y, z)

# test ore count per vein distribution
def test():
	maximum = 35
	minimum = 10
	dictionary = {}
	total = 100000
	for i in range(0, total):
		count = int((random.random() ** 2) * (maximum - minimum) + minimum) # make higher counts rarer by power of 2
		if count not in dictionary:
			dictionary[count] = 0

		dictionary[count] = dictionary[count] + 1
	
	area_under_curve = 0
	area_under_curve_dictionary = {}
	for i in range(10, 35):
		percent = int(dictionary[i] / total * 100)
		area_under_curve = area_under_curve + dictionary[i] / total * 100

		key = int((i - 10) / 5)
		if key not in area_under_curve_dictionary:
			area_under_curve_dictionary[key] = 0

		area_under_curve_dictionary[key] = area_under_curve

		print(i, dictionary[i], f"{percent}%", "%.2f AUC" % area_under_curve)
	
	last = 0
	for key, value in area_under_curve_dictionary.items():
		print(((key + 2) * 5, (key + 3) * 5), "%.2f AUC" % (value - last))

		last = value

# test()

fig = plt.figure()
ax = plt.axes(projection='3d')

for i in range(10):
	plot_ore_vein()

draw_sphere(ax, 0.95)
plt.show()

# 10-15: 38.51%
# 16-20: 19.26%
# 21-30: 27.61%
# 30-35: 14.62%
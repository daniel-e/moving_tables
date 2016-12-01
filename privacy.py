from math import sqrt, atan2


def normalize(v):
	vl = sqrt(v[0] * v[0] + v[1] * v[1])
	return v[0] / vl, v[1] / vl if vl != 0 else 1


def degrees(a, b):
	v = normalize((b[0] - a[0], b[1] - a[1]))
	return 57.29577951308232 * atan2(v[0], v[1]) - atan2(0, 1)


def flip_y(v):
	return [v[0], -v[1]]


def transform_degree(pos, rot, target_pos):
	deg = degrees(flip_y(pos), flip_y(target_pos))
	deg += rot * 90
	if deg > 180:
		deg -= 360
	return deg


def calculate_privacy_panelty(pos, rot, target_pos):
	if list(pos) == target_pos:
		return 1000

	absdeg = abs(transform_degree(pos, rot, target_pos))
	if absdeg < 45:
		return 0  # perfect
	elif absdeg < 90:
		return 50  # ok
	elif absdeg < 135:
		return 100  # bad
	else:
		return 200  # worst


def test():
	degrees_y_flipped = lambda a, b: degrees(flip_y(a), flip_y(b))
	assert 0 == degrees_y_flipped([1, 10], [1, 1])  # sitting far below
	assert -90 == degrees_y_flipped([10, 1], [1, 1])  # sitting far right
	assert 90 == degrees_y_flipped([-10, 1], [1, 1])  # sitting far left (hypothetical)
	assert 180 == degrees_y_flipped([1, -10], [1, 1])  # sitting far up (hypothetical)

	assert 0 == transform_degree([1, 10], 0, [1, 1])
	assert 90 == transform_degree([1, 10], 1, [1, 1])
	assert 180 == transform_degree([1, 10], 2, [1, 1])
	assert -90 == transform_degree([1, 10], 3, [1, 1])

	assert -90 == transform_degree([10, 1], 0, [1, 1])
	assert 0 == transform_degree([10, 1], 1, [1, 1])
	assert 90 == transform_degree([10, 1], 2, [1, 1])
	assert 180 == transform_degree([10, 1], 3, [1, 1])

	assert 100 == calculate_privacy_panelty([10, -3], 0, [1, 1])  # sitting far right


test()

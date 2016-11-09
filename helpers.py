import random, sys

def cp_room(r):
	x = []
	for i in r:
		x.append(i[:])
	return x

def put_table(room, table, x, y, rot, mirror, to_bin = False):
	t = rotate_mirror_table(table, rot, mirror)
	for (ypos, l) in enumerate(t):
		for (xpos, c) in enumerate(l):
			if c != ' ':
				# check collisions with other tables
				if not to_bin:
					if ypos + y >= len(room) or xpos + x >= len(room[ypos + y]) or room[ypos + y][xpos + x] != 'X':
						return False
				if ypos + y < len(room) and xpos + x < len(room[ypos + y]) and ypos + y > 0 and xpos + x > 0:
					if to_bin:
						room[ypos + y][xpos + x] = "!"
					else:
						room[ypos + y][xpos + x] = c
	return True

def put_tables(room, table, table_pos):
    r = cp_room(room)
    for x, y in table_pos:
        if not put_table(r, table, x, y):
            return None
    return r

def get_target_pos(room):
	for (ypos, y) in enumerate(room):
		for (xpos, x) in enumerate(y):
			if x == 'T':
				return [xpos, ypos]
	return None

def dist(x, y, tx, ty):
	return (tx - x) * (tx - x) + (ty - y) * (ty - y)

def find_valid_random_table_layout(n_tables, room, table):
	while True:
		pos = []
		r = cp_room(room)
		for i in xrange(n_tables):
			x = random.randint(0, len(room[0]) - 1)
			y = random.randint(0, len(room) - 1)
			if not put_table(r, table, x, y):
				break
			pos.append((x, y))
		if len(pos) == n_tables:
			return pos

# ------------------------------------

class table_settings:
	def __init__(self, pos, rotation, mirror = False):
		self.pos = pos
		self.rotation = rotation
		self.mirror = mirror

def rotate_mirror_table(table, rot, mirror):
	if mirror:
		return _rotate_table(_mirror_table(table), rot)
	else:
		return _rotate_table(table, rot)

def _rotate_table(table, n):
	if n == 0:
		return table
	maxx = max(len(i) for i in table)
	maxy = len(table)
	r = []
	for i in xrange(maxx):
		r.append([' ' for i in xrange(maxy)])
	for (ypos, y) in enumerate(table):
		for (xpos, v) in enumerate(y):
			r[maxx - xpos - 1][ypos] = v
	return _rotate_table(r, n - 1)

def _mirror_table(table):
	r = []
	maxx = max(len(i) for i in table)
	for l in table:
		x = l[:]
		while len(x) < maxx:
			x.append(' ')
		r.append(list(reversed(x)))
	return r

def put_tables_with_collision(room, table, ts):
	r = cp_room(room)
	cnt = 0
	for t in ts:
		x = t.pos[0]
		y = t.pos[1]
		cnt += _put_table_in_room_with_collision(r, table, x, y, t.rotation, t.mirror, True)
	return r, cnt

rotated_tables = None

def _put_table_in_room_with_collision(room, table, x, y, r, mirror, border = False):
	collisions = 0

	global rotated_tables
	if rotated_tables == None:
		rotated_tables = []
		rotated_tables.append([_rotate_table(table, i) for i in xrange(4)])
		rotated_tables.append([_rotate_table(_mirror_table(table), i) for i in xrange(4)])
	t = rotated_tables[int(mirror)][r]

	for (ypos, l) in enumerate(t):
		for (xpos, c) in enumerate(l):
			if c != ' ':
				if not border:
					if ypos + y >= len(room) or xpos + x >= len(room[ypos + y]):
						return -1
					if room[ypos + y][xpos + x] != 'X':
						collisions += 1
				if border:
					if ypos + y >= len(room) or xpos + x >= len(room[ypos + y]):
						collisions += 1
					else:
						if room[ypos + y][xpos + x] != 'X':
							collisions += 1
						room[ypos + y][xpos + x] = c
	return collisions

def find_random_table_layout_with_collisions(n_tables, room, table):
	while True:
		pos = []
		r = cp_room(room)
		for i in xrange(n_tables):
			x = random.randint(0, len(room[0]) - 1)
			y = random.randint(0, len(room) - 1)
			rot = random.randint(0, 3)
			mir = bool(random.randint(0, 1))
			if _put_table_in_room_with_collision(r, table, x, y, rot, mir) == -1:
				break
			pos.append(table_settings((x, y), rot, mir))
		if len(pos) == n_tables:
			return pos

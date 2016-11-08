import random, sys

def cp_room(r):
	x = []
	for i in r:
		x.append(i[:])
	return x

def put_table(room, table, x, y, to_bin = False):
    for (ypos, l) in enumerate(table):
        for (xpos, c) in enumerate(l):
            if c != ' ':
                # check collisions with other tables
                if not to_bin:
                    if ypos + y >= len(room) or xpos + x >= len(room[ypos + y]) or room[ypos + y][xpos + x] != 'X':
                        return False
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

rotated_tables = None

def rotate_table(table, n):
	if n == 0:
		return table
	maxx = max(len(i) for i in table)
	maxy = len(table)
	r = []
	for i in xrange(maxx):
		r.append([' ' for i in xrange(maxy)])
	for (ypos, y) in enumerate(table):
		for (xpos, v) in enumerate(y):
			r[xpos][ypos] = v
	return rotate_table(r, n - 1)

def put_tables_with_collision(room, table, table_pos):
	r = cp_room(room)
	cnt = 0
	for x, y, rot in table_pos:
		cnt += put_table_in_room_with_collision(r, table, x, y, rot, True)
	return r, cnt

def put_table_in_room_with_collision(room, table, x, y, r, border = False):
	collisions = 0

	global rotated_tables
	if rotated_tables == None:
		rotated_tables = [rotate_table(table, i) for i in xrange(4)]
	t = rotated_tables[r]

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
			if put_table_in_room_with_collision(r, table, x, y, rot) == -1:
				break
			pos.append((x, y, rot))
		if len(pos) == n_tables:
			return pos

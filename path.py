import sys

def allowed(r, x, y):
	return (
		x >= 0 and y >= 0 and x < len(r[0]) and y < len(r) and
		# X = free in room
		# o = person at table
		# - = free place in room not allowed for table
		# T = escape target
		# c = center of person at table
		(r[y][x] == 'X' or r[y][x] == 'o' or r[y][x] == '-' or r[y][x] == 'T' or r[y][x] == 'c')
	)

def big_enough(r, x, y):
	x -= escape_center[0]
	y -= escape_center[1]
	for (ypos, l) in enumerate(escape):
		for (xpos, c) in enumerate(l):
			if c != '-':
				if not allowed(r, x + xpos, y + ypos):
					return False
	return True

def do_compute_path(r, cx, cy, tx, ty, n, stack, visited):
	if n > 700:
		print >> sys.stderr, "stack limit"
		#stack.append((tx, ty))
		return
	stack.append((cx, cy))
	candidates = []
	for y in [-1, 0, 1]:
		for x in [-1, 0, 1]:
			if x != 0 or y != 0:
				if big_enough(r, cx + x, cy + y):
					candidates.append((dist(cx + x, cy + y, tx, ty), cx + x, cy + y))

	for d, x, y in sorted(candidates):
		if (x, y) not in visited:
			if r[y][x] == 'T':
				stack.append((tx, ty))
				return
			visited.add((x, y))
			do_compute_path(r, x, y, tx, ty, n + 1, stack, visited)
			if stack[-1] == (tx, ty):
				return
	stack.pop()

def compute_path(r, x, y):
	global table_start_offset # XXX global !!!
	global target_pos

	xpos = x + table_start_offset[0]
	ypos = y + table_start_offset[1]
	tx = target_pos[0]
	ty = target_pos[1]
	stck = []
	visited = set([])
	do_compute_path(r, xpos, ypos, tx, ty, 0, stck, visited)
	return stck

def compute_paths(room, table, table_pos):
	paths = []
	for i in xrange(len(table_pos)):
		r = cp_room(room)
		for j in xrange(len(table_pos)):
			if j != i:
				# r is changed
				put_table(r, table, table_pos[j][0], table_pos[j][1], True)
		s = compute_path(r, table_pos[i][0], table_pos[i][1])
		paths.append(s)

	# draw paths
	r = cp_room(room)
	for stack in paths:
		if len(stack) > 0:
			stack.pop()  # remove target from stack
			for x, y in stack:
				r[y][x] = 'O'
	return r

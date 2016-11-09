import sys
from io import get_table_start_offset
from helpers import rotate_mirror_table, cp_room, put_table, dist

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

def big_enough(r, x, y, escape_center, escape):
	x -= escape_center[0]
	y -= escape_center[1]
	for (ypos, l) in enumerate(escape):
		for (xpos, c) in enumerate(l):
			if c != '-':
				if not allowed(r, x + xpos, y + ypos):
					return False
	return True

def do_compute_path(r, cx, cy, tx, ty, n, stack, visited, escape_center, escape):
	if n > 700:
	#	print >> sys.stderr, "stack limit"
	#	#stack.append((tx, ty))
		return False
	stack.append((cx, cy))
	candidates = []
	for y in [-1, 0, 1]:
		for x in [-1, 0, 1]:
			if x != 0 or y != 0:
				if big_enough(r, cx + x, cy + y, escape_center, escape):
					candidates.append((dist(cx + x, cy + y, tx, ty), cx + x, cy + y))

	for d, x, y in sorted(candidates):
		if (x, y) not in visited:
			if r[y][x] == 'T':
				stack.append((tx, ty))
				return True
			visited.add((x, y))
			do_compute_path(r, x, y, tx, ty, n + 1, stack, visited, escape_center, escape)
			if stack[-1] == (tx, ty):
				return True
	stack.pop()
	return False

def compute_path(r, table, x, y, rot, mirror, target_pos, escape_center, escape):

	table_start_offset = get_table_start_offset(rotate_mirror_table(table, rot, mirror))

	xpos = x + table_start_offset[0]
	ypos = y + table_start_offset[1]
	tx = target_pos[0]
	ty = target_pos[1]
	stck = []
	visited = set([])
	r = do_compute_path(r, xpos, ypos, tx, ty, 0, stck, visited, escape_center, escape)
	return stck, r

def compute_paths(room, table, table_settings_list, target_pos, escape_center, escape):
	""" Computes paths from each table.
	Returns:
		(list, int): room, number of existing paths
	"""
	paths = []
	cnt = 0
	for i, tp_i in enumerate(table_settings_list):
		r = cp_room(room)
		for j, tp_j in enumerate(table_settings_list):
			if j != i:
				# r is changed
				put_table(r, table, tp_j.pos[0], tp_j.pos[1], tp_j.rotation, tp_j.mirror, True)
		s, res = compute_path(r, table, tp_i.pos[0], tp_i.pos[1], tp_i.rotation, tp_i.mirror, target_pos, escape_center, escape)
		if res:
			cnt += 1
		paths.append(s)

	# draw paths
	r = cp_room(room)
	for stack in paths:
		if len(stack) > 0:
			stack.pop()  # remove target from stack
			for x, y in stack:
				r[y][x] = 'O'
	return (r, cnt)

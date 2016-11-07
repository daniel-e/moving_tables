#!/usr/bin/env python

# XXX rotate tables
# XXX check that radius is 100cm

import sys, random
from io import load_room, load_table
from helpers import put_table, put_tables, cp_room, get_target_pos, dist
from helpers import find_valid_random_table_layout

n_tables = 0
table_pos = [(10, 20), (30, 25)]

#n_tables = 6
#table_pos = []
room = []
table = []
table_start_offset = []   # start position of employee relative to left upper corner of table
target_pos = []           # target position of each employee

# -------------------------

def allowed(r, x, y):
	return (
		x >= 0 and y >= 0 and x < len(r[0]) and y < len(r) and
		(r[y][x] == 'X' or r[y][x] == 'o' or r[y][x] == '-' or r[y][x] == 'T')
	)

def do_compute_path(r, cx, cy, tx, ty, n, stack):
	#if n > 200:
	#	return
	stack.append((cx, cy))
	candidates = []
	for y in [-1, 0, 1]:
		for x in [-1, 0, 1]:
			if x != 0 or y != 0:
				if allowed(r, cx + x, cy + y):
					candidates.append((dist(cx + x, cy + y, tx, ty), cx + x, cy + y))

	for d, x, y in sorted(candidates):
		if r[y][x] == 'T':
			stack.append((tx, ty))
			return
		r[y][x] = 'O'
		do_compute_path(r, x, y, tx, ty, n + 1, stack)
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
	do_compute_path(r, xpos, ypos, tx, ty, 0, stck)
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

# -------------------------

room                      = load_room(open("raum.txt"))     # load room layout from file
target_pos                = get_target_pos(room)
table, table_start_offset = load_table()                    # load table layout from file

# initial population
if n_tables > 0:
	table_pos             = find_valid_random_table_layout(n_tables, room, table)

# put one population into the room
r = put_tables(room, table, table_pos)                   # place tables in room
if not r:
	# this should not happen
	print >> sys.stderr, "invalid table configuration"
	sys.exit(1)

r = compute_paths(r, table, table_pos)


# output room and table setting with escape paths
for line in r:
	print "".join(line)

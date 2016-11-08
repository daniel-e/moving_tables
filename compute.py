#!/usr/bin/env python

# This script computes a possible configuration for eight tables using
# genetic algorithms so that they do not overlap.
# Fitness function is based only on overlapping.

# XXX rotate tables
# XXX fitness function: include escape paths
# XXX fitness function: increase average distance of tables
# XXX fitness function: direction to door / other collegues


import sys, random
from io import load_room, load_table, load_escape
from helpers import put_table, put_tables, cp_room, get_target_pos, dist
from helpers import find_valid_random_table_layout, find_random_table_layout
from helpers import put_tables_with_collision

n_tables = 0
table_pos = [(10, 20), (30, 25)]

n_tables = 8
table_pos = []
room = []
table = []
table_start_offset = []   # start position of employee relative to left upper corner of table
target_pos = []           # target position of each employee
escape = []
escape_center = []

# -------------------------

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

# -------------------------

escape, escape_center     = load_escape()
room                      = load_room(open("raum.txt"))     # load room layout from file
target_pos                = get_target_pos(room)
table, table_start_offset = load_table()                    # load table layout from file

r = None

class individuum:
	def __init__(self, table_pos):
		self.fitness_value = 0.0
		self.room_config = None
		self.table_pos = table_pos

if False:
	# initial population
	if n_tables > 0:
		table_pos = find_valid_random_table_layout(n_tables, room, table)
		# put one population into the room
		r = put_tables(room, table, table_pos)              # place tables in room
	if not r:
		# this should not happen
		print >> sys.stderr, "invalid table configuration"
		sys.exit(1)
	r = compute_paths(r, table, table_pos)


def tobin(i):
	b = []
	# 7 bit for x
	# 6 bit for y
	for x, y in i.table_pos:
		for i in [64, 32, 16, 8, 4, 2, 1]:
			if x & i:
				b.append(1)
			else:
				b.append(0)
		for i in [32, 16, 8, 4, 2, 1]:
			if y & i:
				b.append(1)
			else:
				b.append(0)
	return b

def split_bin(b):
	for i in xrange(0, len(b), 7 + 6):
		yield b[i:i+13]

def fb(v):
	r = 0
	f = 1
	for i in reversed(v):
		r += f * i
		f *= 2
	return r

def frombin(b):
	r = []
	for i in split_bin(b):
		x = fb(i[:7])
		y = fb(i[7:])
		r.append((x, y))
	return individuum(r)


def mutation(i):
	b = tobin(i)
	n = len(b)
	for i in xrange(n):
		if random.randint(0, n - 1) == 0:  # with prob = 1/n
			b[i] = 1 - b[i]                # flip bit
	return frombin(b)

def crossover(i, j):
	ibin = tobin(i)
	jbin = tobin(j)
	p = random.randint(1, len(ibin) - 1)
	a1 = ibin[:p]
	a2 = jbin[p:]
	b2 = ibin[p:]
	b1 = jbin[:p]
	a = frombin(a1 + a2)
	b = frombin(b1 + b2)
	return (a, b)


if True:
	population = []
	n = 100
	n_elitism = 1         # only 1 is allowed
	n_selection = 29
	n_crossover = 60 / 2
	n_mutation = 10

	assert(n_elitism + n_selection + n_crossover * 2 + n_mutation == n)

	# create initial population
	for i in xrange(n):
		# can also return overlapping tables
		table_pos = find_random_table_layout(n_tables, room, table)
		population.append(individuum(table_pos))

	while True:
		assert(len(population) == n)

		# compute fitness function for population
		fsum = 0
		fsumr = 0.0
		best = 0
		for (idx, i) in enumerate(population):
			# cnt = number of collisions
			#print >> sys.stderr, i.table_pos
			r, cnt = put_tables_with_collision(room, table, i.table_pos)
			i.room_config = r
			i.fitness_value = cnt
			fsum += cnt
			fsumr += 1.0 / (cnt + 1)
			if cnt < population[best].fitness_value:
				best = idx
		print >> sys.stderr, "average fitness:", float(fsum) / n, "best:", population[best].fitness_value

		if population[best].fitness_value == 0:
			tp = population[best].table_pos
			r, cnt = put_tables_with_collision(room, table, tp)
			break

		new_pop = []
		# elitism: keep the best indiviuum
		new_pop.append(population[best])

		# selection
		for i in xrange(n_selection):
			rnd = random.random()
			s = 0.0
			for j in population:
				s += 1.0 / (j.fitness_value + 1) / fsumr
				if s >= rnd:
					new_pop.append(j)
					break

		# crossover
		for i in xrange(n_crossover):
			rnda = random.randint(0, n - 1)
			rndb = random.randint(0, n - 1)
			a, b = crossover(population[rnda], population[rndb])
			new_pop.append(a)
			new_pop.append(b)

		# mutation
		for i in xrange(n_mutation):
			j = random.randint(0, n - 1)
			new_pop.append(mutation(population[j]))

		population = new_pop


# output room and table setting with escape paths
for line in r:
	print "".join(line)

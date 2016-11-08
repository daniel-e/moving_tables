#!/usr/bin/env python

# This script computes a possible configuration for eight tables using
# genetic algorithms so that they do not overlap.
# Fitness function is based only on overlapping.

# XXX fitness function: include escape paths
# XXX fitness function: increase average distance of tables
# XXX fitness function: direction to door / other collegues


import sys, random
from io import load_room, load_table, load_escape
from helpers import put_table, put_tables, cp_room, get_target_pos, dist
from helpers import find_valid_random_table_layout, find_random_table_layout_with_collisions
from helpers import put_tables_with_collision, table_settings
from path import compute_paths
import genetic

n_tables = 8
table_pos = []
room = []
table = []
table_start_offset = []   # start position of employee relative to left upper corner of table
target_pos = []           # target position of each employee
escape = []
escape_center = []

# -------------------------

escape, escape_center     = load_escape()
room                      = load_room(open("raum.txt"))     # load room layout from file
target_pos                = get_target_pos(room)
table, table_start_offset = load_table()                    # load table layout from file

r = None

class individuum:
	def __init__(self, ts):
		self.fitness_value = 0.0
		self.room_config = None
		self.table_settings = ts

def tobin(i):
	b = []
	# 7 bit for x
	# 6 bit for y
	for t in i.table_settings:
		x = t.pos[0]
		y = t.pos[1]
		r = t.rotation

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
		for i in [2, 1]:
			if r & i:
				b.append(1)
			else:
				b.append(0)
		if t.mirror:
			b.append(1)
		else:
			b.append(0)
	return b

def split_bin(b):
	for i in xrange(0, len(b), 7 + 6 + 2 + 1):
		yield b[i:i+16]

def bin2dec(v):
	r = 0
	f = 1
	for i in reversed(v):
		r += f * i
		f *= 2
	return r

def frombin(b):
	r = []
	for i in split_bin(b):
		x = bin2dec(i[:7])
		y = bin2dec(i[7:13])
		rot = bin2dec(i[13:15])
		mir = bool(bin2dec(i[15:16]))
		r.append(table_settings((x, y), rot, mir))
	return individuum(r)

def mutation(i):
	return frombin(genetic.mutation(tobin(i)))

def crossover(i, j):
	return [frombin(i) for i in genetic.crossover(tobin(i), tobin(j))]


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
		table_set = find_random_table_layout_with_collisions(n_tables, room, table)
		population.append(individuum(table_set))

	last_best = -1

	while True:
		assert(len(population) == n)

		# compute fitness function for population
		fsum = 0.0
		fsumr = 0.0
		best = 0
		for (idx, i) in enumerate(population):
			# cnt = number of collisions
			r, cnt = put_tables_with_collision(room, table, i.table_settings)

			fitness = float(cnt)

			i.room_config = r
			i.fitness_value = fitness
			fsum += fitness
			fsumr += 1.0 / (fitness + 1.0)
			if fitness < population[best].fitness_value:
				best = idx

		print >> sys.stderr, "average fitness:", float(fsum) / n, "best:", population[best].fitness_value

		if last_best != best:
			last_best = best
			print >> sys.stderr, "updated tmp.txt"
			f = open("tmp.txt", "w")
			for line in r:
				print >> f, "".join(line)
			f.close()

		if population[best].fitness_value == 0:
			tp = population[best].table_settings
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

import random

# b = list of intergers in {0,1}
def mutation(b):
	n = len(b)
	for i in xrange(n):
		if random.randint(0, n - 1) == 0:  # with prob = 1/n
			b[i] = 1 - b[i]                # flip bit
	return b

def crossover(ibin, jbin):
	p = random.randint(1, len(ibin) - 1)
	a1 = ibin[:p]
	a2 = jbin[p:]
	b2 = ibin[p:]
	b1 = jbin[:p]
	return (a1 + a2, b1 + b2)

#!/usr/bin/env python

from multiprocessing import Pool

"""
    Splits the list _l_ in smaller lists each of size _chunk_size_. The smaller
    lists are processed in parallel by _cpus_ threads by function _fn_.
"""
def process_list(l, chunk_size, cpus, fn):
    jobs = []
    for i in xrange(0, len(l), chunk_size):
        c = l[i:i+chunk_size]
        jobs.append(c)
    pool = Pool(cpus)
    # workaround for python bug
    # http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
    r = pool.map_async(fn, jobs).get(9999999)
    pool.close()
    return r

# ------------------------------------------------------------------------------

def times2(list_of_numbers):
    return [i * 2 for i in list_of_numbers]

if __name__ == "__main__":
    print list(process_list(range(100), 12, 4, times2))

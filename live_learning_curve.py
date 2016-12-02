#!/usr/bin/env python

import time
import matplotlib.pyplot as plt

# http://matplotlib.org/users/pyplot_tutorial.html

plt.ion()

def update_plot():
    f = open("learning_curve.txt")
    data = [i.strip() for i in f]
    vals_avg = [float(i.split()[0]) for i in data]
    vals_best = [float(i.split()[1]) for i in data]
    f.close()
    #print vals_avg
    plt.plot(vals_avg, 'r-s')
    plt.plot(vals_best, 'b-d')
    plt.grid(True)

while True:
    update_plot()
    plt.pause(1)

#!/usr/bin/env python

import time
import matplotlib.pyplot as plt

# http://matplotlib.org/users/pyplot_tutorial.html

plt.ion()

def update_plot():
    f = open("learning_curve.txt")
    vals = [float(i) for i in f]
    f.close()
    plt.plot(vals, 'r-s')
    plt.grid(True)

while True:
    update_plot()
    plt.pause(1)

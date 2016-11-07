#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, sys

from io import load_room

room = load_room(sys.stdin)

def draw_rect(cr, x, y, r, g, b):
	cr.set_source_rgb(0.6, 0.2, 0.2)
	cr.rectangle(x * 10, y * 10, 10, 10)
	cr.fill()
	cr.set_source_rgb(r, g, b)
	cr.rectangle(x * 10 + 1, y * 10 + 1, 8, 8)
	cr.fill()

def expose(widget, event):
	cr = widget.window.cairo_create()
	cr.set_line_width(1)
	for (ypos, y) in enumerate(room):
		for (xpos, x) in enumerate(y):
			# table
			if x == '!':
				draw_rect(cr, xpos, ypos, 0.2, 0.6, 0.2)
			elif x == 'o':
				draw_rect(cr, xpos, ypos, 0.2, 0.2, 0.6)
			elif x == 'c':
				draw_rect(cr, xpos, ypos, 0.9, 0.9, 0.2)
			# path
			elif x == 'O':
				draw_rect(cr, xpos, ypos, 0.7, 0.7, 0.7)
			# room
			elif x == '-':
				draw_rect(cr, xpos, ypos, 0.4, 0.4, 0.4)
			elif x == 'T':
				draw_rect(cr, xpos, ypos, 0.9, 0.2, 0.2)
			else:
				draw_rect(cr, xpos, ypos, 0.1, 0.1, 0.1)

def destroy(w, data = None):
	gtk.main_quit()

w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.resize(len(room[0]) * 10, len(room) * 10)
w.connect("destroy", destroy)
c = gtk.DrawingArea()
c.connect("expose-event", expose)
w.add(c)
w.show_all()
gtk.main()

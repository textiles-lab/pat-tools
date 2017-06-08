#!/usr/bin/env python3

#read a file in innova '.pat' format (really, gcode)
#write an svg

import argparse, sys, re

parser = argparse.ArgumentParser(description="Convert Innova Autopilot pattern files (.pat) to SVG files.")
parser.add_argument('patfile', help="input pattern file", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('svgfile', help="output svg file", nargs='?', type=argparse.FileType('w'), default=sys.stdout)

args = parser.parse_args()

path = []

min_x = float('inf')
min_y = float('inf')
max_x = float('-inf')
max_y = float('-inf')

for line in args.patfile:
	m = re.match(r"^N\d+G(\d+)X([\d.]+)Y([\d.]+)$", line)
	if m == None:
		print("Unrecognized line: '" + line + "'", file=sys.stderr)
		continue
	cmd = int(m.group(1))
	x = float(m.group(2))
	y = -float(m.group(3))
	min_x = min(min_x, x)
	min_y = min(min_y, y)
	max_x = max(max_x, x)
	max_y = max(max_y, y)
	if cmd == 0:
		path.append("M " + str(x) + " " + str(y))
	elif cmd == 1:
		path.append("L " + str(x) + " " + str(y))
	else:
		print("Unknown G command " + str(cmd) + ".", file=sys.stderr)

min_x -= 0.25
min_y -= 0.25

max_x += 0.25
max_y += 0.25

width_in = max_x - min_x
height_in = max_y - min_y

f = args.svgfile

print('<?xml version="1.0" standalone="no"?>', file=f)
print('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">', file=f)
print('<svg width="' + str(width_in) + 'in" height="' + str(height_in) + 'in" viewBox="' + str(min_x) + ' ' + str(min_y) + ' ' + str(width_in) + ' ' + str(height_in) + '" version="1.1" xmlns="http://www.w3.org/2000/svg">', file=f)
print('<path d="' + " ".join(path) + '" style="stroke:#000;stroke-width:0.01;fill:none" />', file=f)
print('</svg>', file=f)

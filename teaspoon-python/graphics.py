#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from base import *
import sys, pygame

VERSION.append("graphics")

width = 0
height = 0

def initWindow(w=None, h=None, title=None):

	global screen
	global width, height

	if w==None:
		w = 640

	if h==None:
		h = 360

	if title==None:
		title = 'Teaspoon Game (powered by PyGame)'
	else:
		title = pystring(title)

	pygame.init()

	size = width, height = w, h

	scopeValues[0] = width
	scopeValues[1] = height

	screen = pygame.display.set_mode(size)

	pygame.display.set_caption(title)

def clear(r=None, g=None, b=None):
	if r==None:
		r = 0
	if g==None:
		g = 0
	if b==None:
		b = 0
	screen.fill((r,g,b))

def circle(x, y, radius, r=None, g=None, b=None, width=None):
	if r==None:
		r = 255
	if g==None:
		g = 255
	if b==None:
		b = 255
	if width==None:
		width = 0
	pygame.draw.circle(screen, (r, g, b),  (x, y), radius)

# screen.blit(ball, pygame.Rect(x,y,100,100))

def line(x0, y0, x1, y1, r=None, g=None, b=None, width=None):
	if r==None:
		r = 255
	if g==None:
		g = 255
	if b==None:
		b = 255
	if width==None:
		width = 1
	pygame.draw.line(screen, (r, g, b), (x0, y0), (x1, y1), width)

def polygon(points, r=None, g=None, b=None, width=None):
	if r==None:
		r = 255
	if g==None:
		g = 255
	if b==None:
		b = 255
	if width==None:
		width = 0
	pygame.draw.polygon(screen, (r, g, b), list(zip(points[::2],points[1::2])), width)

def rect(x,y,w,h,r=None,g=None,b=None,width=None):
	if r==None:
		r = 255
	if g==None:
		g = 255
	if b==None:
		b = 255
	if width==None: #line width
		width = 0
	pygame.draw.rect(screen, (r,g,b), pygame.Rect(x,y,w,h), width)

def getEvent():
	event = pygame.event.poll()

	return [event.type,
	event.key if 'key' in event.__dict__.keys() else None,
	event.button if 'button' in event.__dict__.keys() else None,
	event.pos if 'pos' in event.__dict__.keys() else None]

EXTENSIONS.update({
	'initWindow': initWindow,

	'clear': clear,
	'circle': circle,
	'line': line,
	'rect': rect,
	'polygon': polygon,

	'getEvent': getEvent,
	'quit': quit
})

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	scopeNames = ['width', 'height']
	scopeValues = [0, 0]
	call(src, "init", [], scopeNames, scopeValues)

	while True:
		call(src, "update", [], scopeNames, scopeValues)
		pygame.display.flip()

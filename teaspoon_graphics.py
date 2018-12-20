#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from teaspoon_base import *
import sys, pygame

VERSION[0] = "graphics"

def initWindow(w=320, h=240, title='Teaspoon Game (powered by PyGame)'):

	global screen

	pygame.init()

	size = width, height = w, h

	screen = pygame.display.set_mode(size)

	pygame.display.set_caption(title)

def drawCircle(x, y, r):

	global screen
	black = 0, 0, 0

	screen.fill(black)

	pygame.draw.circle(screen, (255,0,0), (x,y), r)
	# screen.blit(ball, pygame.Rect(x,y,100,100))

	pygame.display.flip()


def getEvent():
	event = pygame.event.poll()
	return event.type

EXTENSIONS.update({
	'initWindow': initWindow,
	'drawBall': drawBall,
	'drawCircle': drawCircle,
	'getEvent': getEvent
})

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	exec(src, "main", [])
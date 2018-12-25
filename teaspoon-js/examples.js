var wontwork = `main :
require "superHorse"

% that's the point. its not supposed to work`

var count = `cat x y :
	i = 0
	while :
	c = get y i
	add x c
	i = sum i 1
	ly = len y
	ifLess i ly while
	ret x

hello a :
	msg = "hello"
	% this is a comment
	cat msg " "
	cat msg a
	print msg
	ret

main :
	c = 0
	while :
		p = sum c 48
		hello [p]
		c = sum c 1
		ifEq c 10 skip
	ifEq 0 0 while

	skip :
	ifEq c 10
	print "That was cool!"
	end :
	ret`

var scopeInject = `
% When run with teaspoon_graphics scope injection is done automatically between init and update

init :
	x = 49
ret

update :
	print [x]
ret

% When run with teaspoon_base scope injection is done manually. This is a seperate feature.

"incidentally these kinds of comments work too"

main :
	y = 68
	cool $
ret

cool :
	print [y]
ret`

var poly = `
init :
initWindow
ret

update :
events $
polygon [10,10,20,10,20,30,10,20] . . . 0
ret

events :

ev = getEvent
evCode = get ev 0
evKey = get ev 1
evPos = get ev 3

% quit event
ifEq evCode 12
quit
end :

ret`

var circle2 = `init :

	print "First, we initialize game logic."

	require "base"
	require "graphics"
	initWindow

	speedX = 2
	speedY = 2
	posX = 225
	posY = 150

	rwall = width
	bwall = height
	rwall = sum rwall -50
	bwall = sum bwall -50

	clk = 255

	mx = 0
	my = 0
ret

physics :

	% print "Next, we make calculations related to physics."

	posX = sum posX speedX
	posY = sum posY speedY

	ifLess posX rwall skip
		ifEq posX rwall skip
			speedX = -speedX
	skip :

	ifLess posX 50
		speedX = -speedX
	end :

	ifLess posY bwall skip
		ifEq posY bwall skip
			speedY = -speedY
	skip :

	ifLess posY 50
		speedY = -speedY
	end :

ret

events :

	% print "Also, it's a good idea to handle events."

	ev = getEvent
	evCode = get ev 0
	evKey = get ev 1
	evPos = get ev 3

	% key down
	ifEq evCode 2
		% keycode is key_k
		ifEq evKey 107
			clk = 0
	end :

	% key up
	ifEq evCode 3
		% keycode is key_k
		ifEq evKey 107
			clk = 255
	end :

	% mouse move
	ifEq evCode 4

		evPosX = get evPos 0
		evPosY = get evPos 1

		mx = evPosX
		my = evPosY
	end :

	% quit event
	ifEq evCode 12
		quit
	end :
ret

render :

	% print "Rendering is the most important part."

	clear
	circle posX posY 50 255 clk clk
	line 0 0 posX posY 255 255 255 3

	px = sum mx -10
	py = sum my -10

	%    x  y  w  h  r   g   b
	rect px py 20 20 217 105 105

ret

update :

	physics $
	render $
	events $

ret`

var toString = `% added support for statements like
% print 5
% rendering this unnecessary. Let it be a theoretical example.

div x n :

k = 0

while :
k = sum k 1
m = mul k n
ifLess m x while

ifLess x m
k = sum k -1
end :

ret k

mod x n :

while :

ifLess 0 x skip
ifEq 0 x skip
x = sum x n
skip :

ifLess x n skip
x = sum x -n
skip :

ifLess x 0 while
ifLess n x while
ifEq n x while

ret x

reverse arr :

ln = len arr
k = []

li = ln

while :
li = sum li -1
le = get arr li
add k le
ifLess 0 li while

ret k


toString x :
r = []

while :

m = mod x 10
m = sum m 48
add r m

x = div x 10

ifEq x 0 skip
ifEq 0 0 while
skip :

s = reverse r
ret s

main :
h = toString 506
print h
ret`

var weird = `
% You can get creative with this syntax

main :

x = 5
y = 3

funk x y :

ifLess y 1 skip

p = sum x 48
print [p]
p = sum y 48
print [p]

x = sum x -1
y = sum y -1

funk x y

skip :

ret`


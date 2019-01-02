
VERSION += ['graphics']


var canvas;
var ctx;

var width, height;

function initWindow(w, h, title) {
	if (w == undefined) {
		//fullscreen
		w = 640;
		h = 360;
	}

	if (title == undefined) {
		title = 'Teaspoon Game [HTML5]';
	}

	canvas = document.createElement('canvas');
	ctx = canvas.getContext('2d');
	canvas.style.width = w + 'px';
	canvas.style.height = h + 'px';

	canvas.width = w;
	canvas.height = h;
	width = w;
	height = h;

	document.title = title

	scopeValues[0] = width
	scopeValues[1] = height

	if (document.body == undefined) {
		var body = document.createElement('body')
		document.body = body;
	}

	document.body.appendChild(canvas)
}

function clear(r, g, b) {
	if (r == undefined)
		r = 0;
	if (g == undefined)
		g = 0;
	if (b == undefined)
		b = 0;
	ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
	ctx.fillRect(0, 0, width, height);
}

function circle(x, y, radius, r, g, b, width) {
	if (r == undefined)
		r = 255;
	if (g == undefined)
		g = 255;
	if (b == undefined)
		b = 255;
	if (width == undefined)
		width = 0;

	ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
	ctx.strokeStyle = `rgb(${r}, ${g}, ${b})`;

	ctx.beginPath();
	ctx.arc(x, y, radius, 0, 2 * Math.PI);
	if (width == 0) {
		ctx.fill();
	}
	else {
		ctx.lineWidth = width;
		ctx.stroke();
	}
}

function line(x0, y0, x1, y1, r, g, b, width) {
	if (r == undefined)
		r = 255;
	if (g == undefined)
		g = 255;
	if (b == undefined)
		b = 255;
	if (width == undefined)
		width = 1;

	ctx.strokeStyle = `rgb(${r}, ${g}, ${b})`;
	ctx.lineWidth = width;
	ctx.beginPath();
	ctx.moveTo(x0, y0);
	ctx.lineTo(x1, y1);
	ctx.stroke();
}

function polygon(points, r, g, b, width) {
	if (r == undefined)
		r = 255;
	if (g == undefined)
		g = 255;
	if (b == undefined)
		b = 255;
	if (width == undefined)
		width = 0;

	ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
	ctx.strokeStyle = `rgb(${r}, ${g}, ${b})`;

	ctx.beginPath();

	ctx.moveTo(points[0], points[1])

	for (var i = 2; i < points.length; i += 2) {
		ctx.lineTo(points[i], points[i + 1])
	}

	ctx.lineTo(points[0], points[1])


	if (width == 0) {
		ctx.fill();
	}
	else {
		ctx.lineWidth = width;
		ctx.stroke();
	}
}

function rect(x, y, w, h, r, g, b, width) {
	if (r == undefined)
		r = 255;
	if (g == undefined)
		g = 255;
	if (b == undefined)
		b = 255;
	if (width == undefined) //line width
		width = 0;

	ctx.strokeStyle = `rgb(${r}, ${g}, ${b})`;
	ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
	if (width == 0) {
		ctx.fillRect(x, y, w, h)
	}
	else {
		ctx.lineWidth = width;
		ctx.strokeRect(x, y, w, h)
	}
}

eventInfo = [];

addEventListener('keydown', function (ev) {
	eventInfo = [];
	eventInfo[0] = 2;
	eventInfo[1] = ev.keyCode;
})

function getEvent() {
	return eventInfo;
}

function quit() {
	// not needed
}

NEW_EXTENSIONS = {
	'initWindow': initWindow,

	'clear': clear,
	'circle': circle,
	'line': line,
	'rect': rect,
	'polygon': polygon,

	'getEvent': getEvent,
	'quit': quit
}

for (var ext in NEW_EXTENSIONS) {
	EXTENSIONS[ext] = NEW_EXTENSIONS[ext];
}

var scopeNames = ['width', 'height'];
var scopeValues = [0, 0];

var src = circle2;

call(src, 'init', [], scopeNames, scopeValues);

setInterval(function () {
	call(src, 'update', [], scopeNames, scopeValues)
}, 1000 / 60);
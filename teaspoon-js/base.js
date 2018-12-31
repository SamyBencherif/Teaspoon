
var VERBOSE = 0
var VERSION = ["base"]
var EXTENSIONS = {}

function verbose(info) {
	// condition improves performance
	if (VERBOSE)
		console.debug(info)
}

function argParse(line) {
	if (line.trim() == "")
		return [];

	var k = [];
	var inQuotes = 0;
	var acc = "";

	for (var i of line.trim()) {
		if (i == '"') {
			inQuotes = !inQuotes
		}
		if (!inQuotes && i == ' ') {
			k.push(acc)
			acc = "";
		} else {
			acc += i
		}
	}

	k.push(acc)

	return k
}

function replaceAll(str, a, b) {
	var capture = "";
	var res = "";

	for (var i in str) {
		if (capture == a) {
			res += b
			capture = "";
		}

		if (str[i] != a[capture.length]) {
			res += capture;
			res += str[i];
			capture = "";
		} else {
			capture += str[i];
		}
	}

	return res
}

function jsString(k) {
	return k.map(x => String.fromCharCode(x)).join('')
}

function func_print(args, src, scopeNames, scopeValues) {
	verbose(`print ${resolve(args[0], src, scopeNames, scopeValues)} `)
	if (typeof resolve(args[0], src, scopeNames, scopeValues) == 'number')
		console.log(resolve(args[0], src, scopeNames, scopeValues))
	else
		console.log(jsString(resolve(args[0], src, scopeNames, scopeValues))) // process string literal or vars
	return;
}

function func_require(args, src, scopeNames, scopeValues) {
	if (VERSION.indexOf(jsString(resolve(args[0], src, scopeNames, scopeValues))) == -1)
		console.error(`This program is not compatible with this version of Teaspoon.It requires teaspoon_${jsString(resolve(args[0], src, scopeNames, scopeValues))}.`)

}

function func_get(args, src, scopeNames, scopeValues) {
	return resolve(args[0], src, scopeNames, scopeValues)[resolve(args[1], src, scopeNames, scopeValues)]
}

function func_add(args, src, scopeNames, scopeValues) {
	return resolve(args[0], src, scopeNames, scopeValues).push(resolve(args[1], src, scopeNames, scopeValues))
}

function func_sum(args, src, scopeNames, scopeValues) {
	return resolve(args[0], src, scopeNames, scopeValues) + resolve(args[1], src, scopeNames, scopeValues)
}

function func_mul(args, src, scopeNames, scopeValues) {
	return resolve(args[0], src, scopeNames, scopeValues) * resolve(args[1], src, scopeNames, scopeValues)
}

function func_div(args, src, scopeNames, scopeValues) {
	return Math.floor(resolve(args[0], src, scopeNames, scopeValues) / resolve(args[1], src, scopeNames, scopeValues));
}

function func_len(args, src, scopeNames, scopeValues) {
	return resolve(args[0], src, scopeNames, scopeValues).length
}

BUILTINS = {
	"print": func_print,
	"require": func_require,
	"get": func_get,
	"add": func_add,
	"sum": func_sum,
	"mul": func_mul,
	"div": func_div,
	"len": func_len
}

function pretty(scopeVals) {
	if (typeof scopeVals != 'object')
		return `${scopeVals}`;

	var res = "[";
	for (var x of scopeVals) {
		res += pretty(x) + ','
	}
	return res + ']'
}

function resolve(line, src, scopeNames, scopeValues) {
	verbose(`resolve ${line} with scope ${scopeNames} : ${pretty(scopeValues)} `)

	if (line == ".")
		return undefined;

	if (line[0] == '[') {
		var k = [];
		for (i of argParse(replaceAll(replaceAll(line.slice(1, -1), ', ', ' '), ',', ' '))) {
			k.push(resolve(i, src, scopeNames, scopeValues));
		}
		return k;
	}

	if (line[0] == '"') {
		var k = [];
		for (var i of line.slice(1, -1)) {
			k.push(i.charCodeAt());
		}
		return k;
	}

	if ("-.0123456789".indexOf(line[0]) != -1) {
		if (line[0] == '-') {
			return -resolve(line.slice(1), src, scopeNames, scopeValues);
		}
		else if (line.indexOf('.') != -1) {
			return parseFloat(line);
		}
		else {
			return parseInt(line);
		}
	}

	if (scopeNames.length != scopeValues.length) {
		// TODO write this info in a log file.
		console.error("Internal Error: Overloaded Scope.");
		return;
	}

	if (scopeNames.indexOf(line) != -1) {
		return scopeValues[scopeNames.indexOf(line)]
	}

	var tokens = argParse(line);
	var name = tokens[0];
	var args = tokens.slice(1);

	if (BUILTINS.hasOwnProperty(name))
		return BUILTINS[name](args, src, scopeNames, scopeValues);
	else if (EXTENSIONS.hasOwnProperty(name))
		return EXTENSIONS[name].apply({}, args.map(arg => resolve(arg, src, scopeNames, scopeValues)));
	else {
		verbose(`user func ${name} `);

		if (args.length && args[0] == '$') {
			verbose('manual scope injection');
			return call(src, name, args.slice(1).map(arg => resolve(arg, src, scopeNames, scopeValues)), scopeNames, scopeValues);
		} else {
			return call(src, name, args.map(arg => resolve(arg, src, scopeNames, scopeValues)));
		}
	}
}

function call(src, func, args, injectNames, injectValues) {
	if (func == undefined)
		func = "main"
	if (args == undefined)
		args = []
	if (injectNames == undefined)
		injectNames = []
	if (injectValues == undefined)
		injectValues = []

	var currLine = 0;

	var srcArr = src.split('\n');


	for (var line of srcArr) {
		tokens = argParse(line)
		if (tokens.length != 0 && tokens[0] == func && tokens[tokens.length - 1] == ":")
			break;
		currLine += 1;
	}

	if (currLine == srcArr.length) {
		console.error(`Symbol ${func} is not defined.`);
		return;
	}

	for (var i = currLine; i < srcArr.length; i++) {
		tokens = argParse(srcArr[i]);
		if (tokens.length != 0 && tokens[0] == 'ret')
			break;
	}

	var retLoc = i;

	var tokens = argParse(srcArr[currLine]);
	verbose(`function header ${srcArr[currLine]} `);
	verbose(`arg tokens ${tokens.slice(1, -1)} `);

	var localNames = injectNames;
	var localValues = injectValues;

	if (tokens.slice(1, -1).length > args.length) {
		console.error("Missing arguments");
		return;
	}

	for (var tok of tokens.slice(1, -1))
		localNames.push(tok);

	for (var arg of args) {
		localValues.push(arg);
	}

	// logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

	while (currLine < retLoc) {
		currLine += 1;

		tokens = argParse(srcArr[currLine]);

		// if len(tokens) and tokens[-1]==":":
		// 	logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

		// no execute
		if (tokens.length == 0 || tokens[0] == "%" || tokens.slice(-1)[0] == ":")
			continue;
		// logLine(srcArr[currLine], str(list(zip(localNames, localValues))))


		// assignment
		if (tokens.length >= 2 && tokens[1] == '=') {
			var name = tokens[0].trim();
			var value = tokens.slice(2).join(' ');
			var i = localNames.indexOf(name)
			if (i != -1) {
				localValues[i] = resolve(value, src, localNames, localValues);
			}
			else {
				localValues.push(resolve(value, src, localNames, localValues));
				localNames.push(name);
			}
		}

		// returns
		else if (tokens[0] == "ret") {
			verbose(`returning ${tokens.slice(1)} `)

			if (tokens.length == 1) {
				return undefined;
			}
			else {
				return resolve(tokens[1], src, localNames, localValues)
			}
		}

		// control structures
		else if (tokens[0] == 'ifEq') {
			var args = tokens.slice(1);

			if (args.length == 2) {
				var dest = "end";
			} else {
				var dest = args[2];
			}
			if ((dest == "end") ^ (resolve(args[0], src, localNames, localValues) == resolve(args[1], src, localNames, localValues))) {
				while (argParse(srcArr[currLine]).length == 0 || argParse(srcArr[currLine])[0] != dest) {
					{
						currLine += dest == "while" ? -1 : 1
					}
				}
			}
		}
		else if (tokens[0] == 'ifLess') {
			var args = tokens.slice(1);

			if (args.length == 2) {
				var dest = "end";
			} else {
				var dest = args[2];
			}
			if ((dest == "end") ^ (resolve(args[0], src, localNames, localValues) < resolve(args[1], src, localNames, localValues))) {
				while (argParse(srcArr[currLine]).length == 0 || argParse(srcArr[currLine])[0] != dest) {
					currLine += dest == "while " ? -1 : 1
				}
			}
		}
		// arbitrary function call
		else {
			verbose(`root function call { ${srcArr[currLine]} } `);
			resolve(srcArr[currLine], src, localNames, localValues);
		}
	}

}

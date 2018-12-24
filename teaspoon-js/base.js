
function resolve(line, src, scopeNames, scopeValues) {
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
	}

	tokens = argParse(srcArr[currLine]);
	verbose(`function header ${srcArr[currLine]}`));
	verbose(`arg tokens ${tokens.slice(1, -1)}`);

	localNames = injectNames;
	localValues = injectValues;

	if len(tokens.slice(1, -1)) > len(args):
		console.error("Missing arguments");

	for (var tok of tokens.slice(1, -1))
		localNames.push(tok);

	for (var arg of args) {
		localValues.push(arg);
	}

	// logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

	while (argParse(srcArr[currLine]).length && argParse(srcArr[currLine])[0] != 'ret') {
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
			verbose(`returning ${tokens.slice(1)}`)

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
					currLine += dest == "while " ? -1 : 1
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
			verbose(`root function call {${srcArr[currLine]}}`);
			resolve(srcArr[currLine], src, localNames, localValues);
		}
	}



}
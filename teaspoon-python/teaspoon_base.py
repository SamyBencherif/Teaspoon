#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys

VERBOSE = 0
STEP = 0

RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
YELLOW  = "\033[36m"
DEFAULT = "\033[0m"

VERSION = ["base"]

EXTENSIONS = {}

def verbose(info):
	if VERBOSE:
		print (info)

def logLine(line, scope):
	if STEP:
		if input (YELLOW + line + DEFAULT):
			print(BLUE + scope + DEFAULT)

def argParse(line):
	if line.strip() == "":
		return []

	k = []
	inQuotes = 0
	acc = ""
	for i in line.strip():
		if i=='"':
			inQuotes = ~inQuotes
		if ~inQuotes and i==" ":
			k.append(acc)
			acc = ""
		else:
			acc += i
	k.append(acc)

	return k

def resolve(line, src, scopeNames, scopeValues):
	verbose('resolve {} with scope {} : {}'.format(line, scopeNames, scopeValues))

	if line[0]=='[':
		k = []
		for i in argParse(line[1:-1].replace(', ', ' ').replace(',', ' ')):
			k.append(resolve(i, src, scopeNames, scopeValues))
		return k

	if line[0]=='"':
		k = []
		for i in line[1:-1]:
			k.append(ord(i))
		return k

	if line[0] in "-.0123456789":
		if line[0]=="-" and line[1] != "-.0123456789":
			return -resolve(line[1:], src, scopeNames, scopeValues)
		elif '.' in line:
			return float(line)
		else:
			return int(line)

	if line in scopeNames:
		return scopeValues[scopeNames.index(line)]

	tokens = argParse(line)
	name = tokens[0]
	args = tokens[1:]

	# builtins
	if name == "print":
		print(''.join([chr(x) for x in resolve(args[0], src, scopeNames, scopeValues)])) # process string literal or vars
		return;
	elif name == "require":
		if not ''.join([chr(x) for x in resolve(args[0], src, scopeNames, scopeValues)]) in VERSION:
			# print(VERSION[0], args[0])
			print('This program is not compatible with this version of Teaspoon. It requires teaspoon_{}.'.format(''.join([chr(x) for x in resolve(args[0], src, scopeNames, scopeValues)])))
			exit(1)
	elif name == "get":
		return resolve(args[0], src, scopeNames, scopeValues)[resolve(args[1], src, scopeNames, scopeValues)]
	elif name == "add":
		return resolve(args[0], src, scopeNames, scopeValues).append(resolve(args[1], src, scopeNames, scopeValues))
	elif name == "sum":
		return sum([resolve(arg, src, scopeNames, scopeValues) for arg in args])
	elif name == "mul":
		return resolve(args[0], src, scopeNames, scopeValues) * resolve(args[1], src, scopeNames, scopeValues)
	elif name == "len":
		return len(resolve(args[0], src, scopeNames, scopeValues))
	# extensions
	elif name in EXTENSIONS.keys():
		return EXTENSIONS[name](*[resolve(arg, src, scopeNames, scopeValues) for arg in args])
	# user defined
	else:
		verbose ('user func {}'.format(name))
		call(src, name, [resolve(arg, src, scopeNames, scopeValues) for arg in args])

def call(src, func, args, scopeInject=[]):

	verbose('call {} with args {}'.format(func, args))

	currLine = 0

	srcArr = src.split('\n')

	for line in srcArr:
		tokens = argParse(line)
		if len(tokens)==0:
			pass
		elif tokens[0] == func and tokens[-1] == ":":
			break
		currLine += 1

	if currLine == len(srcArr):
		raise NameError("Symbol {} is not defined.".format(func))

	for i in range(currLine, len(srcArr)):
		tokens = argParse(srcArr[i])
		if len(tokens)==0:
			pass
		elif tokens[0] == "ret":
			break

	retLoc =  i

	tokens = argParse(srcArr[currLine])
	verbose ('function header {}'.format(srcArr[currLine]))
	verbose ('arg tokens {}'.format(tokens[1:-1]))

	#TODO: arg and local scope don't need to be seperate

	# argNames = tokens[1:-1]
	# argValues = args

	localNames = tokens[1:-1]
	localValues = args

	logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

	# step
	while currLine < retLoc:


		currLine += 1

		tokens = argParse(srcArr[currLine])

		# no execute
		if len(tokens) == 0 or tokens[0]=="%" or tokens[-1]==":":
			continue
		logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

		# assignment
		if len(tokens) >= 2 and tokens[1] == "=":
			name = tokens[0].strip()
			value = ' '.join(tokens[2:])
			if name in localNames:
				localValues[localNames.index(name)] = resolve(value, src, localNames, localValues)
			else:
				verbose('initializing {}'.format(name))
				verbose('scope {}'.format(localNames))
				localValues.append(resolve(value, src, localNames, localValues))
				localNames.append(name)

		# returns
		elif tokens[0] == "ret":
			verbose('returning {}'.format(tokens[1:]))
			if len(tokens) == 1:
				return None
			else:
				return resolve(tokens[1], src, localNames, localValues)

		# control structures
		elif tokens[0] == "ifEq":
			args = tokens[1:]

			if len(args) == 2:
				dest = "end"
			else:
				dest = args[2]
			if (dest=="end") ^ (resolve(args[0], src, localNames, localValues) == resolve(args[1], src, localNames, localValues)):
				while len(argParse(srcArr[currLine])) == 0 or argParse(srcArr[currLine])[0] != dest:
					currLine += -1 if dest=="while" else 1

		elif tokens[0] == "ifLess":
			args = tokens[1:]

			if len(args) == 2:
				dest = "end"
			else:
				dest = args[2]
			if (dest=="end") ^ (resolve(args[0], src, localNames, localValues) < resolve(args[1], src, localNames, localValues)):
				while len(argParse(srcArr[currLine])) == 0 or argParse(srcArr[currLine])[0] != dest:
					currLine += -1 if dest=="while" else 1

		else: # arbitrary function call
			verbose("root function call {{{}}}".format(srcArr[currLine]))
			resolve(srcArr[currLine], src, localNames, localValues)

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	call(src, "main", [])